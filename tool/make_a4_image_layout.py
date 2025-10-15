import os
from PIL import Image
from reportlab.pdfgen import canvas

# Configuration
IMAGE_DIR = "./tag36h11_out"  # directory with PNGs
OUTPUT_PDF = "output.pdf"
DPI = 300
MARGIN = 0        # left/right/bottom margin (pixels)
TOP_MARGIN = 100  # extra top margin so printer can print header (pixels)
SPACING = 0       # spacing between images (pixels)
FONT_SIZE = 24    # font size for filename label
TEXT_MARGIN = 30  # margin between filename and image (pixels)


def main():
    images = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR)
              if f.lower().endswith(".png")]
    images.sort()  # sort files alphabetically
    if not images:
        print("No PNG files found in", IMAGE_DIR)
        return

    # A4 size in pixels at DPI
    mm_to_px = DPI / 25.4
    page_width = int(210 * mm_to_px)
    page_height = int(297 * mm_to_px)

    c = canvas.Canvas(OUTPUT_PDF, pagesize=(page_width, page_height))
    c.setFont("Helvetica", FONT_SIZE)

    # Start below top margin
    x, y = MARGIN, page_height - TOP_MARGIN
    max_row_height = 0

    for img_path in images:
        with Image.open(img_path) as img:
            w, h = img.size

        filename = os.path.splitext(os.path.basename(img_path))[0]
        label_height = FONT_SIZE + TEXT_MARGIN  # space for text + gap

        # Move to next row if no horizontal space
        if x + w + MARGIN > page_width:
            x = MARGIN
            y -= max_row_height + SPACING
            max_row_height = 0

        # Add new page if no vertical space
        if y - (h + label_height) - MARGIN < 0:
            c.showPage()
            c.setFont("Helvetica", FONT_SIZE)
            x, y = MARGIN, page_height - TOP_MARGIN
            max_row_height = 0

        # Draw filename centered above the image
        text_x = x + w / 2
        text_y = y - FONT_SIZE
        c.drawCentredString(text_x, text_y, filename)

        # Draw image below the text
        image_bottom_y = text_y - h - TEXT_MARGIN
        c.drawInlineImage(img_path, x, image_bottom_y, width=w, height=h)

        # Update for next image
        x += w + SPACING
        max_row_height = max(max_row_height, h + label_height)

    c.save()
    print(f"✅ PDF saved as {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
