def ingest_file(filename):
    # Ingest data from a file
    with open(filename) as f:
        data = f.read()
    return data
