import os
import fitz

def merge_pdfs(file_paths: list[str], output_path: str) -> dict:
    """
    Merges multiple PDF documents into a single output PDF.

    :param file_paths: Ordered list of absolute paths to input PDF files.
    :param output_path: Destination path for the merged PDF file.
    :return: Dictionary containing execution status and result.

    """
    if not file_paths:
        raise ValueError("At least one PDF file must be provided for merging.")

    for path in file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Input file not found: {path}")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok = True)

    merged_doc = fitz.open()

    try:
        total_pages = 0
        for path in file_paths:
            with fitz.open(path) as source_doc:
                merged_doc.insert_pdf(source_doc)
                total_pages += len(source_doc)

        merged_doc.save(output_path)

        return {
            "success": True,
            "output_path": output_path,
            "file_count": len(file_paths),
            "total_pages": total_pages,
            "file_size_bytes": os.path.getsize(output_path),
        }

    finally:
        merged_doc.close()