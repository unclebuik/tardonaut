#!/usr/bin/env python3

"""
Tardonaut Research Publisher

Converts eligible research records into static HTML.

Requirements:
    Python 3.12
    Standard library only

Usage:
    python3 scripts/publish_research.py
"""

import html
import json
from pathlib import Path

from validate_research import validate


ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
RECORDS = RESEARCH / "records"
OUTPUT = RESEARCH / "publications"


def escape(value):
    return html.escape(str(value), quote=True)


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def render_items(items):
    if not items:
        return "<p>None documented.</p>"

    content = "\n".join(
        f"<li>{escape(item)}</li>"
        for item in items
    )

    return f"<ul>{content}</ul>"


def render_sources(sources):
    if not sources:
        return "<p>No sources listed.</p>"

    content = []

    for source in sources:
        title = escape(source.get("title", "Untitled"))
        author = escape(source.get("author", "Unknown"))
        date = escape(source.get("date", "Undated"))

        # Display URLs as text rather than injecting
        # untrusted links into generated HTML.
        url = escape(source.get("url", ""))

        content.append(
            "<li>"
            f"<strong>{title}</strong><br>"
            f"Author: {author}<br>"
            f"Date: {date}<br>"
            f"URL or DOI: {url}"
            "</li>"
        )

    return "<ul>" + "\n".join(content) + "</ul>"


def render_record(record, sources):
    record_id = escape(record["id"])
    title = escape(record["title"])
    category = escape(record["category"])
    question = escape(record["question"])
    methodology = escape(record["methodology"])
    license_name = escape(record["license"])
    updated = escape(record["last_updated"])

    findings = render_items(record["findings"])
    limitations = render_items(record["limitations"])
    references = render_sources(sources)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>{title} | Tardonaut</title>

    <style>
        body {{
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            font: 16px/1.7 Arial, sans-serif;
        }}

        nav {{
            margin-bottom: 40px;
        }}

        section {{
            margin: 35px 0;
        }}

        h1, h2 {{
            line-height: 1.3;
        }}

        a {{
            overflow-wrap: anywhere;
        }}

        li {{
            margin-bottom: 12px;
        }}

        footer {{
            margin-top: 50px;
            border-top: 1px solid #aaa;
            padding-top: 15px;
        }}
    </style>
</head>

<body>

<nav>
    <a href="index.html">Publications</a>
    |
    <a href="../index.html">Research</a>
</nav>

<main>

    <h1>{title}</h1>

    <p>
        Research ID: {record_id}<br>
        Category: {category}<br>
        Status: Published<br>
        Updated: {updated}
    </p>

    <section>
        <h2>Research question</h2>
        <p>{question}</p>
    </section>

    <section>
        <h2>Methodology</h2>
        <p>{methodology}</p>
    </section>

    <section>
        <h2>Findings</h2>
        {findings}
    </section>

    <section>
        <h2>Limitations</h2>
        {limitations}
    </section>

    <section>
        <h2>Sources</h2>
        {references}
    </section>

    <section>
        <h2>Research files</h2>

        <ul>
            <li>
                <a href="../datasets/{record_id}.csv"
                   download>
                    Download dataset (CSV)
                </a>
            </li>

            <li>
                <a href="../sources/{record_id}.json"
                   download>
                    Download source registry (JSON)
                </a>
            </li>

            <li>
                <a href="../articles/{record_id}.md"
                   download>
                    Download research article (Markdown)
                </a>
            </li>
        </ul>
    </section>

    <section>
        <h2>License</h2>
        <p>{license_name}</p>
    </section>

</main>

<footer>
    <p>
        Tardonaut Open Research
    </p>
    <p>
        Research information is publicly accessible
        without ownership of TDNT.
    </p>
</footer>

</body>
</html>
"""


def render_index(publications):
    items = []

    for record in publications:
        record_id = escape(record["id"])
        title = escape(record["title"])

        items.append(
            f'<li><a href="{record_id}.html">'
            f'{title}</a></li>'
        )

    listing = (
        "<ul>" + "\n".join(items) + "</ul>"
        if items
        else "<p>No research published yet.</p>"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>Tardonaut Research Publications</title>
</head>

<body>

    <nav>
        <a href="../index.html">Research</a>
    </nav>

    <h1>Research Publications</h1>

    <p>
        Publicly accessible research and datasets.
    </p>

    {listing}

</body>
</html>
"""


def publish():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    publications = []
    generated = set()

    for record_path in sorted(
        RECORDS.glob("*.json")
    ):
        record = load_json(record_path)
        record_id = record_path.stem

        if record.get("status") != "published":
            print(f"SKIP: {record_id} (not published)")
            continue

        # Reuse the validator created in Step 35.
        validate(record_id)

        source_path = (
            RESEARCH / "sources" / f"{record_id}.json"
        )

        source_registry = load_json(source_path)

        page = render_record(
            record,
            source_registry["sources"],
        )

        output_path = OUTPUT / f"{record_id}.html"

        output_path.write_text(
            page,
            encoding="utf-8",
        )

        publications.append(record)
        generated.add(output_path.name)

        print(f"GENERATED: {output_path.name}")

    # Remove previously generated pages that no
    # longer correspond to published records.
    for old_page in OUTPUT.glob("*.html"):
        if old_page.name == "index.html":
            continue

        if old_page.name not in generated:
            old_page.unlink()
            print(f"REMOVED: {old_page.name}")

    index_path = OUTPUT / "index.html"

    index_path.write_text(
        render_index(publications),
        encoding="utf-8",
    )

    print()
    print("Publication build complete")
    print(f"Published records: {len(publications)}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    publish()
