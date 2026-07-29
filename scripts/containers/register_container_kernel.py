#!/usr/bin/env python3

"""
Register Apptainer containers as Jupyter kernels.

Usage:
    python register_container_kernel.py /path/to/container.yaml

Example:
    python register_container_kernel.py \
        /path/to/container/yamls/sc_basic.yaml
"""

import argparse
import json
from pathlib import Path

import yaml

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

HOME = Path.home()

JUPYTER_KERNEL_DIR = HOME / ".local" / "share" / "jupyter" / "kernels"

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LAUNCHER = (
    PROJECT_ROOT / "scripts" / "containers" / "apptainer_kernel_launcher.sh"
).resolve()


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def check_file(path, description):
    """
    Check a file exists.
    """
    if not path.exists():
        raise FileNotFoundError(f"{description} not found:\n{path}")


def write_kernel_spec(kernel_name, display_name, language, image, executable, metadata):
    """
    Create Jupyter kernel.json
    """

    kernel_dir = JUPYTER_KERNEL_DIR / kernel_name

    kernel_dir.mkdir(parents=True, exist_ok=True)

    kernel_json = {
        "display_name": display_name,
        "language": language,
        "argv": [str(LAUNCHER), str(image), executable, "{connection_file}"],
        "metadata": metadata,
    }

    kernel_file = kernel_dir / "kernel.json"

    with open(kernel_file, "w") as f:
        json.dump(kernel_json, f, indent=4)

    print("Registered kernel:")
    print(f"  Name: {kernel_name}")
    print(f"  Display: {display_name}")
    print(f"  Location: {kernel_file}")
    print()


# ------------------------------------------------------------
# Main registration
# ------------------------------------------------------------


def register_container(yaml_file):

    yaml_file = Path(yaml_file).expanduser().resolve()

    check_file(yaml_file, "Container YAML")

    with open(yaml_file) as f:
        config = yaml.safe_load(f)

    # Validate container type

    if config.get("type") != "apptainer":

        raise ValueError("Only type: apptainer is supported")

    # Resolve image path

    image = Path(config["image"]).expanduser().resolve()

    check_file(image, "Apptainer image")

    check_file(LAUNCHER, "Apptainer kernel launcher")

    metadata = {
        "container": config.get("name"),
        "version": config.get("version"),
        "image": str(image),
        "definition": config.get("created", {}).get("definition"),
        "resources": config.get("resources", {}),
        "packages": config.get("packages", {}),
    }

    # --------------------------------------------------------
    # Python kernel
    # --------------------------------------------------------

    if "python" in config:

        python = config["python"]

        write_kernel_spec(
            kernel_name=python["kernel_name"],
            display_name=python["display_name"],
            language="python",
            image=image,
            executable=python.get("executable", "python"),
            metadata=metadata,
        )

    # --------------------------------------------------------
    # R kernel
    # --------------------------------------------------------

    if "r" in config:

        r = config["r"]

        write_kernel_spec(
            kernel_name=r["kernel_name"],
            display_name=r["display_name"],
            language="R",
            image=image,
            executable="R",
            metadata=metadata,
        )


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------


def main():

    parser = argparse.ArgumentParser(description="Register Apptainer Jupyter kernels")

    parser.add_argument("yaml", help="Container registry YAML file")

    args = parser.parse_args()

    register_container(args.yaml)


if __name__ == "__main__":
    main()
