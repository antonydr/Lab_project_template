"""Synchronisation management utilities."""

from __future__ import annotations

from pathlib import Path

import yaml

from interfaces.filesystems import FilesystemManager
from interfaces.rsync import RsyncRunner


class SyncManager:
    """Manage configured synchronisation jobs."""

    CONFIG_DIR = Path("config")

    def __init__(self) -> None:
        """Load synchronisation configuration files."""

        self.transfer = self._load_config("transfer")
        self.sync = self._load_config("sync")
        self.runtime = self._load_config("runtime")
        self.logging = self._load_config("logging")
        self.project = self._load_config("project")

        self.filesystems = FilesystemManager()

    @classmethod
    def _load_config(cls, name: str) -> dict:
        """Load a YAML configuration file.

        Args:
            name: Configuration name without the ``.yaml`` extension.

        Returns:
            Parsed YAML configuration.
        """
        config_path = cls.CONFIG_DIR / f"{name}.yaml"

        with config_path.open(encoding="utf-8") as config_file:
            return yaml.safe_load(config_file)

    def runtimes(self) -> list[str]:
        """Return available runtime names.

        Returns:
            A sorted list of configured runtime names.
        """
        return sorted(self.runtime.get("runtimes", {}).keys())

    def list_filesystems(self) -> list[str]:
        """Return available synchronisation job names.

        Returns:
            A sorted list of configured synchronisation names.
        """
        return sorted(self.sync["syncs"].keys())

    def run(
        self,
        name: str,
        dry_run: bool = False,
        runtime_name: str = "interactive",
        show_command: bool = False,
        quiet: bool = False,
    ) -> None:
        """Run a configured synchronisation job.

        Args:
            name: Name of the synchronisation job.
            dry_run: Run rsync without making changes.
            runtime_name: Runtime configuration name.
            verbose: Display the generated rsync command.
            quiet: Suppress terminal output.

        Raises:
            ValueError: If the synchronisation job or runtime does not exist.
        """

        if name not in self.sync["syncs"]:
            raise ValueError(f"Unknown sync '{name}'")

        job = self.sync["syncs"][name]

        #
        # Resolve runtime configuration
        #

        runtime_config = self.runtime.get("runtimes", {}).get(runtime_name)

        if runtime_config is None:
            raise ValueError(f"Unknown runtime '{runtime_name}")

        #
        # Resolve source and destination
        #

        source = self.filesystems.path(
            job["source"]["filesystem"], job["source"].get("path")
        )

        destination = self.filesystems.path(
            job["destination"]["filesystem"], job["destination"].get("path")
        )

        #
        # Build exclusions
        #

        default_excludes = (
            self.transfer.get("transfer", {})
            .get("rsync", {})
            .get("exclude_patterns", [])
        )

        additional_excludes = job.get("options", {}).get(
            "additional_exclude_patterns", []
        )

        excludes = sorted(set(default_excludes + additional_excludes))

        #
        # Build rsync options
        #

        options = self.transfer.get("transfer", {}).get("rsync", {}).copy()

        job_options = job.get("options", {}).copy()

        job_options.pop("additional_exclude_patterns", None)

        options.update(job_options)

        RsyncRunner().run(
            source,
            destination,
            excludes,
            options,
            dry_run,
            sync_name=name,
            runtime_config=runtime_config,
            logging_config=(self.logging.get("logging", {})),
            project_config=self.project,
            show_command=show_command,
            quiet=quiet,
        )
