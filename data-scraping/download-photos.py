import os
import requests

# Create the images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Open the result.txt file for reading
with open("result.txt", "r") as file:
    lines = file.readlines()

# Initialize a list to store image URLs
image_urls = []

# Extract image URLs from the file
for line in lines:
    if line.startswith("Image URL:"):
        # Get the URL by stripping whitespace and splitting
        image_url = line.split(":", 1)[1].strip()
        image_urls.append(image_url)

# Download each image
for url in image_urls:
    try:
        # Get the image name from the URL
        image_name = os.path.basename(url)
        # Send a GET request to fetch the image
        response = requests.get(url)

        if response.status_code == 200:  # Check if the request was successful
            # Save the image in the images directory
            with open(os.path.join("images", image_name), "wb") as img_file:
                img_file.write(response.content)
            print(f"Downloaded: {image_name}")
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")
