import os
from bs4 import BeautifulSoup

# Path to the folder containing the perfume HTML files
folder_path = "perfumes"

# Open a result file to save the output
with open("result.txt", "w") as result_file:
    # Iterate over all files in the perfumes folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            print(f"Processing: {file_path}")

            # Open and read the file content
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            # Parse the page content with BeautifulSoup
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

            # Extract the brand element
            brand_tag = soup.find("span", class_="brand")
            if brand_tag:
                brand_name = brand_tag.text.strip()
                print(f"Brand: {brand_name}")
                result_file.write(f"Brand: {brand_name}\n")
            else:
                print("Could not find the brand.")
                result_file.write("Brand: Unknown\n")

            # Extract notes section (as in your original script)
            # NOTE: Find Notes in HTML elements
            pyramid_section = soup.find(id="pyramid")
            if pyramid_section:
                # Extract the different note categories
                categories = pyramid_section.find_all("h4")
                for category in categories:
                    category_name = category.text.strip()
                    print(f"Category: {category_name}")
                    result_file.write(f"{category_name}:\n")

                    # Get the corresponding notes for each category
                    notes_div = category.find_next("pyramid-level")
                    if notes_div:
                        # Find all note items within this section
                        note_items = notes_div.find_all(
                            "div",
                            style=lambda style: style and "display: flex" in style,
                        )
                        if note_items:
                            for item in note_items:
                                # Extract the note name
                                note_name = item.get_text(strip=True)
                                print(f"Note: {note_name}")
                                result_file.write(f"- {note_name}\n")
                        else:
                            print(f"No notes found for {category_name}.")
                            result_file.write(
                                f"- No notes found for {category_name}.\n"
                            )
                    else:
                        print(f"No notes found for {category_name}.")
                        result_file.write(f"- No notes found for {category_name}.\n")
            else:
                print("Could not find any perfume notes.")

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
