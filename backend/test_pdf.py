from pdf_service import extract_pdf_text

pdf_path = r"C:\Users\ankit\Downloads\Research paper.pdf"

text = extract_pdf_text(pdf_path)

print(text[:1000])