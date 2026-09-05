import pymupdf
from pathlib import Path
from src.error_handler import setup_logging, log_error
from src.image_extractor import extract_images
from src.ocr_processor import extract_text_from_image


def load_pdf(pdf_path, image_output_dir="results/images"):
    """
    Load a PDF and extract text, tables, and images page by page.
    """

    pdf_path = Path(pdf_path)

    

    if not pdf_path.exists():
        error = FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

        log_error(error)
        raise error

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        tables = page.find_tables().tables

        extracted_tables = []

        for table in tables:
            extracted_tables.append(table.extract())

        images = []

        for image_number, image in enumerate(
            page.get_images(full=True),
            start=1
        ):

            xref = image[0]

            image_data = document.extract_image(xref)

            image_bytes = image_data["image"]
            image_ext = image_data["ext"]

            output_dir = Path(image_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            filename = (
                f"page_{page_number:03d}"
                f"_image_{image_number:02d}."
                f"{image_ext}"
            )

            image_path = output_dir / filename

            with open(image_path, "wb") as file:
                file.write(image_bytes)

            images.append({
                "image_number": image_number,
                "path": str(image_path),
                "width": image_data["width"],
                "height": image_data["height"],
                "extension": image_ext
            })

        pages.append({
            "page": page_number,
            "source": pdf_path.name,
            "text": text,
            "tables": extracted_tables,
            "images": images,
            "image_count": len(images)
        })

    document.close()

    return pages


def normalize_pages(pages):
    """
    Convert text, tables, and OCR-processed images
    into a common searchable format.
    """

    documents = []

    for page in pages:

        # -------------------------
        # TEXT
        # -------------------------

        if page["text"]:

            documents.append({
                "content": page["text"],
                "type": "text",
                "page": page["page"],
                "source": page["source"]
            })

        # -------------------------
        # TABLES
        # -------------------------

        for table in page["tables"]:

            if not table:
                continue

            headers = table[0]
            rows = table[1:]

            for row in rows:

                fields = []

                for header, value in zip(headers, row):

                    if value:
                        fields.append(
                            f"{header}: {value}"
                        )

                if fields:

                    table_content = "\n".join(fields)
                    documents.append({
                        "content": table_content,
                        "type": "table",
                        "page": page["page"],
                        "source": page["source"]
                    })

        # -------------------------
        # IMAGES + OCR
        # -------------------------

        for image in page["images"]:

            ocr_text = extract_text_from_image(
                image["path"]
            )

            if ocr_text:

                documents.append({
                    "content": ocr_text,
                    "type": "image_ocr",
                    "page": page["page"],
                    "source": page["source"],
                    "image_path": image["path"]
                })

    return documents


# import pymupdf
# from pathlib import Path


# def load_pdf(pdf_path):
#     """
#     Extract text, tables, and images from a PDF.
#     Returns page-level multimodal data.
#     """

#     pdf_path = Path(pdf_path)

#     if not pdf_path.exists():
#         raise FileNotFoundError(f"PDF not found: {pdf_path}")

#     document = pymupdf.open(pdf_path)

#     pages = []

#     for page_number, page in enumerate(document, start=1):

#         # -------------------------
#         # 1. Extract normal text
#         # -------------------------
#         text = page.get_text("text").strip()

#         # -------------------------
#         # 2. Extract tables
#         # -------------------------
#         tables = page.find_tables().tables

#         extracted_tables = []

#         for table in tables:
#             extracted_tables.append(table.extract())

#         # -------------------------
#         # 3. Detect images
#         # -------------------------
#         images = page.get_images(full=True)

#         page_data = {
#             "page": page_number,
#             "source": pdf_path.name,
#             "text": text,
#             "tables": extracted_tables,
#             "image_count": len(images)
#         }

#         pages.append(page_data)

#     document.close()

#     return pages


# def normalize_pages(pages):
#     """
#     Convert text and tables into a common searchable format.
#     """

#     documents = []

#     for page in pages:

#         # -------------------------
#         # Normalize text
#         # -------------------------
#         if page["text"]:
#             documents.append({
#                 "content": page["text"],
#                 "type": "text",
#                 "page": page["page"],
#                 "source": page["source"]
#             })

#         # -------------------------
#         # Normalize tables
#         # -------------------------
#         for table in page["tables"]:

#             if not table:
#                 continue

#             headers = table[0]
#             rows = table[1:]

#             for row in rows:

#                 fields = []

#                 for header, value in zip(headers, row):
#                     if value:
#                         fields.append(f"{header}: {value}")

#                 if fields:
#                     table_content = " | ".join(fields)

#                     documents.append({
#                         "content": table_content,
#                         "type": "table",
#                         "page": page["page"],
#                         "source": page["source"]
#                     })

#     return documents



# import pymupdf
# from pathlib import Path


# def load_pdf(pdf_path):
#     """
#     Load a PDF and extract text, tables, and image information
#     page by page.
#     """

#     pdf_path = Path(pdf_path)

#     if not pdf_path.exists():
#         raise FileNotFoundError(f"PDF not found: {pdf_path}")

#     document = pymupdf.open(pdf_path)

#     pages = []

#     for page_number, page in enumerate(document, start=1):

#         # Extract normal text
#         text = page.get_text("text").strip()

#         # Detect and extract tables
#         tables = page.find_tables().tables

#         extracted_tables = []

#         for table in tables:
#             extracted_tables.append(table.extract())

#         # Detect images
#         images = page.get_images(full=True)

#         page_data = {
#             "page": page_number,
#             "source": pdf_path.name,
#             "text": text,
#             "tables": extracted_tables,
#             "image_count": len(images)
#         }

#         pages.append(page_data)

#     document.close()

#     return pages




# import pymupdf
# from pathlib import Path


# def load_pdf(pdf_path):
#     """
#     Load a PDF and extract page-level text and image information.
#     """

#     pdf_path = Path(pdf_path)

#     if not pdf_path.exists():
#         raise FileNotFoundError(f"PDF not found: {pdf_path}")

#     document = pymupdf.open(pdf_path)

#     pages = []

#     for page_number, page in enumerate(document, start=1):

#         text = page.get_text("text").strip()
#         images = page.get_images(full=True)

#         page_data = {
#             "page": page_number,
#             "text": text,
#             "image_count": len(images),
#             "source": pdf_path.name
#         }

#         pages.append(page_data)

#     document.close()

#     return pages