from pathlib import Path


# Anchored to this file rather than the working directory, so the app behaves the
# same whether it is launched from the project root, from an IDE, or from a shortcut.
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def project_path(*parts) -> Path:
    """Builds an absolute path from segments relative to the project root.

    :param parts: Path segments, e.g. ("data", "questions.json").
    :return: Absolute Path.
    """
    return PROJECT_ROOT.joinpath(*parts)


def as_file_url(path) -> str:
    """Converts a filesystem path into a file:// URL that Tkhtml can resolve.

    Windows paths need forward slashes and a leading slash before the drive letter
    (file:///C:/A+_StudyProgram/...), which Path.as_uri() handles correctly.

    :param path: Path or string pointing at a file or directory.
    :return: file:// URL string. Directories keep a trailing slash so they work as a base_url.
    """
    resolved = Path(path).resolve()
    url = resolved.as_uri()

    if resolved.is_dir() and not url.endswith("/"):
        url += "/"

    return url
