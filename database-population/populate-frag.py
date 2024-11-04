import requests
import os

# Define the API endpoint
url = "http://localhost:5003/add_product"

# Path to results.txt file
file_path = "/Users/bryanmedina/Documents/Parfummelier/data-scraping/result.txt"


def parse_data(file_path):
    products = []
    with open(file_path, "r") as file:
        product = {}
        for line in file:
            line = line.strip()
            if line.startswith("Perfume Name:"):
                if product:
                    products.append(product)
                product = {"name": line.replace("Perfume Name:", "").strip()}
            elif line.startswith("Base Notes:"):
                product["notes"] = line.replace("Base Notes:", "").strip().split(", ")
            elif line.startswith("Accords:"):
                product["accords"] = line.replace("Accords:", "").strip().split(", ")
        if product:
            products.append(product)
    return products

# Function to send data to API
def send_to_api(product_data):
    response = requests.post(url, json=product_data)
    if response.status_code == 201:
        print(f"Product {product_data['name']} added successfully.")
    else:
        print(f"Failed to add product {product_data['name']}. Error: {response.text}")

def main():
    products = parse_data(file_path)
    if products:
        # Loop over products and send each one to the API
        for product in products:
            send_to_api(product)

if __name__ == "__main__":
    main()

