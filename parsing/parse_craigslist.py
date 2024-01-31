import csv
import requests

# format: [id, date, city, ti_n, title, po_n, post, pi_n, pictures, price]
def get_image_urls():
    filepath = 'real.csv'
    urls = [] # format: [id, title]
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip headers
        for row in reader:
            url_list = row[8].split(' ')
            for url in url_list:
                urls.append(url)
    urls = [x for x in urls if x != '']
    return urls
def check_images(image_urls):
    success, fail = 0, 0
    for url in image_urls:
        try:
            response = requests.get(url)
            # Check if the Content-Type header indicates an image
            if 'image' in response.headers.get('Content-Type', ''):
                success += 1
            else:
                print(url)
                fail += 1
        except:
            fail += 1
    print("Success: " + str(success))
    print("Fail: " + str(fail))

    with open('results.txt', 'a') as file:
        file.write(f"{success}\n")
        file.write(f"{fail}\n")

def main():
    urls = get_image_urls()
    batch = urls[:100]
    check_images(batch)

if __name__ == "__main__":
    main()
