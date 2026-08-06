import argparse
import json
import random
from pathlib import Path


def load_pointcloud(json_path: Path) -> dict:
    """Load a point cloud JSON file."""

    with json_path.open("r") as f:
        return json.load(f)


def sample_points(points: list, max_points: int | None, rng: random.Random) -> list:
    """
    Optionally reduce the number of points.

    If max_points is None or larger than the point cloud,
    the original point cloud is returned.
    """

    if max_points is None:
        return points

    if len(points) <= max_points:
        return points

    return rng.sample(points, max_points)


def export_dataset(
    input_dir: Path,
    output_file: Path,
    num_classes: int,
    samples_per_class: int,
    max_points: int | None,
    shuffle: bool,
    seed: int,
) -> None:

    rng = random.Random(seed)

    samples = []

    label = int(input_dir.name)

    json_files = sorted(
        input_dir.glob("*.json"),
        key=lambda p: int(p.stem),
    )

    for json_file in json_files:
        data = load_pointcloud(json_file)
        data["num_points"] = len(data["points"])
        samples.append(data)

    if shuffle:
        rng.shuffle(samples)

    output = {
        "metadata": {
            "num_classes": num_classes,
            "samples_per_class": samples_per_class,
            "total_samples": len(samples),
            "max_points": max_points,
            "shuffle": shuffle,
            "seed": seed,
        },
        "samples": samples,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as f:
        json.dump(output, f, indent=2)

    print(f"Exported {len(samples)} samples")
    print(f"Saved to: {output_file}")


def main():

    parser = argparse.ArgumentParser(
        description="Export subsets of the point-cloud dataset."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Point cloud directory.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON file.",
    )

    parser.add_argument(
        "--classes",
        type=int,
        default=10,
        help="Number of classes to export.",
    )

    parser.add_argument(
        "--samples-per-class",
        type=int,
        default=2,
        help="Samples per class.",
    )

    parser.add_argument(
        "--max-points",
        type=int,
        default=None,
        help="Maximum number of points per sample.",
    )

    parser.add_argument(
        "--shuffle",
        action="store_true",
        help="Shuffle exported samples.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed.",
    )

    args = parser.parse_args()

    export_dataset(
        input_dir=Path(args.input),
        output_file=Path(args.output),
        num_classes=args.classes,
        samples_per_class=args.samples_per_class,
        max_points=args.max_points,
        shuffle=args.shuffle,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()