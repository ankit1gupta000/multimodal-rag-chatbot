from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("test_upload.pdf", pagesize=letter)
c.setFont("Helvetica", 12)
c.drawString(72, 720, "This is a test PDF used for end-to-end testing.")
c.drawString(72, 700, "It contains several lines of text to ensure extraction works.")
c.save()
print("test_upload.pdf created")
