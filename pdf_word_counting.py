import os
import PyPDF2

books = {}
directory = '../books/'

for file_name in os.listdir(directory):
    if file_name.endswith('.pdf'):
        try:
            file = open(os.path.join(directory, file_name), 'rb')
            pdfReader = PyPDF2.PdfReader(file)

            content = ""
            for page in pdfReader.pages:
                content += page.extract_text()

            if content:
                books[file_name] = len(content.split())
            else:
                print(f"No text found in the PDF: {file_name}")
        finally:
            file.close()
total_length = 0
number_of_books = 0
for book, length in books.items():
    print(f"{book} : {length}")
    total_length += length
    number_of_books += 1
print(f"books: {number_of_books}")
print(f"words: {total_length}")
