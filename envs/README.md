# Folder to store environments used
# Environments

This directory contains the files used to define and reproduce the project's software environments. These definitions are used for local development, continuous integration (GitHub Actions), and containerised execution.

## Directory Structure

```text
envs/
├── environment-dev.yml      # Default Conda environment
└── containers/
    └── sc_basic.def         # Example container definition
```

## Conda Environments

The primary environment for this project is:

- **`environment-dev.yml`** – The default development environment.

This environment is the canonical source of the project's software dependencies and is used for:

- Local development.
- GitHub Actions CI workflows.
- Building reproducible execution environments.

### Creating the environment

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
mamba env create -f ./envs/environment-dev.yml -c conda-forge
```

## Container Definitions

The `containers/` directory contains container definition files for building portable execution environments.

Example:

- **`sc_basic.def`** – A basic Apptainer/Singularity definition file that demonstrates how to package the project environment for reproducible execution.

Container definitions are useful for:

- Running on HPC systems.
- Sharing reproducible computational environments.
- Ensuring consistent software stacks across platforms.

## Adding New Environments

If additional environments are needed (for example GPU-enabled, documentation, or release-specific environments), add them alongside `environment-dev.yml` using descriptive names such as:

- `environment-gpu.yml`
- `environment-docs.yml`
- `environment-minimal.yml`

Where possible:

- Keep `environment-dev.yml` as the primary development environment.
- Avoid unnecessary duplication between environment files.
- Keep container definitions aligned with their corresponding Conda environments.

## Best Practices

- Update `environment-dev.yml` whenever project dependencies change.
- Keep dependency versions pinned where reproducibility is important.
- Test environment changes locally before merging.
- Ensure container definitions remain consistent with the environments they package.
