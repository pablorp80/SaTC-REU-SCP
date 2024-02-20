import csv
import json
from cleantext import clean

def clean_text(text):
    return clean(text,
                 fix_unicode=True,               # fix various unicode errors
                 to_ascii=True,                  # transliterate to closest ASCII representation
                 lower=True,                     # lowercase text
                 no_line_breaks=True,            # fully strip line breaks as opposed to only normalizing them
                 no_urls=True,                   # replace all URLs with a special token
                 no_emails=True,                 # replace all email addresses with a special token
                 no_phone_numbers=True,          # replace all phone numbers with a special token
                 no_numbers=False,               # do not replace numbers
                 no_digits=False,                # do not replace digits
                 no_currency_symbols=True,       # replace all currency symbols with a special token
                 no_punct=True)                  # fully remove punctuation


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
            title = clean_text(row[4].strip())
            description = clean_text(row[6].strip())
            images = row[8]

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
