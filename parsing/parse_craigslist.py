import csv
import random
import requests
import json

# format: [id, date, city, ti_n, title, po_n, post, pi_n, pictures, price]
def get_image_file_names():
    filepath = 'data.csv'
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip headers
        id_to_image_names = {}
        for row in reader:
            id = row[0]
            images = row[8]
            processed_data_str = images.replace('""', '"')
            data_map = json.loads(processed_data_str)
            file_names = list(data_map.values())
            id_to_image_names[id] = file_names

    return id_to_image_names


def check_images(image_urls):
    success, fail = 0, 0
    count = 0
    for url in image_urls:
        count += 1
        print(count)
        try:
            response = requests.get(url)
            if 'image' in response.headers.get('Content-Type', ''):
                success += 1
            else:
                fail += 1
        except:
            fail += 1
    print("Success: " + str(success))
    print("Fail: " + str(fail))

    with open('results2.txt', 'a') as file:
        file.write(f"{success}\n")
        file.write(f"{fail}\n")

def main():
    id_to_images = get_image_file_names()
    post_id, images = random.choice(list(id_to_images.items()))
    print(post_id + '\n')
    for image in images:
        print(image)


if __name__ == "__main__":
    main()
