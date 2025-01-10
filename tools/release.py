import os

def main() -> None:
    with open("pyproject.toml", "r") as config_file:
        lines = config_file.readlines()
        # find version line "version = "X.Y.Z""
        version_line = ""
        for line in lines:
            if "version" in line:
                version_line = line
                break

        version = version_line.split("=")[1].strip().replace('"', "")

        ## create a new git tag

        os.system(f"git tag {version}")
        os.system(f"git push origin {version}")

        print(f"Done! Tagged version {version}!")

if __name__ == "__main__":
    main()