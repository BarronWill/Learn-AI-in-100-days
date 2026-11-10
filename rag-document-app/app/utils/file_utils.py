from pathlib import Path


def allowed_file(file_name: str) -> bool:
    """Check whether the uploaded file format is supported."""
    # TODO: accept .pdf, .txt, .docx
    return True


def save_uploaded_file(file, upload_dir: str) -> str:
    """Save an uploaded file to a local folder."""
    # TODO: create folder if not exists, save file, return saved path
    return ""
