import csv

def get_data():
    filepath = 'craigslist_sample_dataset_no_dup.csv'
    data = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip headers
        for row in reader:
            data.append(row)
    return data

def main():
    data = get_data()

    for row in data:
        for attr in row:
            # Do something with attr

if __name__ == "__main__":
    main()
