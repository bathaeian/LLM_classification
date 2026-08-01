import argparse
import json
from pathlib import Path


def load_dataset(dataset_path: Path) -> dict:
    with dataset_path.open() as f:
        return json.load(f)


def load_template(template_path: Path) -> str:
    return template_path.read_text()


def format_dataset(dataset: dict) -> str:
    """
    Convert dataset JSON into a compact text representation.
    """

    lines = []

    for i, sample in enumerate(dataset["samples"], start=1):
        lines.append(f"Sample {i}")
        lines.append(f"Class: {sample['class']}")
        lines.append(f"Image size: {sample['width']}x{sample['height']}")
        lines.append(f"Number of points: {sample['num_points']}")
        lines.append("Points:")

        point_str = " ".join(f"({x},{y})" for x, y in sample["points"])

        lines.append(point_str)
        lines.append("")

    return "\n".join(lines)


def build_prompt(template: str, dataset_text: str) -> str:
    return template.replace("{{DATASET}}", dataset_text)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    dataset = load_dataset(Path(args.dataset))

    template = load_template(Path(args.template))

    dataset_text = format_dataset(dataset)

    prompt = build_prompt(template, dataset_text)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(prompt)

    print(f"Prompt saved to {output_path}")
    print(f"Characters: {len(prompt):,}")
    print(f"Words: {len(prompt.split()):,}")


if __name__ == "__main__":
    main()
