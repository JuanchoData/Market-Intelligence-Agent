from pathlib import Path
from bs4 import BeautifulSoup


INPUT_PATH = Path("nvda-20260125.html")
OUTPUT_PATH = Path("data/sec/nvda_10k.txt")


def clean_local_sec_filing():
    """
    Read NVIDIA's local 10-K HTML filing
    and save cleaner human-readable text.
    """

    print("Reading local NVIDIA 10-K...")

    html = INPUT_PATH.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove elements that do not contain useful filing text
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg"
    ]):
        tag.decompose()

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    # Remove empty lines
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    clean_text = "\n".join(lines)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_PATH.write_text(
        clean_text,
        encoding="utf-8"
    )

    print(
        f"Characters extracted: {len(clean_text):,}"
    )

    print(
        f"Saved cleaned filing to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    clean_local_sec_filing()