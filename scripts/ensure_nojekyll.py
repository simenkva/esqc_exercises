#!/usr/bin/env python3
"""Restore the GitHub Pages .nojekyll marker after each Quarto render."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOJEKYLL = ROOT / "docs" / ".nojekyll"


def main() -> None:
    """Create the marker in the root of the GitHub Pages publishing tree."""
    NOJEKYLL.parent.mkdir(parents=True, exist_ok=True)
    NOJEKYLL.touch()
    print(f"Ensured {NOJEKYLL.relative_to(ROOT)} exists")


if __name__ == "__main__":
    main()
