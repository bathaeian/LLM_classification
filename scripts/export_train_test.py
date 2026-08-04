import argparse
import json
from pathlib import Path
import random


def load_json(path):
    with open(path) as f:
        return json.load(f)


def export_dataset(
    input_dir,
    output_file,
    classes,
    train=True,
    max_points=None,
):
    samples = []

    class_dirs = sorted(
        [d for d in Path(input_dir).iterdir() if d.is_dir()],
        key=lambda p: int(p.name),
    )

    selected_sets = class_dirs[:classes]

    for alphabet in selected_sets:

        if train:
            image_numbers = range(1, 20, 2)   # 1,3,5,...
        else:
            image_numbers = range(2, 21, 2)   # 2,4,6,...

        for n in image_numbers:

            file = alphabet / f"{n}.json"

            data = load_json(file)

            if (
                max_points is not None
                and len(data["points"]) > max_points
            ):
                rng = random.Random(42)

                data["points"] = rng.sample(
                    data["points"],
                    max_points,
                )

                data["num_points"] = len(data["points"])

            samples.append(data)

    output = {
        "metadata": {
            "samples": len(samples),
            "train": train,
        },
        "samples": samples,
    }

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as f:
        json.dump(output, f, indent=2)

    print(output_file)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--classes", type=int, default=20)

    parser.add_argument(
        "--train",
        action="store_true",
        help="Export odd images (train).",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Export even images (test).",
    )

    parser.add_argument(
        "--max-points",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    export_dataset(
        input_dir=args.input,
        output_file=args.output,
        classes=args.classes,
        train=not args.test,
        max_points=args.max_points,
    )


if __name__ == "__main__":
    main()