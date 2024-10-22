#!/bin/bash

# Define the base URL for the product service
URL="http://localhost:5003/add_product"

# Loop to add 20 products
for i in {1..20}; do
  # Randomize product data
  product_name="Product_$i"
  manufacturer="Manufacturer_$((i % 5))"
  designer="Designer_$((i % 3))"
  collection_name="Collection_$((i % 4))"
  notes=("Citrus" "Woody" "Floral" "Spicy" "Vanilla")
  accords=("Fresh" "Warm" "Earthy" "Sweet" "Citrusy")
  seasons=("Summer" "Winter" "Spring" "Autumn")

  # Create JSON payload and send request using HTTPie
  http POST $URL \
    name="$product_name" \
    manufacturer="$manufacturer" \
    designer="$designer" \
    collection="$collection_name" \
    note:='["'${notes[$((i % 5))]}'"]' \
    accords:='["'${accords[$((i % 5))]}'"]' \
    seasons:='["'${seasons[$((i % 4))]}'"]'

  echo -e "\nAdded product $i: $product_name"

done

echo "Finished adding 20 products."
