import os
import json
import base64

def save_base64_image(base64_string, filename):
    """Decodes a base64 image string and saves it as a file."""
    try:
        # Typically base64 images come as "data:image/png;base64,iVBORw0KGgo..."
        # Split the header from the actual encoded data
        header, encoded = base64_string.split(",", 1)
        img_data = base64.b64decode(encoded)  # Decode base64
        with open(filename, "wb") as img_file:
            img_file.write(img_data)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def extract_images_from_obj(obj, output_dir, image_key="url", image_counter_start=0):
    """
    Recursively traverses a dict (or list of dicts) and saves base64-encoded PNG images.
    Returns the total number of images saved (to help with incremental counters).
    """
    img_counter = image_counter_start

    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == image_key and isinstance(v, str) and v.startswith("data:image/png;base64,"):
                # Found a base64-encoded image
                filename = os.path.join(output_dir, f"image_{img_counter}.png")
                save_base64_image(v, filename)
                img_counter += 1
            else:
                # Recursively look deeper
                if isinstance(v, (dict, list)):
                    img_counter = extract_images_from_obj(v, output_dir, image_key, img_counter)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                img_counter = extract_images_from_obj(item, output_dir, image_key, img_counter)

    return img_counter

def process_json(json_path):
    """Reads JSON file and groups images into folders by pairs."""
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # The parent directory for all extracted images
    base_output_dir = "extracted_images"
    os.makedirs(base_output_dir, exist_ok=True)

    # Ensure your JSON has a structure like:
    # {
    #   "pairs": [ { ...pair 1... }, { ...pair 2... }, ... ]
    # }
    # If your structure is different, adjust accordingly.
    pairs = data.get("pairs")
    if not pairs or not isinstance(pairs, list):
        print("No 'pairs' list found in the JSON. Check your data structure.")
        return

    total_images_saved = 0

    # Iterate over each pair
    for pair_index, pair_data in enumerate(pairs):
        # Create a subdirectory for this pair
        pair_dir = os.path.join(base_output_dir, f"pair_{pair_index}")
        os.makedirs(pair_dir, exist_ok=True)

        # Recursively extract images from the current pair object
        print(f"\nProcessing pair_{pair_index}...")
        total_images_saved = extract_images_from_obj(
            pair_data,
            output_dir=pair_dir,
            image_key="url",
            image_counter_start=total_images_saved
        )

    print(f"\nTotal images saved across all pairs: {total_images_saved}")

if __name__ == "__main__":
    json_file_path = "/Users/jameswong/PycharmProjects/ui-validator/report.json"
    process_json(json_file_path)
