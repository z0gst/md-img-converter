import os
import re
from PIL import Image

def convert_images_to_webp(directory_or_file):
    total_files_converted = 0
    total_space_saved = 0

    # Check if the input is a directory or a Markdown file
    if os.path.isdir(directory_or_file):
        md_files = [f for f in os.listdir(directory_or_file) if f.endswith('.md')]
    elif os.path.isfile(directory_or_file) and directory_or_file.endswith('.md'):
        md_files = [os.path.basename(directory_or_file)]
        directory_or_file = os.path.dirname(directory_or_file)
    else:
        print("Invalid input. Please provide a directory or a Markdown file.")
        return

    # Process each Markdown file
    for md_file in md_files:
        with open(os.path.join(directory_or_file, md_file), 'r') as file:
            content = file.read()
        
        updated_content = content
        
        # Find all PNG image links in the Markdown file
        image_links = re.findall(r'!\[.*?\]\((.*?\.png)\)', content)
        
        for image_link in image_links:
            image_path = os.path.join(directory_or_file, image_link)
            if os.path.exists(image_path):
                webp_image_path = image_path.replace('.png', '.webp')
                original_size = os.path.getsize(image_path)
                
                # Convert PNG image to WebP format
                image = Image.open(image_path)
                image.save(webp_image_path, 'webp')
                os.remove(image_path)
                new_size = os.path.getsize(webp_image_path)
                total_files_converted += 1
                total_space_saved += (original_size - new_size)
                webp_image_relative_path = os.path.relpath(webp_image_path, directory_or_file)
                
                # Update the Markdown content with the new WebP image link
                updated_content = updated_content.replace(image_link, webp_image_relative_path)
        
        # Write the updated content back to the Markdown file
        with open(os.path.join(directory_or_file, md_file), 'w') as file:
            file.write(updated_content)
    
    # Print the total space saved and the number of files converted
    if total_space_saved > 1024 * 1024:
        print(f"Total space saved: {total_space_saved / (1024 * 1024):.2f} MB")
    else:
        print(f"Total space saved: {total_space_saved / 1024:.2f} KB")
    print(f"Total files converted: {total_files_converted}")

if __name__ == "__main__":
    input_path = input("Enter a Markdown file or a directory: ")
    convert_images_to_webp(input_path)
