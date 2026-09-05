import pymupdf
from pathlib import Path


def extract_images(pdf_path, output_dir="results/images"):
    """
    Extract all embedded images from a PDF.

    Returns metadata about every extracted image.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    document = pymupdf.open(pdf_path)

    extracted_images = []

    for page_number, page in enumerate(document, start=1):

        images = page.get_images(full=True)

        for image_number, image in enumerate(images, start=1):

            xref = image[0]

            image_data = document.extract_image(xref)

            image_bytes = image_data["image"]
            image_ext = image_data["ext"]

            filename = (
                f"page_{page_number:03d}"
                f"_image_{image_number:02d}."
                f"{image_ext}"
            )

            image_path = output_dir / filename

            with open(image_path, "wb") as file:
                file.write(image_bytes)

            extracted_images.append({
                "source": pdf_path.name,
                "page": page_number,
                "type": "image",
                "image_number": image_number,
                "path": str(image_path),
                "width": image_data["width"],
                "height": image_data["height"],
                "extension": image_ext
            })

    document.close()

    return extracted_images