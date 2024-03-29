import csv
import json

def get_image_file_names():
    filepath = 'full_data.csv'
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip headers
        posts = []
        for row in reader:
            id_title_images = tuple()
            id = row[0]
            title = row[5].strip()
            description = row[7].strip()
            images = row[9]

            if (title and description):
                text = title + '\n' + description

                processed_data_str = images.replace('""', '"')
                data_map = json.loads(processed_data_str)
                file_names = list(data_map.values())
                file_names = [x for x in file_names if x]
                if len(file_names) > 0:
                    id_title_images = id, text, file_names
                    posts.append(id_title_images)
    return posts
