# DataSync: HPC Data Synchronisation Tool

## Overview

DataSync provides a simple command-line interface (CLI) around `rsync` for synchronising data between:

- Persistent storage (backup / long-term storage)
- Compute workspace (active working environment)

The intended workflow is:

```text
START OF DAY

persistent_storage
        |
        | stage_in
        v
compute_storage


WORK


compute_storage
        |
        | stage_out
        v
persistent_storage
```

The CLI command is:

```bash
datasync
```

---

# Project Structure

The expected repository structure is:

```text
project/

├── config/
│   ├── defaults.yaml
│   ├── filesystems.yaml
│   ├── runtime.yaml
│   └── sync.yaml
│
├── interfaces/
│   ├── filesystem.py
│   ├── rsync.py
│   └── sync.py
│
├── scripts/
│   └── cli
|     └── cli
|       └── datasync
|         ├── datasync
|         ├── activate_datasync.sh
|         └── deactivate_datasync.sh
│
└── logs/
```

---

# Storage Configuration

## Configure storage locations

Edit:

```text
config/filesystems.yaml
```

This defines the available storage systems.

Example:

```yaml
filesystems:

  compute_storage:

    type: posix

    host: server

    path: /path/to/projects/root/folder

    description: >
      High-performance compute storage used for active analysis.
      Data may be removed by system policies.

    properties:

      compute_access: true

      backup: false



  persistent_storage:

    type: posix

    host: backup_server

    path: /path/to/projects/root/folder

    description: >
      Long-term backed-up storage containing project data,
      processed outputs and reproducible analysis states.

    properties:

      compute_access: false

      backup: true
```

The assumption given using rsync is that if required, storage locations are already mounted.

---

# Storage Design Principles

## compute_storage

Purpose:

- active working environment
- compute node access
- temporary workspace

Characteristics:

- directly accessible from compute systems
- used for active analysis
- not considered the source of truth
- can be recreated from persistent storage


Example:

```text
compute_storage

/mnt/nfs/home/<username>/Projects
```

---

## persistent_storage

Purpose:

- long-term storage
- backup location
- source of truth

Characteristics:

- retained between compute sessions
- contains important project data
- should contain final results


Example:

```text
persistent_storage

/external_server/<project>/<storage_location>
```

---

# Synchronisation Profiles

## Configure synchronisation jobs

Edit:

```text
config/sync.yaml
```

Example:

```yaml
syncs:

  stage_in:

    source:
      filesystem: persistent_storage
      path: root_folder_test

    destination:
      filesystem: compute_storage
      path: test_folder_data_sync

    options:
      # Keep any stale files on the compute storage until they are explicitly
      # replaced, avoiding unnecessary deletion work during staging.
      delete_delay: false


  stage_out:

    source:
      filesystem: compute_storage
      path: test_folder_data_sync

    destination:
      filesystem: persistent_storage
      path: root_folder_test

    options:
      # Delay deletions until the transfer has completed to minimise the risk
      # of leaving the persistent storage in a partially synchronised state.
      delete_delay: true

      # Exclude transient working data that should not be persisted.
      additional_exclude_patterns:
        - "test_work_area/"
```

---

# Sync Definitions

## stage_in

Direction:

```text
persistent_storage
        |
        v
compute_storage
```

Purpose:

- start a compute session
- retrieve previous work
- prepare workspace

Recommended first:
```bash
datasync sync stage_in --dry-run
```

Execute:

```bash
datasync sync stage_in
```

---

## stage_out

Direction:

```text
compute_storage
        |
        v
persistent_storage
```

Purpose:

- save results
- update persistent storage
- finish compute session

Recommended first:
```bash
datasync sync stage_out --dry-run
```

Execute:

```bash
datasync sync stage_out
```

---

# Runtime Configuration

## Configure default rsync behaviour

Edit:

```text
config/transfer.yaml
```

Example:

```yaml
transfer:

  engine: rsync


  rsync:
    archive: true
    preserve_owner: false
    preserve_group: false
    verbose: false
    human_readable: true
    progress: true
    partial: true
    delete_delay: true

    exclude_patterns:

    # Housekeeping
      - .git/
      - .venv/
      - __pycache__/
      - .pytest_cache/
      - .ruff_cache/
      - "*.pyc"
      - "*.tmp"
      - "*.log"

    # Folder structures
      - data/raw/
      - logs/
      - exploratory/

```

---

## Configure execution environments

Edit:

```text
config/runtime.yaml
```

Example:

```yaml
runtimes:

  interactive:

    type: terminal
    output:
      show_command: false
      show_progress: true
      verbose: false

  debug:
    type: terminal
    output:
      show_command: true
      show_progress: true
      verbose: true

  batch:
    type: scheduler
    output:
      show_command: false
      show_progress: false
      verbose: false
```

---

# Logging

Logs for datasync are generated automatically during real synchronisation runs (i.e. not `--dry-run`) so there is no need to manually curate them.

They currently follow the format `{command}_{sync_name}_{timestamp}.log`

Example:

```text
logs/

├── sync_stage_in_20260723_081530.log
└── sync_stage_out_20260723_174512.log
```

Logs:

- are created locally and stored in `./logs`
- are not synchronised
- provide an audit trail
- contain rsync transfer information

---

# File Permissions

## Make scripts executable

In order to use the datasync CLI, the scripts and CLI permissions need to be updated by the user.

Run:

```bash
chmod +x scripts/cli/datasync/datasync

chmod +x scripts/cli/datasync/activate_datasync.sh

chmod +x scripts/cli/datasync/deactivate_datasync.sh
```

---

# Activate DataSync CLI

## 6. Activate environment

The datasync command won't automatically be running so a manual start is required.

From the project root:

```bash
source scripts/cli/datasync/activate_datasync.sh
```

Expected output:

```text
datasync activated
Run: datasync --help
```

The activation:

- only affects the current terminal session
- does not modify `.bashrc`
- does not require administrator privileges
- hides the project path from the terminal prompt

---

# Verify Installation

Check the executable:

```bash
which datasync
```

Expected:

```text
.../scripts/datasync
```

Show available commands:

```bash
datasync --help
```

List configured filesystems:

```bash
datasync filesystems
```

List configured synchronisation jobs:

```bash
datasync sync --list
```

Example:

```text
stage_in
stage_out
```

---

# Daily Workflow

## Start of Day

Activate datasync CLI:

```bash
source scripts/cli/datasync/activate_datasync.sh
```

Review proposed changes:

```bash
datasync sync stage_in --dry-run
```

Synchronise data:

```bash
datasync sync stage_in
```

Data movement:

```text
persistent_storage
        |
        | stage_in
        v
compute_storage
```

---

# During Work

Perform normal compute tasks:

Examples:
```text
- analysis
- pipelines
- experiments
- simulations
```

The compute workspace should be considered your active working environment.

---

# End of Day

Review proposed changes:

```bash
datasync sync stage_out --dry-run
```

Confirm:

- files to be transferred
- files to be deleted
- exclusions
- destination

Then execute:

```bash
datasync sync stage_out
```

Data movement:

```text
compute_storage
        |
        | stage_out
        v
persistent_storage
```

---

# Command Line Options

## Dry Run

Preview a synchronisation without modifying any files (highly recommended):

```bash
datasync sync stage_out --dry-run
```

Dry-run:

- shows planned changes
- does not transfer files
- does not delete files
- creates no log file

---

## Verbose Mode

Display the complete rsync command.

Useful for debugging.

```bash
datasync sync stage_out --verbose
```

---

## Quiet Mode

Suppress datasync status message while still allowing rsync progress to be displayed.

```bash
datasync sync stage_out --quiet
```

Useful for long-running synchronisations.

---

## Runtime

Specify the execution environment.

Example:
```bash
datasync sync stage_out --runtime interactive
```

---

# Delete Behaviour

Some synchronisation jobs enable:

```text
--delete-delay
```

Currently this is set by default for `stage_out`

This means:

- destination mirrors source
- files removed from the source may also be removed from destination

Always review changes first:

```bash
datasync sync stage_out --dry-run
```

before executing:

```bash
datasync sync stage_out
```

---

# Exclusions

The following are excluded from synchronisation by default:

```text
.git/
__pycache__/
*.pyc
*.tmp
*.log
logs/
```

Reason:

| Pattern | Reason |
|---|---|
| `.git/` | Git metadata |
| `__pycache__/` | Python cache |
| `*.pyc` | Compiled Python files |
| `*.tmp` | Temporary files |
| `*.log` | Log files |
| `logs/` | Runtime logs |


Global exclusions should be put in `transfer.yaml` whereas if it is job-specific exclusions, this should be added to the `sync.yaml`.

---

# Useful Commands

## Help

```bash
datasync --help
```

---

## List available sync profiles

```bash
datasync sync --list
```

Example:

```text
stage_in
stage_out
```

---

## Dry Run

```bash
datasync sync stage_out --dry-run
```

---

## Run Sync

```bash
datasync sync stage_out
```

---

# Logs

List logs:

```bash
ls -ltr logs/
```

View a log:

```bash
less logs/<log_file>
```

Example:

```bash
less logs/stage_out_20260723_174512.log
```

---

# Deactivate

When finished you may wish to deactivate the CLI so it isn't accidentially used.

To deactivte the datasync CLI:

```bash
source scripts/cli/datasync/deactivate_datasync.sh
```

Expected output:

```text
datasync deactivated
```

---

# Troubleshooting

## Command not found

If:

```text
datasync: command not found
```

run:

```bash
source scripts/cli/datasync/activate_datasync.sh
```

---

## Check storage paths

Review:

```text
config/filesystems.yaml
```

Confirm:

- filesystem is mounted
- path exists
- permissions are correct

---

## Check configured synchronisation jobs

```bash
datasync sync --list
```

---

## Check synchronisation command

Run:

```bash
datasync sync stage_out --dry-run
```

Confirm:

- source path
- destination path
- exclusions
- delete behaviour

---

# Recommended Workflow Summary

## Morning

```bash
source scripts/cli/datasync/activate_datasync.sh

datasync sync stage_in --dry-run

datasync sync stage_in
```

---

## Work

```text
Perform compute work
```

---

## Evening

```bash
datasync sync stage_out --dry-run

datasync sync stage_out
```

---

## Finish

```bash
source scripts/cli/datasync/deactivate_datasync.sh
```
