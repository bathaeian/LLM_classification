import argparse
import json
import random
from pathlib import Path


def load_json(path):
    with open(path) as f:
        return json.load(f)


def export_dataset(
    input_dir,
    output_file,
    labels,
    train,
    max_points,
    count,
):

    rng = random.Random(42)
    samples = []

    class_dirs = sorted(
        [d for d in Path(input_dir).iterdir() if d.is_dir()],
        key=lambda p: int(p.name),
    )

    for alphabet in class_dirs:

        if train:
            image_numbers = range(1, 20, 2)
        else:
            image_numbers = range(2, 21, 2)

        for n in image_numbers:

            data = load_json(alphabet / f"{n}.json")

            if data["class"] not in labels:
                continue

            if (
                max_points is not None
                and len(data["points"]) > max_points
            ):
                data["points"] = rng.sample(
                    data["points"],
                    max_points,
                )
                data["num_points"] = len(data["points"])

            samples.append(data)
            if count is not None and len(samples) >= count:
                break

        if count is not None and len(samples) >= count:
            break

    output = {
        "metadata": {
            "labels": labels,
            "samples": len(samples),
            "train": train,
        },
        "samples": samples,
    }

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as f:
        json.dump(output, f, indent=2)

    print(f"Exported {len(samples)} samples")
    print(f"Saved to: {output_file}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    parser.add_argument(
        "--labels",
        nargs="+",
        required=True,
    )

    parser.add_argument("--train", action="store_true")
    parser.add_argument("--test", action="store_true")

    parser.add_argument(
    "--max-points",
    type=int,
    default=None,
)
    
    parser.add_argument(
    "--count",
    type=int,
    default=None,
    help="Maximum number of samples",
)

    args = parser.parse_args()

    export_dataset(
        input_dir=args.input,
        output_file=args.output,
        labels=args.labels,
        train=not args.test,
        max_points=args.max_points,
        count=args.count,
        
    )


if __name__ == "__main__":
    main()