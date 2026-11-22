"""Explore symptom overlap in an editable teaching catalog."""
import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).with_name("catalog.json")


def rank(symptoms, catalog):
    selected = {term.strip().casefold() for term in symptoms if term.strip()}
    results = []
    for condition, terms in catalog.items():
        features = set(terms)
        matches = sorted(selected & features)
        if matches:
            overlap = len(matches) / len(selected | features)
            results.append((overlap, condition, matches))
    return sorted(results, key=lambda row: (-row[0], row[1]))[:3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symptoms", nargs="*", help="One quoted symptom per argument")
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf8"))
    if not args.symptoms:
        print("Available terms:", ", ".join(sorted({s for terms in catalog.values() for s in terms})))
        return
    results = rank(args.symptoms, catalog)
    print("Educational catalog matches. Scores measure term overlap only.")
    for score, name, terms in results:
        print(f"{name} | {score:.2f} | {', '.join(terms)}")
    if not results:
        print("No matching catalog terms.")


if __name__ == "__main__":
    main()
