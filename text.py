import fitz  # PyMuPDF
pdf_document = fitz.open("test.pdf")
for page in pdf_document:
    print(page.get_text())
    # Save the text to a file
    with open("output.txt", "w") as text_file:
        text_file.write(page.get_text())
