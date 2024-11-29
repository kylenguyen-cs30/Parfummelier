import re

def extract_accords(file_path):
    accords = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r"Accord:\s*([\w\s,&-]+),\s*Background Color:\s*#([0-9a-fA-F]+)", line)
            if match:
                accord_name = match.group(1).strip()
                color_code = f"#{match.group(2)}"
                accords[accord_name] = color_code
    return accords

def write_accords_to_file(accords, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for accord, color in sorted(accords.items()):
            file.write(f"{accord}: {color}\n")

# Define file paths
input_file = "result.txt"
output_file = "distinct_accords.txt"

# Extract and write accords
accords = extract_accords(input_file)
write_accords_to_file(accords, output_file)

print(f"Extracted {len(accords)} distinct accords. Saved to '{output_file}'.")
