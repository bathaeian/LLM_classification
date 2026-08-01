import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from skimage import feature, morphology


def image_to_pointcloud(
    img_array: np.ndarray,
    threshold: int = 127,
    canny_sigma: float = 1.0,
    thin_edges: bool = True,
) -> np.ndarray:
    """
    Convert a grayscale image into an Nx2 point cloud using Canny edges.
    Each point represents the (x, y) coordinate of an edge pixel.
    """
    mask = img_array < threshold

    edges = feature.canny(mask.astype(float), sigma=canny_sigma)

    if thin_edges:
        edges = morphology.thin(edges)

    y, x = np.nonzero(edges)
    return np.column_stack((x, y))


def save_pointcloud(
    points: np.ndarray,
    output_path: Path,
    label: int,
    image_name: str,
    image_shape: tuple[int, int],
) -> None:
    """
    Save a point cloud to a JSON file.
    """
    data = {
        "class": label,
        "image": image_name,
        "width": image_shape[1],
        "height": image_shape[0],
        "num_points": len(points),
        "points": points.tolist(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as f:
        json.dump(data, f, indent=2)


def process_dataset(
    input_dir: str,
    output_dir: str,
    threshold: int,
    canny_sigma: float,
    thin_edges: bool,
) -> None:
    """
    Convert every PNG image in the dataset into a point cloud.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    total_images = 0

    class_dirs = sorted(
        [d for d in input_dir.iterdir() if d.is_dir()],
        key=lambda p: int(p.name),
    )

    for class_dir in class_dirs:
        label = int(class_dir.name)

        images = sorted(
            class_dir.glob("*.png"),
            key=lambda p: int(p.stem),
        )

        print(f"Processing class {label}: {len(images)} images")

        for img_path in images:
            img_array = np.array(Image.open(img_path).convert("L"))

            points = image_to_pointcloud(
                img_array,
                threshold=threshold,
                canny_sigma=canny_sigma,
                thin_edges=thin_edges,
            )

            output_path = output_dir / str(label) / f"{img_path.stem}.json"

            save_pointcloud(
                points=points,
                output_path=output_path,
                label=label,
                image_name=img_path.name,
                image_shape=img_array.shape,
            )

            total_images += 1

    print(f"\nFinished. Converted {total_images} images.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PMF_OMNIGLOT images into point clouds."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the train dataset directory.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Directory where JSON point clouds will be saved.",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=127,
        help="Pixel threshold used for binarization (default: 127).",
    )

    parser.add_argument(
        "--canny-sigma",
        type=float,
        default=1.0,
        help="Gaussian sigma used by the Canny filter (default: 1.0).",
    )

    parser.add_argument(
        "--no-thin",
        action="store_true",
        help="Disable thinning after Canny edge detection.",
    )

    args = parser.parse_args()

    process_dataset(
        input_dir=args.input,
        output_dir=args.output,
        threshold=args.threshold,
        canny_sigma=args.canny_sigma,
        thin_edges=not args.no_thin,
    )


if __name__ == "__main__":
    main()
