#!/usr/bin/env python3

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"

REQUIRED_FIELDS = (
    "id",
    "title",
    "category",
    "status",
    "question",
    "methodology",
    "article",
    "dataset",
    "sources",
    "license",
    "findings",
    "limitations",
    "last_updated",
)

CSV_COLUMNS = (
    "sample_id",
    "collection_date",
    "parameter",
    "value",
    "unit",
    "method",
    "source_id",
)


def validate(record_id):
    record_path = (
        RESEARCH / "records" / f"{record_id}.json"
    )

    with record_path.open(encoding="utf-8") as file:
        record = json.load(file)

    missing = [
        field
        for field in REQUIRED_FIELDS
        if field not in record
    ]

    if missing:
        raise ValueError(
            f"Missing fields: {', '.join(missing)}"
        )

    if record["id"] != record_id:
        raise ValueError("Research ID mismatch")

    if record["status"] not in (
        "draft",
        "review",
        "published",
    ):
        raise ValueError("Invalid research status")

    for field in ("article", "dataset", "sources"):
        path = (
            RESEARCH / "records" / record[field]
        ).resolve()

        if not path.is_relative_to(RESEARCH.resolve()):
            raise ValueError(
                f"Invalid path for {field}"
            )

        if not path.is_file():
            raise FileNotFoundError(path)

        if field == "sources":
            with path.open(encoding="utf-8") as file:
                sources = json.load(file)

            if sources.get("research_id") != record_id:
                raise ValueError(
                    "Source registry ID mismatch"
                )

            if not isinstance(
                sources.get("sources"), list
            ):
                raise ValueError(
                    "Sources must be a list"
                )

        if field == "dataset":
            with path.open(
                encoding="utf-8",
                newline="",
            ) as file:
                reader = csv.reader(file)
                columns = next(reader, [])

            if tuple(columns) != CSV_COLUMNS:
                raise ValueError(
                    "Unexpected dataset columns"
                )

    if record["status"] == "published":
        if not record["findings"]:
            raise ValueError(
                "Published research needs findings"
            )

        if not sources["sources"]:
            raise ValueError(
                "Published research needs sources"
            )

        if record["license"] == "undetermined":
            raise ValueError(
                "Published research needs a license"
            )

    print(f"PASS: {record_id}")
    print(f"Status: {record['status']}")
    print("Structural validation complete")
    print("Scientific validity not assessed")


if __name__ == "__main__":
    record_id = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "R001"
    )

    try:
        validate(record_id)
    except (
        ValueError,
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
    ) as error:
        print(f"FAIL: {error}")
        sys.exit(1)
