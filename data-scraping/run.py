import requests
from bs4 import BeautifulSoup

# Set custom headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Open the file containing the list of URLs and read line by line
with open("perfume-links.txt", "r") as url_file:
    urls = url_file.readlines()

# Open a result file to save the output
with open("result.txt", "w") as result_file:
    for url in urls:
        url = url.strip()  # Remove any extra whitespace/newline characters

        if not url:  # Check if the URL is empty
            print("Empty URL encountered. Skipping...")
            continue

        if not url.startswith(("http://", "https://")):  # Validate URL schema
            print(f"Invalid URL: {url}. Skipping...")
            continue

        print(f"Processing: {url}")

        # Send an HTTP request to get the page content with headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Page loaded successfully")
        else:
            print(f"Failed to load page. Status code: {response.status_code}")
            continue  # Skip to the next URL if the page failed to load

        # Parse the page content with BeautifulSoup
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the perfume name from the <h1> tag with itemprop="name"
        perfume_name_tag = soup.find("h1", itemprop="name")
        if perfume_name_tag:
            perfume_name = perfume_name_tag.text.strip()
            print(f"Perfume Name: {perfume_name}")
        else:
            print("Could not find the perfume name.")
            perfume_name = "Unknown Perfume Name"

        # Write the perfume name to the result file
        result_file.write(f"Perfume Name: {perfume_name}\n")

        # Extract the product image URL from <img itemprop="image">
        image_tag = soup.find("img", itemprop="image")
        if image_tag:
            image_url = image_tag.get("src", "No image found")
            print(f"Image URL: {image_url}")
            result_file.write(f"Image URL: {image_url}\n")
        else:
            print("Could not find the image.")

        # Extract the notes from the specific div structure
        notes_divs = soup.find_all(
            "div", style=lambda value: value and "display: flex" in value
        )
        if notes_divs:
            print(f"Found {len(notes_divs)} notes elements.")
            for note_div in notes_divs:
                # Look for the <div> containing the <a> tag which holds the note name
                note_name_tag = note_div.find("a")
                if note_name_tag:
                    note_name = note_name_tag.text.strip()
                    print(f"Note: {note_name}")
                    result_file.write(f"Note: {note_name}\n")
        else:
            print("Could not find any notes.")

        # Extract the collection name from the <span> with 'small' tag
        collection_tag = soup.find("span")
        if collection_tag and "Collections" in collection_tag.get_text():
            collection_name = (
                collection_tag.get_text().replace("Collections", "").strip()
            )
            print(f"Collection Name: {collection_name}")
            result_file.write(f"Collection Name: {collection_name}\n")
        else:
            print("Could not find the collection name.")

        # Find all elements with the class 'accord-bar' for accords
        accord_elements = soup.find_all("div", class_="accord-bar")
        if not accord_elements:
            print("Could not find any accord elements.")
        else:
            print(f"Found {len(accord_elements)} accord elements.")
            # Loop through all the accord elements and extract accord information
            for accord in accord_elements:
                accord_name = accord.text.strip()
                style = accord.get("style", "")
                background_color = ""
                width = ""

                # Parse the style attribute for background color and width
                if "background" in style:
                    background_color = (
                        style.split("background:")[1].split(";")[0].strip()
                    )

                if "width" in style:
                    width = style.split("width:")[1].split(";")[0].strip()

                # Write the extracted data to the result file
                result_file.write(
                    f"Accord: {accord_name}, Background Color: {background_color}, Width: {width}\n"
                )

        # Add a separator between perfume entries
        result_file.write("\n---\n\n")

print("Data extraction complete! Check the 'result.txt' file.")
