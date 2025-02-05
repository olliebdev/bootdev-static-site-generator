def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
        else:
            raise Exception("No title heading found in markdown")
