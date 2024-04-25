import os
from reportlab.lib.pagesizes import letter
import csv
from reportlab.pdfgen import canvas
from PIL import Image
from parse_craigslist import get_image_file_names

def wrap_text(text, width, c):
    paragraphs = text.split('\n')
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        words = paragraph.split()
        lines = []
        line = ''
        for word in words:
            test_line = f"{line} {word}".strip()
            if c.stringWidth(test_line, 'Helvetica', 12) < width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        wrapped_paragraphs.append(lines)
    return wrapped_paragraphs

def load_cluster_data(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        cluster_data = {}
        for row in reader:
            cluster = row[0]
            post_ids = row[1].split(', ')  # Split the string into individual post IDs
            cluster_data[cluster] = post_ids
        return cluster_data

def compile_cluster_documents():
    all_posts = get_image_file_names()
    posts_dict = {post[0]: post for post in all_posts}

    cluster_data = load_cluster_data('../try.csv')  # Update the filename as needed

    pdf_filename = 'maybe_right.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    margin = 72
    text_width = width - 2 * margin
    line_height = 14

    for cluster_num, post_ids in cluster_data.items():
        y_position = height - margin  # Reset position for each cluster
        c.drawString(margin, y_position, f'{cluster_num}')
        y_position -= 2 * line_height  # Move down to start post content

        for post_id in post_ids:
            if post_id in posts_dict:
                if y_position < margin + 3 * line_height:  # Check if we need a new page for the next post
                    c.showPage()
                    y_position = height - margin
                c.drawString(margin, y_position, f'Post ID: {post_id}')  # Post header
                y_position -= 2 * line_height

                _, text, image_paths = posts_dict[post_id]
                title, description = text.split('\n', 1)
                wrapped_title = wrap_text(title, text_width, c)
                wrapped_description = wrap_text(description, text_width, c)

                for paragraph in wrapped_title + wrapped_description:
                    for line in paragraph:
                        if y_position < margin + line_height:  # New page if not enough space for line
                            c.showPage()
                            y_position = height - margin
                        c.drawString(margin, y_position, line)
                        y_position -= line_height
                    y_position -= line_height  # Extra space between paragraphs

                # Add images for each post
                for image_path in image_paths:
                    image_path = '../.assets/images/' + image_path
                    if os.path.exists(image_path) and os.access(image_path, os.R_OK):
                        if y_position < margin + 100:  # Check space for image
                            c.showPage()
                            y_position = height - margin
                        try:
                            img = Image.open(image_path)
                            img_width, img_height = img.size
                            aspect = img_width / float(img_height)
                            img_width, img_height = (text_width, text_width / aspect) if aspect > 1 else ((text_width * aspect), text_width)
                            c.drawImage(image_path, margin, y_position - img_height, width=img_width, height=img_height)
                            y_position -= img_height + 24  # Extra space after image
                        except Exception as e:
                            print(f"Error adding image {image_path}: {e}")

                # Separate posts by a visible line or space
                y_position -= line_height  # Extra space before the separator
                if y_position > margin:
                    c.line(margin, y_position, width - margin, y_position)
                    y_position -= line_height  # Space after the separator

        c.showPage()

    c.save()
    print(f"Document compiled: {pdf_filename}")

if __name__ == "__main__":
    compile_cluster_documents()
