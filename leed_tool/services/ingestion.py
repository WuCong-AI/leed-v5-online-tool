"""Safe, in-memory extraction for uploaded project documents and drawings."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, field
from io import BytesIO, StringIO
from pathlib import Path

from docx import Document
from openpyxl import load_workbook
from PIL import Image
from pypdf import PasswordType, PdfReader
from pypdf.errors import DependencyError, PyPdfError

MAX_FILE_BYTES = 30 * 1024 * 1024
MAX_TEXT_CHARS = 250_000
MAX_PDF_PAGES = 300
MAX_SHEET_ROWS = 5_000
MAX_SHEET_COLUMNS = 80

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".xlsx", ".csv", ".txt", ".md",
    ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".dxf", ".ifc", ".dwg",
}


@dataclass(frozen=True, slots=True)
class DocumentRecord:
    name: str
    extension: str
    content_type: str
    size_bytes: int
    sha256: str
    text: str
    page_count: int = 0
    kind: str = "Document"
    extraction_status: str = "Extracted"
    warnings: tuple[str, ...] = field(default_factory=tuple)


def _safe_name(name: str) -> str:
    return Path(name.replace("\x00", "")).name[:180] or "unnamed-file"


def _decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "utf-16", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _truncate(text: str, warnings: list[str]) -> str:
    clean = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if len(clean) > MAX_TEXT_CHARS:
        warnings.append(f"Extracted text was limited to {MAX_TEXT_CHARS:,} characters for online analysis.")
        return clean[:MAX_TEXT_CHARS]
    return clean


def _extract_pdf(data: bytes, warnings: list[str]) -> tuple[str, int]:
    try:
        reader = PdfReader(BytesIO(data), strict=False)
    except DependencyError as exc:
        raise ValueError(
            "Encrypted PDF support is unavailable on the server. "
            "Install pypdf[crypto] or upload an unlocked PDF."
        ) from exc
    except PyPdfError as exc:
        raise ValueError(f"PDF structure could not be read: {exc}") from exc

    if reader.is_encrypted:
        try:
            password_type = reader.decrypt("")
        except DependencyError as exc:
            raise ValueError(
                "Encrypted PDF support is unavailable on the server. "
                "Install pypdf[crypto] or upload an unlocked PDF."
            ) from exc
        except PyPdfError as exc:
            raise ValueError("Password-protected PDF cannot be analyzed; upload an unlocked copy.") from exc
        if password_type == PasswordType.NOT_DECRYPTED:
            raise ValueError("Password-protected PDF cannot be analyzed; upload an unlocked copy.")
    page_count = len(reader.pages)
    if page_count > MAX_PDF_PAGES:
        warnings.append(f"Only the first {MAX_PDF_PAGES} of {page_count} PDF pages were analyzed.")
    pages: list[str] = []
    for index, page in enumerate(reader.pages[:MAX_PDF_PAGES], start=1):
        try:
            extracted = page.extract_text() or ""
        except Exception:
            extracted = ""
            warnings.append(f"Page {index} text extraction failed.")
        if extracted.strip():
            pages.append(f"[Page {index}]\n{extracted}")
    if not pages:
        warnings.append("No searchable PDF text was found; this file likely needs OCR or visual review.")
    return "\n".join(pages), page_count


def _extract_docx(data: bytes) -> str:
    document = Document(BytesIO(data))
    blocks = [p.text for p in document.paragraphs if p.text.strip()]
    for table in document.tables:
        for row in table.rows:
            blocks.append(" | ".join(cell.text.strip() for cell in row.cells))
    return "\n".join(blocks)


def _extract_xlsx(data: bytes, warnings: list[str]) -> str:
    workbook = load_workbook(BytesIO(data), read_only=True, data_only=True)
    blocks: list[str] = []
    try:
        for sheet in workbook.worksheets:
            blocks.append(f"[Worksheet: {sheet.title}]")
            for row_index, row in enumerate(
                sheet.iter_rows(max_row=MAX_SHEET_ROWS, max_col=MAX_SHEET_COLUMNS, values_only=True),
                start=1,
            ):
                values = [str(value) for value in row if value is not None]
                if values:
                    blocks.append(" | ".join(values))
                if row_index >= MAX_SHEET_ROWS:
                    warnings.append(f"Worksheet '{sheet.title}' was limited to {MAX_SHEET_ROWS:,} rows.")
                    break
    finally:
        workbook.close()
    return "\n".join(blocks)


def _extract_csv(data: bytes) -> str:
    decoded = _decode_text(data)
    rows = csv.reader(StringIO(decoded))
    output: list[str] = []
    for index, row in enumerate(rows, start=1):
        if index > MAX_SHEET_ROWS:
            break
        output.append(" | ".join(row[:MAX_SHEET_COLUMNS]))
    return "\n".join(output)


def _inspect_image(data: bytes, name: str, warnings: list[str]) -> str:
    with Image.open(BytesIO(data)) as image:
        width, height = image.size
        image_format = image.format or "raster"
        image.verify()
    warnings.append("Raster drawing validated, but visual content requires OCR/vision review; use searchable PDF for full automated evidence extraction.")
    return f"Raster drawing file {name}. Format {image_format}. Image dimensions {width} x {height} pixels."


def extract_document(name: str, data: bytes, content_type: str = "") -> DocumentRecord:
    """Validate and extract one upload without writing it to disk."""

    safe_name = _safe_name(name)
    extension = Path(safe_name).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension or 'no extension'}")
    if not data:
        raise ValueError("The uploaded file is empty.")
    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"File exceeds the {MAX_FILE_BYTES // (1024 * 1024)} MB online limit.")

    warnings: list[str] = []
    page_count = 0
    kind = "Document"
    status = "Extracted"
    try:
        if extension == ".pdf":
            text, page_count = _extract_pdf(data, warnings)
            kind = "Drawing / PDF"
        elif extension == ".docx":
            text = _extract_docx(data)
            kind = "Specification / Narrative"
        elif extension == ".xlsx":
            text = _extract_xlsx(data, warnings)
            kind = "Calculation / Schedule"
        elif extension == ".csv":
            text = _extract_csv(data)
            kind = "Calculation / Schedule"
        elif extension in {".txt", ".md", ".dxf", ".ifc"}:
            text = _decode_text(data)
            kind = "BIM / CAD Export" if extension in {".dxf", ".ifc"} else "Narrative"
        elif extension in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            text = _inspect_image(data, safe_name, warnings)
            kind = "Raster Drawing"
            status = "Visual review required"
        else:  # DWG is intentionally accepted into the manifest but not decoded.
            text = f"Binary CAD drawing {safe_name}."
            kind = "CAD Drawing"
            status = "Conversion required"
            warnings.append("Native DWG is inventoried but not parsed; export to searchable PDF, IFC, or DXF for automated review.")
    except (ValueError, OSError, KeyError, EOFError, DependencyError, PyPdfError) as exc:
        raise ValueError(f"Could not safely parse {safe_name}: {exc}") from exc

    text = _truncate(text, warnings)
    return DocumentRecord(
        name=safe_name,
        extension=extension,
        content_type=content_type or "application/octet-stream",
        size_bytes=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
        text=text,
        page_count=page_count,
        kind=kind,
        extraction_status=status,
        warnings=tuple(dict.fromkeys(warnings)),
    )


def extract_many(files: list[tuple[str, bytes, str]]) -> tuple[list[DocumentRecord], list[str]]:
    """Extract a package while isolating failures to individual files."""

    documents: list[DocumentRecord] = []
    errors: list[str] = []
    for name, data, content_type in files:
        try:
            documents.append(extract_document(name, data, content_type))
        except ValueError as exc:
            errors.append(str(exc))
    return documents, errors
