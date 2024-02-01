import csv
import random
import json

#format: [index,date,city,ti_n,title,po_n,post,pi_n,pictures,price,username]
def get_image_file_names():
    filepath = 'offerup_sample_data.csv'
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip headers
        posts = []
        for row in reader:
            id_title_images = tuple()
            id = row[0]
            title = row[4]
            images = row[8]

            data_map = json.loads(images)
            file_names = list(data_map.values())
            id_title_images = id, title, file_names
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
