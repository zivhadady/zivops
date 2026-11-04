#!/usr/bin/env python3
"""Site link and asset integrity validator.

Scans generated HTML files to verify internal hyperlinks, asset references (images,
stylesheets, scripts), and basic HTML tag balancing before deployment.
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

# Standard HTML self-closing / void elements (HTML5 spec)
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr", "!doctype",
}

IGNORED_DIRS = {".git", ".jekyll-cache", "node_modules", "vendor"}
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}


class HTMLStructureValidator(HTMLParser):
    """Checks for unclosed or mismatched HTML tags."""

    def __init__(self, filepath: Path):
        super().__init__()
        self.filepath = filepath
        self.tag_stack = []
        self.errors = []

    def handle_starttag(self, tag: str, attrs):
        tag_lower = tag.lower()
        if tag_lower not in VOID_TAGS:
            self.tag_stack.append(tag_lower)

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if tag_lower in VOID_TAGS:
            return

        if not self.tag_stack:
            self.errors.append(f"Unexpected closing tag </{tag}> in {self.filepath}")
            return

        expected = self.tag_stack.pop()
        if expected != tag_lower:
            self.errors.append(
                f"Tag mismatch in {self.filepath}: expected </{expected}>, found </{tag}>"
            )

    def finalize(self):
        if self.tag_stack:
            unclosed = ", ".join(f"<{t}>" for t in self.tag_stack)
            self.errors.append(f"Unclosed tag(s) in {self.filepath}: {unclosed}")


def extract_baseurl_from_config(config_path: Path) -> str:
    """Extracts baseurl value from _config.yml if present."""
    if not config_path.is_file():
        return ""
    try:
        content = config_path.read_text(encoding="utf-8")
        match = re.search(r"^baseurl:\s*[\"']?([^\"'\n]+)[\"']?", content, re.MULTILINE)
        if match:
            return match.group(1).strip().rstrip("/")
    except OSError:
        pass
    return ""


def validate_internal_link(target: str, root_dir: Path, source_file: Path, baseurl: str) -> bool:
    """Verifies that an internal reference resolves to an existing file."""
    parsed = urlparse(target)
    path_part = unquote(parsed.path)

    if not path_part or path_part == "/":
        return True

    # Strip configured Jekyll baseurl prefix if matching
    if baseurl and path_part.startswith(baseurl):
        path_part = path_part[len(baseurl):]

    if path_part.startswith("/"):
        candidate = root_dir / path_part.lstrip("/")
    else:
        candidate = source_file.parent / path_part

    # Check direct match, .html extension, or directory index.html
    return (
        candidate.exists()
        or candidate.with_suffix(".html").exists()
        or (candidate.is_dir() and (candidate / "index.html").exists())
    )


def validate_site(target_dir: str, baseurl_override: str = None) -> bool:
    root = Path(target_dir).resolve()
    if not root.exists():
        print(f"[ERROR] Target directory does not exist: {root}", file=sys.stderr)
        return False

    baseurl = (
        baseurl_override.rstrip("/")
        if baseurl_override is not None
        else extract_baseurl_from_config(Path("_config.yml"))
    )

    html_files = [
        path for path in root.rglob("*.html")
        if not any(part in IGNORED_DIRS for part in path.parts)
    ]

    if not html_files:
        print(f"[WARN] No HTML files found in {root}")
        return True

    has_errors = False
    link_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding="utf-8")
        except OSError as err:
            print(f"[ERROR] Failed to read {html_file}: {err}", file=sys.stderr)
            has_errors = True
            continue

        # Tag balance check
        parser = HTMLStructureValidator(html_file)
        try:
            parser.feed(content)
            parser.finalize()
            for err in parser.errors:
                print(f"[HTML ERROR] {err}", file=sys.stderr)
                has_errors = True
        except Exception as err:
            print(f"[HTML PARSE ERROR] {html_file}: {err}", file=sys.stderr)
            has_errors = True

        # Extract links, ignoring scripts and styles
        sanitized = re.sub(
            r"<(script|style)\b[^>]*>[\s\S]*?<\/\1>", "", content, flags=re.IGNORECASE
        )

        for match in link_pattern.finditer(sanitized):
            url = match.group(1).strip()

            # Skip empty, anchors, Liquid templates, and external schemes
            if not url or url.startswith(("#", "{{", "{%")):
                continue

            parsed = urlparse(url)
            if parsed.scheme.lower() in EXTERNAL_SCHEMES or url.startswith("//"):
                continue

            if not validate_internal_link(url, root, html_file, baseurl):
                print(f"[BROKEN LINK] {html_file.name} -> {url}", file=sys.stderr)
                has_errors = True

    return not has_errors


def main():
    parser = argparse.ArgumentParser(description="Validate HTML links and markup in built site.")
    parser.add_argument(
        "directory",
        nargs="?",
        default="./_site" if Path("./_site").exists() else ".",
        help="Directory containing HTML files to scan (default: ./_site or .)",
    )
    parser.add_argument(
        "--baseurl",
        default=None,
        help="Explicit baseurl prefix override (e.g. /zivops)",
    )

    args = parser.parse_args()
    success = validate_site(args.directory, args.baseurl)

    if not success:
        print("\nSite validation failed with errors.", file=sys.stderr)
        sys.exit(1)

    print("Site validation passed: all HTML markup and internal links are valid.")


if __name__ == "__main__":
    main()
