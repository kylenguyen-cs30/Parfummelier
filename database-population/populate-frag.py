import re
import requests
import json


def parse_perfume_data(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    perfumes = content.split("\n\n---\n\n")
    parsed_data = []

    for perfume in perfumes:
        if not perfume.strip():
            continue

        perfume_data = {}

        # Extract name
        name_match = re.search(r"Perfume Name: (.*?)\n", perfume)
        if name_match and name_match.group(1) != "Unknown Perfume Name":
            perfume_data["name"] = name_match.group(1)
        else:
            continue

        # Extract brand (previously manufacturer)
        brand_match = re.search(r"Brand: (.*?)\n", perfume)
        if brand_match and brand_match.group(1) != "Unknown":
            perfume_data["brand"] = brand_match.group(
                1
            )  # Changed from 'manufacturer' to 'brand'
        else:
            continue

        # Extract image URL and get just the filename
        image_match = re.search(r"Image URL: .*?/(\d+x\d+\.\d+\.jpg)", perfume)
        if image_match:
            image_filename = image_match.group(1)
            perfume_data["imageURL"] = image_filename

        # Extract accords
        accords = []
        accord_matches = re.finditer(r"Accord: (.*?), Background Color:", perfume)
        for match in accord_matches:
            accords.append(match.group(1))
        perfume_data["accords"] = accords

        if perfume_data.get("name") and perfume_data.get(
            "brand"
        ):  # Changed from 'manufacturer' to 'brand'
            parsed_data.append(perfume_data)

    return parsed_data


def populate_database(data):
    api_endpoint = "http://localhost:8000/product/add_product"

    for perfume in data:
        try:
            print(f"Sending data: {json.dumps(perfume, indent=2)}")  # Debug print
            response = requests.post(
                api_endpoint, json=perfume, headers={"Content-Type": "application/json"}
            )

            if response.status_code == 201:
                print(f"Successfully added: {perfume['name']}")
            else:
                print(f"Failed to add {perfume['name']}: {response.text}")

        except Exception as e:
            print(f"Error adding {perfume['name']}: {str(e)}")


if __name__ == "__main__":
    file_path = "/Users/kyle/Developer/projects/Parfummelier/data-scraping/result.txt"
    perfume_data = parse_perfume_data(file_path)
    print(f"Found {len(perfume_data)} perfumes to add")
    populate_database(perfume_data)
