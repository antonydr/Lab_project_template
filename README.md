# Project Name

![Last Commit](https://img.shields.io/github/last-commit/arose20/Lab_project_template_v2)
![License](https://img.shields.io/github/license/arose20/Lab_project_template_v2)

---

## ⚠️ Template Usage Note

This repository is a **template framework**.

When instantiated for a new project, the following placeholders must be replaced automatically via GitHub Actions:

- `arose20/Lab_project_template_v2` → **current repository slug**
- Workflow badge path (`main.yml`) → adjust if workflow name differs
- Any hardcoded project metadata (if added later via config injection)

This replacement is handled by:

> `.github/workflows/update-readme-badges.yml`

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

## Citation

If you use this repository, please cite:

> [Insert citation]

See `CITATION.cff` for structured formats.

---

## Contributors

Contributors can be viewed on the project's GitHub Contributors page:

https://github.com/arose20/Lab_project_template_v2/graphs/contributors

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
