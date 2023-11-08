import os

# Function to replace text according to specified rules
def replace_text(original_text):
    replacements = {
        '>': '>\n',
        'stroke-width': 'strokeWidth',
        'stop-color': 'stopColor',
        'stop-opacity': 'stopOpacity'
    }
    for old, new in replacements.items():
        original_text = original_text.replace(old, new)
    return original_text

# Function to process all .svg files in a directory
def process_svgs(directory):
    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print("The provided directory does not exist.")
        return

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        # Check if the file is an .svg
        if filename.endswith('.svg'):
            filepath = os.path.join(directory, filename)
            # Read the content of the .svg file
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace the text
            updated_content = replace_text(content)

            # Write the updated content back to the file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(updated_content)

            print(f"Processed {filename}")

# Replace 'your_directory_path_here' with the path to the directory containing your .svg files
# Example: process_svgs('/path/to/your/svg/folder')
process_svgs('C:\\Users\\calvi\\3D Objects\\glyptoshop\\public')
