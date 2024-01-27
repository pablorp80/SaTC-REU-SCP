import csv

# format: [id, date, city, ti_n, title, po_n, post, pi_n, pictures, price]
def get_data():
    filepath = 'real.csv'
    titles = [] # format: [id, title]
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip headers
        for row in reader:
            titles.append((row[0], row[4])) # id and title
    return titles
