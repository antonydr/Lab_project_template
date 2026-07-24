"""Wrapper around the rsync command for filesystem synchronisation."""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


class RsyncRunner:
    """Execute rsync synchronisation operations."""

    """Grab runtime config outputs."""

    def _runtime_output_settings(
        self,
        runtime_config: dict[str, Any],
    ) -> tuple[bool, bool, bool]:
        """Return runtime output settings."""

        output = runtime_config.get("output", {})

        return (
            output.get("show_progress", True),
            output.get("show_command", False),
            output.get("show_summary", True),
        )

    def _date_time_values(
        self,
        project_config: dict[str, Any],
    ) -> dict[str, str]:
        """Return formatted date and timestamp values.

        Args:
            project_config: Project configuration containing conventions.

        Returns:
            Dictionary containing formatted date and timestamp strings.
        """

        conventions = project_config.get("conventions", {})

        now = datetime.now()

        return {
            "date": now.strftime(
                conventions.get(
                    "date_format",
                    "%Y%m%d",
                )
            ),
            "timestamp": now.strftime(
                conventions.get(
                    "timestamp_format",
                    "%Y%m%d_%H%M%S",
                )
            ),
        }

    def _build_rsync_options(
        self,
        options: dict[str, Any],
        show_progress: bool,
        dry_run: bool,
    ) -> list[str]:
        """Build rsync command options.

        Args:
            options: Rsync configuration options.
            show_progress: Whether runtime allows progress output.
            dry_run: Whether this is a dry run.

        Returns:
            List of rsync command arguments.
        """

        cmd_options: list[str] = []

        #
        # Archive mode
        #

        if options.get("archive", False):
            cmd_options.append("-a")

            if options.get("preserve_owner") is False:
                cmd_options.append("--no-owner")

            if options.get("preserve_group") is False:
                cmd_options.append("--no-group")

        #
        # Simple boolean options
        #

        simple_options = {
            "verbose": "-v",
            "human_readable": "-h",
            "partial": "--partial",
            "delete_delay": "--delete-delay",
        }

        for key, flag in simple_options.items():
            if options.get(key, False):
                cmd_options.append(flag)

        #
        # Progress handling
        #

        if options.get("progress", False) and show_progress:
            cmd_options.append("--info=progress2")

        #
        # Dry run
        #

        if dry_run:
            cmd_options.append("--dry-run")

        return cmd_options

    def run(
        self,
        source: str | Path,
        destination: str | Path,
        excludes: list[str],
        options: dict[str, Any],
        dry_run: bool,
        sync_name: str,
        runtime_config: dict[str, Any],
        logging_config: dict[str, Any],
        project_config: dict[str, Any],
        show_command: bool = False,
        quiet: bool = False,
    ) -> None:
        """Run an rsync synchronisation.

        Args:
            source: Source directory.
            destination: Destination directory.
            excludes: List of exclude patterns.
            options: Dictionary of rsync option flags.
            dry_run: Whether to perform a dry run.
            sync_name: Name of the synchronisation task.
            runtime_config: Runtime configuration.
            logging_config: Logging configuration.
            project_config: Project configuration.
            show_command: Whether to display the full rsync command.
            quiet: Whether to suppress terminal output.

        Raises:
            RuntimeError: If the rsync command exits with a non-zero status.
        """

        cmd: list[str] = ["rsync"]

        #
        # Runtime configuration
        #

        show_progress, runtime_show_command, show_summary = (
            self._runtime_output_settings(runtime_config)
        )

        show_command = show_command or runtime_show_command

        #
        # Rsync options
        #

        cmd.extend(
            self._build_rsync_options(
                options,
                show_progress,
                dry_run,
            )
        )

        #
        # Logging
        #

        log_file: Path | None = None

        if logging_config.get("enabled", False) and not dry_run:
            log_dir = Path(logging_config["directory"])

            log_dir.mkdir(exist_ok=True)

            date_values = self._date_time_values(project_config)

            filename = logging_config["filename_format"]["sync"].format(
                command="sync",
                sync_name=sync_name,
                date=date_values["date"],
                timestamp=date_values["timestamp"],
            )

            log_file = log_dir / filename

            cmd.extend(["--log-file", str(log_file)])

        #
        # Exclude patterns
        #

        for pattern in excludes:
            cmd.extend(["--exclude", pattern])

        #
        # Source and destination paths
        #

        cmd.extend(
            [
                f"{source}/",
                f"{destination}/",
            ]
        )

        #
        # Terminal output
        #

        if not quiet:
            print()
            print(f"Sync: {sync_name}")
            print()
            print("Starting synchronisation ...")
            print()

        if show_command:
            print("Executing:")
            print(" ".join(cmd))
            print()

        #
        # Execute
        #

        try:
            subprocess.run(cmd, check=True)

        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                f"Synchronisation '{sync_name}' failed "
                f"(exit code {error.returncode}). "
                "See log file for details."
            ) from error

        #
        # Completion message
        #

        if not quiet and show_summary:
            print()
            print("Synchronisation complete.")

            if log_file:
                print()
                print(f"Log: {log_file}")

            print()
