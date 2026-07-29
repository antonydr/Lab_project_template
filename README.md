# Project Name

![Last Commit](https://img.shields.io/github/last-commit/arose20/Lab_project_template_v2)
![License](https://img.shields.io/github/license/arose20/Lab_project_template_v2)

---

## 👋 Getting started

This repository is a **template framework**.

When utalising for a new project, it is suggested you take time to perform the following:

- Update this README.md file for content appropriate for your project
- Decide on how to and also curate a contributing guide
    - This should include things like branch usage, forking, pre-commands, custom structures and workflows
- Suggested: create a environment from `/envs/environment-dev.yml`

#### **environment-dev creation**

Most environment curations can be used to curate an environment to install pre-commit and other packages for project management/maintenance. 

As there is already an `/envs/environment-dev.yml`, creating an environment from this will keep your local environment and the environment GitHub actions will use in sync. 

To curate an environment from the yml file, some suggestions include:

- **conda** / **miniconda** (Ensure you use community channels like `conda-forge`. Standard installations pull from Anaconda's proprietary `defaults` channel, which requires a paid commercial license for organisations with 200+ employees).
- **mamba** / **micromamba** (Recommended. Faster, open-source alternatives that use community channels out of the box and bypass commercial licensing restrictions).

If working on a High-Performance Computing (HPC) cluster, administrators will have strict rules around Conda tools to avoid these licensing liabilities. Most HPC sites explicitly block or ban standard Anaconda installations.

To make compliance simple, HPCs usually provide pre-installed software modules that are pre-configured to strictly use free, open-source package repositories (like `conda-forge`).

##### **Using HPC Pre-Set Modules**

Instead of installing your own Conda distribution on the cluster, you should load the system's pre-configured toolset. For example, loading a module named **Miniforge** already configured on a HPC to automatically give you access to license-compliant versions of both `conda` and `mamba`:

```bash
# Load the pre-configured, cluster-safe Miniforge module
module load Miniforge

# Create your environment securely from the project file
mamba env create -f /envs/environment-dev.yml
```

#### **pre-commit**
This repository already contains a `.pre-commit-config.yaml` file so that actions are performed when trying to commit a file.

To use this, activate a environment with the pre-commit package is installed and then run `git commit` command within this activated environment. This is included in the `/envs/environment-dev.yml`.

By default, the `.pre-commit-config.yaml` is set to run linting of files trying to commit to help ensure clean code quality.

Note: **make sure to run** `pre-commit install` inside the activated environment to ensure it will run when commiting files since it will then add the git hook.

---

## Overview

This project applies a modular, reproducible computational framework to investigate [INSERT PROJECT GOAL HERE].

It is designed for scalable scientific computing across domains, supporting structured data processing, modelling, and reproducible workflows.

For system design, repository architecture, and execution principles, see:

> **[docs/architecture.md](./docs/architecture.md)**

---

## Scientific Objective

Brief description of the specific scientific or computational objective.

This may include:
- system or process being analysed
- hypotheses or computational tasks
- expected outputs or models

---

## Data Availability

### Input Data

- Primary datasets: [...]
- External datasets: [...]
- Reference datasets: [...]

### Access

- Local/HPC paths: [...]
- Cloud storage: [...]
- Public repositories: [...]

---

## Outputs

All outputs are fully reproducible and stored in `results/`:

- `results/figures/` → visual outputs
- `results/tables/` → structured results
- `results/models/` → trained or fitted models
- `results/embeddings/` → latent representations
- `results/reports/` → generated summaries
- `results/exports/` → external data formats

---

## Reproducibility

A result is reproducible if it can be regenerated from:

- `config/`
- `envs/`
- `data/`
- `src/`
- `workflows/`

No outputs are manually edited.

---

## Repository Structure

Full system design and architecture is documented in:

> **[docs/architecture.md](./docs/architecture.md)**

---

## Getting Started

### Setup environment

```bash
conda env create -f envs/environment.yaml
conda activate project_env
```

---

### Run workflows

```bash
nextflow run workflows/main.nf -params-file config/config.yaml
```

or

```bash
snakemake --configfile config/config.yaml
```

---

### Explore outputs

- notebooks: `notebooks/`
- reports: `results/reports/`
- exports: `results/exports/`

---

## Documentation

- System architecture: `docs/architecture.md`
- Data synchronisation: `docs/datasync_cli.md`
- Study design: `docs/study_overview.md`
- Workflow guide: `docs/analysis_overview.md`
- Contribution guide: `CONTRIBUTING.md`

---

## Staging files

This repository includes a controlled file staging script for large scientific projects.

It provides safe, reproducible staging of files before committing, with size limits, gitignore awareness, and optional preview mode.

**Important to note:** you should still know what you are trying to add to github so this should be used responsibly where appropriate

### Script location

```bash
scripts/git/stage_files.sh
```

### Setup (first time only)

Ensure the script is executable:
```bash
chmod +x scripts/git/stage_files.sh
```

### Usage

**Full repository staging (default)**
```bash
bash scripts/git/stage_files.sh
```

**Dry run (preview only)**
No files are staged; output is shown.
```bash
bash scripts/git/stage_files.sh --dry-run
```

**Specific directory**
You can restrict staging to a subdirectory using `DIR`
```bash
DIR=src bash scripts/git/stage_files.sh
```
```bash
DIR=notebooks bash scripts/git/stage_files.sh
```
```bash
DIR=scripts bash scripts/git/stage_files.sh
```

**Dry run for a specific directory**
```bash
DIR=src bash scripts/git/stage_files.sh --dry-run
```

**What this script does**
- Scans files inside the selected directory (`DIR`)
- Respects `.gitignore`
- Skips files larger than configured threshold (`config/git.yaml`)
- Stages valid files using `git add`
- Safely stages deletions using `git add -u`
- Writes skipped-file logs locally in `logs/git/`

---

## Data syncing through custom CLI

This repository has a custom CLI to utalise rsync for synchronising data between different locations e.g. a compute storage and backup storage.

This is useful for the following scenarios:

- Your compute resource storage isn't backed up (e.g. scratch)
- Your backup storgae is a mounted drive
- Your backup storage can't be accessed by a compute cluster

For more information on how to use the custom CLI `datasync`, this is documented in:

> **[docs/datasync_cli.md](./docs/datasync_cli.md)**

---

## Citation

If you use this repository, please cite:

> [Insert citation]

See `CITATION.cff` for structured formats.

---

## Contributors

Contributors can be viewed on the project's GitHub Contributors page:

https://github.com/antonydr/Lab_project_template/graphs/contributors

---

## Contribution Tracking

This repository currently uses GitHub-based contributor tracking.

### Recommended upgrade

For richer attribution (code, ideas, design, analysis contributions), it is recommended to adopt:

> https://allcontributors.org/en/

This allows:
- categorised contributions (code, docs, ideas, data, review, etc.)
- explicit acknowledgment beyond commits
- better suitability for scientific collaboration
