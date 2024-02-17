import csv
import random
import json

# format: [id, date, city, ti_n, title, po_n, post, pi_n, pictures, price]
def get_image_file_names():
    filepath = 'data.csv'
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip headers
        posts = []
        for row in reader:
            id_title_images = tuple()
            id = row[0]
            title = row[4]
            description = row[6]
            images = row[8]

            if (title.strip() and description.strip()):
                text = title + '\n' + description

                processed_data_str = images.replace('""', '"')
                data_map = json.loads(processed_data_str)
                file_names = list(data_map.values())
                file_names = [x for x in file_names if x]
                if len(file_names) > 0:
                    id_title_images = id, text, file_names
                    posts.append(id_title_images)

    return posts

def main():
    id_title_imagepaths = get_image_file_names()
    post_id, title, images = random.choice(id_title_imagepaths)
    print(post_id + '\n\n' + title + '\n\n')
    for image in images:
        print(image)

if __name__ == "__main__":
    main()
