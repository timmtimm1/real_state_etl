from pathlib import Path
import json


def clean_urls():
    # Use the correct path
    input_dir = Path('realstate/property_urls')
    output_dir = Path('realstate/clean_urls')
    output_dir.mkdir(exist_ok=True)

    print("Starting URL cleaning process...")

    # Read and process each JSON file
    for json_file in input_dir.glob('*.json'):
        try:
            # Get state from filename
            state = json_file.stem.split('_')[0]  # Gets the state code (sp, rj, etc)

            print(f"\nProcessing {state.upper()}...")

            # Read the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Get URLs and remove duplicates
            if 'urls' in data:
                original_urls = data['urls']
                unique_urls = list(set(original_urls))

                print(f"Original URLs: {len(original_urls)}")
                print(f"Unique URLs: {len(unique_urls)}")
                print(f"Removed {len(original_urls) - len(unique_urls)} duplicates")

                # Save clean data
                clean_data = {
                    'state': state.upper(),
                    'total_urls': len(unique_urls),
                    'urls': unique_urls
                }

                # Save to new file
                output_file = output_dir / f'{state}_clean.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(clean_data, f, ensure_ascii=False, indent=2)

            else:
                print(f"No URLs found in {json_file.name}")

        except Exception as e:
            print(f"Error processing {json_file.name}: {str(e)}")

    print("\nCleaning process completed!")
    print(f"Clean files saved in: {output_dir}")


if __name__ == "__main__":
    clean_urls()