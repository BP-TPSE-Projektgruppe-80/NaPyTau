def ingest_file(filename: str) -> str:
    # Ingest data from a file
    with open(filename) as f:
        data = f.read()
    return data
