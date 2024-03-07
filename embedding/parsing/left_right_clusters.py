import csv
import json
import os
import shutil
from cleantext import clean

def clean_text(text):
    return clean(text, no_line_breaks=True, no_urls=True, no_emails=True, no_phone_numbers=True, replace_with_url="", replace_with_email="", replace_with_phone_number="")

def read_valid_ids():
    left_ids = set()
    right_ids = set()
    with open('../labeling/left.txt', 'r', encoding='utf-8') as file:
        for line in file:
            left_ids.add(line.strip())
    with open('../labeling/right.txt', 'r', encoding='utf-8') as file:
        for line in file:
            right_ids.add(line.strip())
    return left_ids, right_ids

def get_samples(left_ids, right_ids):
    filepath = '../data.csv'
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip headers
        posts = []
        for row in reader:
            id = row[0]
            prefix = ""
            if id in left_ids:
                prefix = "left"
            elif id in right_ids:
                prefix = "right"
            else:
                continue  # Skip this post if the ID is not in either list

            id_with_prefix = prefix + id
            title = clean_text(row[4].strip())
            description = clean_text(row[6].strip())
            images = row[8]

            if title and description:
                text = title + '\n' + description

                processed_data_str = images.replace('""', '"')
                data_map = json.loads(processed_data_str)
                file_names = list(data_map.values())
                file_names = [x for x in file_names if x]
                if len(file_names) > 0:
                    id_title_images = (id_with_prefix, text, file_names)
                    posts.append(id_title_images)
    return posts

def main():
    left_ids, right_ids = read_valid_ids()  # Read the valid IDs before processing posts
    posts = get_samples(left_ids, right_ids)
    for post in posts:
        post_id, text, images = post

        # Create a directory for the post
        os.makedirs(post_id, exist_ok=True)

        # Copy images to the new directory
        for image in images:
            source_path = os.path.join('../.assets/images', image)
            destination_path = os.path.join(post_id, image)
            if os.path.exists(source_path):
                shutil.copy(source_path, destination_path)

        # Write title and description to text.txt in the new directory
        text_file_path = os.path.join(post_id, 'text.txt')
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(text)

if __name__ == "__main__":
    main()
