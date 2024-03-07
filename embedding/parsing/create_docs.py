import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

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

def compile_documents(group):
    pdf_filename = f"{group}_posts.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter  # Dimensions of the page
    margin = 72  # Margin size
    text_width = width - 2 * margin
    line_height = 14

    for dirname in os.listdir('.'):
        if dirname.startswith(group):
            text_file_path = os.path.join(dirname, 'text.txt')
            if os.path.exists(text_file_path):
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    wrapped_paragraphs = wrap_text(text, text_width, c)
                    y_position = height - margin
                    for paragraph in wrapped_paragraphs:
                        for line in paragraph:
                            if y_position < margin + line_height:
                                c.showPage()
                                y_position = height - margin
                            c.drawString(margin, y_position, line)
                            y_position -= line_height
                        y_position -= line_height

            y_position = max(y_position - 24, height - margin - 100)

            for image_name in os.listdir(dirname):
                if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_path = os.path.join(dirname, image_name)
                    try:
                        if y_position < margin + 100:
                            c.showPage()
                            y_position = height - margin

                        img = Image.open(image_path)
                        img_width, img_height = img.size
                        aspect = img_width / float(img_height)
                        img_width, img_height = (text_width, text_width / aspect) if aspect > 1 else ((text_width * aspect), text_width)
                        c.drawImage(image_path, margin, y_position - img_height, width=img_width, height=img_height)
                        y_position -= (img_height + 24)
                    except Exception as e:
                        print(f"Error adding image {image_path}: {e}")

            c.showPage()
    c.save()
    print(f"Document compiled: {pdf_filename}")

if __name__ == "__main__":
    compile_documents("left")
    compile_documents("right")
