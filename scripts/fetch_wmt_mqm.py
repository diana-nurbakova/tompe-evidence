#!/usr/bin/env python3
"""Download the WMT 2020 MQM (newstest2020, EN-DE) annotations used by tom_validation.

The file is fetched from google/wmt-mqm-human-evaluation (Apache 2.0) at a
pinned commit and checked against the SHA-256 of the copy the committed results
were computed from. It is not redistributed in this repository.

Usage:
    python scripts/fetch_wmt_mqm.py            # download if missing, then verify
    python scripts/fetch_wmt_mqm.py --force    # re-download

Writes:
    data/wmt-mqm/mqm_newstest2020_ende.tsv
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "wmt-mqm" / "mqm_newstest2020_ende.tsv"

REPO = "google/wmt-mqm-human-evaluation"
COMMIT = "9d2d6ca92d466d507665e31417302bcc44903970"  # 2022-07-13, last change to the file
PATH = "newstest2020/ende/mqm_newstest2020_ende.tsv"
URL = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{PATH}"
SHA256 = "22acb4d5cc4dc0d8f2683e9251c179c917ae8589d71b1945d755c46d88d345e3"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="Re-download even if present")
    args = parser.parse_args()

    if args.force or not TARGET.exists():
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {URL}")
        tmp = TARGET.with_suffix(".part")
        urllib.request.urlretrieve(URL, tmp)
        tmp.replace(TARGET)

    digest = sha256(TARGET)
    if digest != SHA256:
        print(f"Checksum mismatch for {TARGET}\n  expected {SHA256}\n  got      {digest}",
              file=sys.stderr)
        return 1
    print(f"OK: {TARGET.relative_to(ROOT)} (sha256 verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
