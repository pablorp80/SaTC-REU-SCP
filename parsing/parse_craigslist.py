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
            url_list = row[8].split(',')
            for url in url_list:
                urls.append(url.strip())
    return urls
def check_images(image_urls):
    success, fail = 0, 0
    for url in image_urls:
        try:
            requests.get(url)
            success += 1
        except:
            fail += 1
    print("Success: " + str(success))
    print("Fail: " + str(fail))

    with open('results.txt', 'a') as file:
        file.write(f"{success}\n")
        file.write(f"{fail}\n")

def main():
    urls = get_image_urls()
    batch = urls[200:300]
    check_images(batch)

if __name__ == "__main__":
    main()
