import os
import json
import base64

def save_base64_image(base64_string, filename):
    """Decodes a base64 image string and saves it as a file."""
    try:
        header, encoded = base64_string.split(",", 1)  # Split header and encoded data
        img_data = base64.b64decode(encoded)  # Decode base64
        with open(filename, "wb") as img_file:
            img_file.write(img_data)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def process_json(json_path):
    """Reads JSON file, finds base64 images, and saves them with a sequential filename."""
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    img_counter = 0
    img_dir = "extracted_images"
    os.makedirs(img_dir, exist_ok=True)  # Create directory for images

    def extract_and_save(obj, key, path="root"):
        nonlocal img_counter
        if isinstance(obj, dict):
            for k, v in obj.items():
                current_path = f"{path}.{k}"
                # Check if the value is a base64-encoded PNG image
                if k == key and isinstance(v, str) and v.startswith("data:image/png;base64,"):
                    filename = os.path.join(img_dir, f"image_{img_counter}.png")
                    save_base64_image(v, filename)
                    print(f"Found image at: {current_path}, saved as: {filename}")
                    img_counter += 1
                else:
                    extract_and_save(v, key, current_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                extract_and_save(item, key, f"{path}[{i}]")

    # Look for the base64 image data in fields named "url"
    extract_and_save(data, "url")
    print(f"Total images saved: {img_counter}")

if __name__ == "__main__":
    json_file_path = "/Users/jameswong/PycharmProjects/ui-validator/report.json"
    process_json(json_file_path)
