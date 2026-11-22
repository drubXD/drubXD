"""Request a plain-language explanation of a project result."""
import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


def explain(project, document, key, model):
    instructions = {
        "healthguard": "Explain the supplied educational catalog matches and their overlap measure. Do not infer likelihood, diagnose, or recommend treatment.",
        "mri-reader": "Paraphrase only the supplied radiology report in plain language. Preserve uncertainty and negation. Do not infer findings or give medical advice."
    }
    payload = {"model": model, "max_tokens": 700, "system": instructions[project],
               "messages": [{"role": "user", "content": document}]}
    request = urllib.request.Request("https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(), headers={"x-api-key": key,
        "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.load(response)
    return "\n".join(block["text"] for block in result["content"] if block["type"] == "text")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", choices=["healthguard", "mri-reader"])
    parser.add_argument("file", type=Path, help="Text you authorize sending to Anthropic")
    args = parser.parse_args()
    key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL")
    if not key or not model or key.startswith("YOUR_"):
        parser.exit(2, "Set your own ANTHROPIC_API_KEY and ANTHROPIC_MODEL first.\n")
    document = args.file.read_text(encoding="utf8").strip()
    if not 1 <= len(document) <= 24000:
        parser.error("Supply between 1 and 24000 characters.")
    try:
        print(explain(args.project, document, key, model))
    except (urllib.error.URLError, TimeoutError) as exc:
        parser.exit(1, f"Provider request failed: {exc}\n")
