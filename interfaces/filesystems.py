"""Filesystem management utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

FILESYSTEM_CONFIG = Path("config/filesystems.yaml")


class FilesystemManager:
    """Manage filesystem locations defined in the application configuration."""

    def __init__(self) -> None:
        """Load the filesystem configuration from disk."""
        with open(FILESYSTEM_CONFIG) as config_file:
            self.config: dict[str, Any] = yaml.safe_load(config_file)

    @property
    def filesystems(self) -> dict[str, Any]:
        """Return the configured filesystems.

        Returns:
            A dictionary containing the configured filesystems indexed by name.
        """
        return self.config["filesystems"]

    def list_filesystems(self) -> list[str]:
        """Return the configured filesystem names.

        Returns:
            A sorted list of configured filesystem names.
        """
        return sorted(self.filesystems.keys())

    def path(
        self,
        name: str,
        subpath: str | Path | None = None,
    ) -> Path:
        """Return the path for a configured filesystem.

        Args:
            name: The name of the configured filesystem.
            subpath: An optional path relative to the filesystem root.

        Returns:
            The resolved filesystem path.

        Raises:
            ValueError: If the filesystem is not configured.
        """
        if name not in self.filesystems:
            raise ValueError(f"Unknown filesystem '{name}'")

        base = Path(self.filesystems[name]["path"])

        if subpath:
            return base / subpath

        return base
