import re


def extract_image_urls(text):
    urls = {}
    current_perfume = None

    for line in text.split("\n"):
        if line.startswith("Perfume Name: "):
            current_perfume = line.replace("Perfume Name: ", "").strip()
        elif line.startswith("Image URL: "):
            if current_perfume:
                url = line.replace("Image URL: ", "").strip()
                filename = url.split("/")[-1]
                urls[current_perfume] = filename

    return urls


def get_downloaded_files(downloads_text):
    pattern = r"375x500\.\d+\.jpg"
    return re.findall(pattern, downloads_text)


# NOTE: I don't know that i should keep this or not
def compare_files(urls_dict, downloaded_files):
    missing = {}
    duplicate_downloads = {}

    # find missing downloads
    for perfume, filename in urls_dict.items():
        if filename not in downloaded_files:
            missing[perfume] = filename

    # find dubplicate downloads
    filename_counts = {}
    for filename in downloaded_files:
        filename_counts[filename] = filename_counts.get(filename, 0) + 1

    for filename, count in filename_counts.items():
        if count > 1:
            # find perfumes using this filename
            perfumes = [name for name, f in urls_dict.items() if f == filename]
            duplicate_downloads[filename] = {"count": count, "perfumes": perfumes}

    return missing, duplicate_downloads


# add a funciton to load and process files
def analyze_files(result_file_path, downloads_file_path):
    with open(result_file_path, "r") as f:
        result_content = f.read()

    with open(downloads_file_path, "r") as f:
        downloads_content = f.read()

    urls_dict = extract_image_urls(result_content)
    downloaded_files = get_downloaded_files(downloads_content)

    filename_count = {}
    for filename in downloaded_files:
        filename_count[filename] = filename_count.get(filename, 0) + 1

    missing, duplicates = compare_files(urls_dict, downloaded_files)

    print(f"\nTotal perfumes: {len(urls_dict)}")
    print(f"Total downloaded files: {len(downloaded_files)}")

    duplicates = {f: c for f, c in filename_count.items() if c > 1}
    if duplicates:
        print("\nDuplicate downloads:")
        for filename, count in duplicates.items():
            print(f"- {filename} (downloaded {count} times)")

    # Find missing files
    required_files = set(urls_dict.values())
    downloaded_unique = set(downloaded_files)
    missing = required_files - downloaded_unique

    if missing:
        print("\nMissing downloads:")
        for filename in missing:
            perfumes = [name for name, f in urls_dict.items() if f == filename]
            print(f"- {filename} (needed for: {perfumes[0]})")


analyze_files("result.txt", "list-downloaded-photos.txt")
