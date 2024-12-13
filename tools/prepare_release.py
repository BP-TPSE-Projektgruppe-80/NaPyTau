from argparse import ArgumentParser
import os


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="The type of the release.",
        choices=["major", "minor", "patch"],
    )

    args = parser.parse_args()

    with open("pyproject.toml", "r") as config_file:
        lines = config_file.readlines()
        # find version line "version = "X.Y.Z""
        version_line = ""
        for line in lines:
            if "version" in line:
                version_line = line
                break

        version = version_line.split("=")[1].strip().replace('"', "")
        major, minor, patch = version.split(".")
        major, minor, patch = int(major), int(minor), int(patch)
        match args.type:
            case "major":
                major += 1
                minor = 0
                patch = 0
            case "minor":
                minor += 1
                patch = 0
            case "patch":
                patch += 1
        new_version = f"{major}.{minor}.{patch}"

    ## create a new git branch
    branch_name = f"release/{new_version}"
    os.system(f"git checkout -b {branch_name}")

    new_lines = []
    for line in lines:
        if "version" in line:
            line = f'version = "{new_version}"\n'
        new_lines.append(line)

    with open("pyproject.toml", "w") as config_file:
        config_file.writelines(new_lines)

    ## update the uv.lock file
    os.system("uv sync")

    ## commit the changes
    os.system("git add pyproject.toml")
    os.system("git add uv.lock")
    os.system(f'git commit -m "Bump version to {new_version}"')
    # os.system(f"git push origin {branch_name}")

    print(
        f"Done! Branch {branch_name} created! Please create a pull request to merge the changes." # noqa E501
    )


if __name__ == "__main__":
    main()
