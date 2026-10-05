import csv
from pathlib import Path

import pandas as pd
from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(file_path):

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text


def extract_text_from_text(file_path):
    return Path(file_path).read_text(encoding = "utf-8-sig", errors="replace")


def extract_text_from_csv(file_path):
    with open(file_path, newline="", encoding = "utf-8-sig", errors="replace") as csv_file:
        rows = csv.reader(csv_file)
        return "\n".join("\t".join(cell.strip() for cell in row) for row in rows)


def extract_text_from_excel(file_path):
    workbook = pd.ExcelFile(file_path)
    sheets = []

    for sheet_name in workbook.sheet_names:
        data = workbook.parse(sheet_name)
        sheets.append(f"Sheet: {sheet_name}\n{data.to_csv(index=False)}")

    return "\n\n".join(sheets)


def extract_resume_text(file_path):

    if file_path.lower().endswith(".pdf"):

        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):

        return extract_text_from_docx(file_path)

    elif file_path.lower().endswith((".txt", ".text")):

        return extract_text_from_text(file_path)

    elif file_path.lower().endswith(".csv"):

        return extract_text_from_csv(file_path)

    elif file_path.lower().endswith((".xlsx", ".xls")):

        return extract_text_from_excel(file_path)

    else:

        raise ValueError(
            "Unsupported file format. Please use PDF, DOCX, TXT, CSV, XLSX, or XLS."
        )