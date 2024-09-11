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

        # Find all elements with the class 'accord-bar' for accords
        accord_elements = soup.find_all("div", class_="accord-bar")

        if not accord_elements:
            print("Could not find any accord elements.")
        else:
            print(f"Found {len(accord_elements)} accord elements.")

        # Write the perfume name to the result file
        result_file.write(f"Perfume Name: {perfume_name}\n")

        # Loop through all the accord elements and extract accord information
        for accord in accord_elements:
            # Extract the accord name (text inside the div)
            accord_name = accord.text.strip()

            # Extract the background color (style attribute)
            style = accord.get("style", "")
            background_color = ""
            width = ""

            # Parse the style attribute for background color and width
            if "background" in style:
                background_color = style.split("background:")[1].split(";")[0].strip()

            if "width" in style:
                width = style.split("width:")[1].split(";")[0].strip()

            # Write the extracted data to the result file
            result_file.write(
                f"Accord: {accord_name}, Background Color: {background_color}, Width: {width}\n"
            )

        # Add a separator between perfume entries
        result_file.write("\n---\n\n")

print("Data extraction complete! Check the 'result.txt' file.")
