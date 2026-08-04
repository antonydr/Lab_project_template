# Building and Registering Apptainer Containers for VS Code and Jupyter

This guide documents a workflow for building reproducible Apptainer containers for bioinformatics analyses (Python and/or R), testing them, and registering them as Jupyter kernels that can be used from both Jupyter and Visual Studio Code.

Although in the examples below there are packages related to Scanpy/SpatialData environment, the same workflow applies to any containerised Python or R environment.

Note: in future will also show container building for docker.

---

# Overview

The overall workflow is:

1. Build an Apptainer sandbox from a definition file
2. Test the environment interactively
3. Build the final immutable SIF image
4. Register the container as one or more Jupyter kernels
5. Use the registered kernels from VS Code or Jupyter

## Table of Contents

| Section | Description |
|---------|-------------|
| [Overview](#overview) | Summary of the workflow for building Apptainer containers and registering them as Jupyter kernels. |
| [Prerequisites](#prerequisites) | Required HPC setup including Apptainer modules, temporary build storage, and Jupyter environment requirements. |
| [Project Layout](#project-layout) | Recommended organisation of definition files, sandbox builds, SIF images, registry files, and scripts. |
| [Step 1 — Write an Apptainer Definition File](#step-1--write-an-apptainer-definition-file) | Creating the container definition file containing the operating system, software environment, packages, and kernels. |
| [Step 2 — Build a Sandbox](#step-2--build-a-sandbox) | Creating a writable development environment for testing before producing the final image. |
| [Step 3 — Test the Environment](#step-3--test-the-environment) | Testing installed Python/R packages and verifying the container environment works correctly. |
| [Step 4 — Build the Final SIF](#step-4--build-the-final-sif) | Building the immutable Apptainer image used for long-term deployment. |
| [Step 5 — Create a Container Registry File](#step-5--create-a-container-registry-file) | Defining YAML metadata used to describe the container and kernel configuration. |
| [Step 6 — Kernel Launcher](#step-6--kernel-launcher) | Creating the wrapper script that launches Jupyter kernels inside Apptainer. |
| [Step 7 — Configure Jupyter Runtime Directory](#step-7--configure-jupyter-runtime-directory) | Ensuring Jupyter runtime paths are consistent for VS Code communication. |
| [Step 8 — Register the Container](#step-8--register-the-container) | Registering the Apptainer image as a Jupyter kernel using the YAML registry. |
| [Step 9 — Using the Container in VS Code](#step-9--using-the-container-in-vs-code) | Selecting and launching registered container kernels from VS Code notebooks. |
| [Step 10 — Extracting package information for traceability](#step_10--extracting-package-information-for-traceability) | Export detailed package information for the environment in the container. |
| [Troubleshooting](#troubleshooting) | Diagnosing common kernel startup, runtime directory, and container execution issues. |
| [Best Practices](#best-practices) | Recommendations for reproducible builds, version control, and maintaining containers. |
| [Files Included](#files-included) | Summary of scripts and configuration files required for the workflow. |
| [Appendix](#appendix) | Full example files for definition, YAML registry, launcher, and registration scripts. |

---

# Prerequisites

Sometimes there are restrictions on where apptainer can build containers. Check prior to ensure you are building the container in a area this is allowed. For some HPCs, they have dedicated areas for building or it is restricted to login nodes and not available on compute nodes. Therefore:

- Build containers **where allowed to**
- Load the Apptainer module
- Set a temporary directory. e.g. below:

```bash
export APPTAINER_TMPDIR=/scratch/
```

The temporary build directory is highly advised and on some systems required to point to a specific area such as `/scratch` area. This is because container builds require substantially more temporary storage than is available under classical `/tmp` areas.

Load Apptainer:

```bash
module load apptainer
```

or, if you need a specific version:

```bash
module load apptainer/1.4.1
```

This work assumes apptainer has been installed prior, most likely as a module.

As we are working with Jupyter, this workflow assumes you are also working in a virtual environment (e.g. `venv`) with `Jupyter` installed so can manage kernels. This is needed when registering kernels.

---

# Project Layout

A simple directory structure is recommended.

```text
containers/
├── def/
│   └── sc_basic.def
├── sandbox/
├── sif/
├── registry/
│   └── scanpy_basic.yaml
└── scripts/
    ├── apptainer_kernel_launcher.sh
    └── register_container_kernel.py
```

If you plan to use these containers across projects, it is recommended to have the containers themselves in a designated area outside the project directory, a copy backed up elsewhere and to have a copy of the definition file `.def` kept with the project.

For this template, the following structure is assumed:

```text
containers/
├── sandbox/
├── sifs/
└── defs/

...

project/
├── config/
│   ├── containers.yaml
│   └── kernels/
|
├── envs/
│   └── containers/
|
└── scripts/
│   └── containers/
│       ├── apptainer_kernel_launcher.sh
│       ├── build_container.sh
│       ├── extract_container_provenance.sh
│       └── register_container_kernel.py
```

A containers directory should exist outside your project directory and this should be where:

- sandbox experiments are done
- final `.sif` images are stored
- a copy of `.def` files are stored

---

# Step 1 — Write an Apptainer Definition File

Container contents are defined in a `.def` file.

For example:

```text
sc_basic.def
```

The definition file should install:

- languages required (e.g. Python, R)
- required packages for the languages installed
- kernel(s)

For Jupyter integration it is important that the image installs

```
ipykernel
```

and, if R is included,

```
IRkernel
```

The `%post` section should also install the kernelspecs inside the container. Examples:

Python:

```bash
python -m ipykernel install \
    --name sc_basic \
    --display-name "Python (sc_basic)" \
    --prefix=/usr/local
```

R:

```r
IRkernel::installspec(
    name="sc_basic-r",
    displayname="R (sc_basic)",
    prefix="/usr/local"
)
```

---

# Step 2 — Build a Sandbox

Develop inside a writable sandbox before producing the final image. Replace below with paths to the desired sandbox and definition file locations.

```bash
apptainer build \
    --sandbox \
    sandbox/sc_basic \
    def/scanpy_basic.def
```

Using a sandbox allows packages to be tested and modified without repeatedly rebuilding the entire image.

---

# Step 3 — Test the Environment

Launch a shell inside the sandbox.

```bash
apptainer shell sandbox/sc_basic
```

Verify that Python and R packages import correctly. Remeber to launch python and/or R first:

Python:

```python
import scanpy
import squidpy
import spatialdata
```

R:

```r
library(Seurat)
library(IRkernel)
```

Confirm that both environments and required packages work before building the final image.

---

# Step 4 — Build the Final SIF

Once testing is complete, build an immutable SIF post updating the `.def` file with any required changes. Again, update paths as required.

```bash
apptainer build \
    sif/sc_basic.sif \
    def/sc_basic.def
```

The SIF image is the version intended for long-term use.


### Alternatively

To aid in construction, a `build_container.sh` script is provided in `/scripts/containers/`.

This can help run the apptainer commands for building the `.sif` image ensuring the `.yaml` and `.def` files are present and correctly formatted. 

Constructing the `.yaml` is covered in step 5 but if this is constructed prior to building the `.sif` then the below command can be run instead:

```bash
./scripts/containers/build_container.sh sc_basic
```

This shell script assumes you have a `.def` and `.yaml` with matching names. 

Note: it will use the same name throughout so if want a different name for `.yaml`, `.def` or `.sif` perform steps manually.

---

# Step 5 — Create a Container Registry File

Each container is described using a small YAML file.

Example:

```yaml
name: sc_basic

version: 1.0

image: /absolute/path/to/user/containers/sif/sc_basic.sif

type: apptainer

language:
  - python
  - r

python:
  executable: python
  kernel_name: sc_basic
  display_name: "Python (sc_basic 1.0)"

r:
  kernel_name: sc_basic-r
  display_name: "R (sc_basic 1.0)"
```

This provides metadata describing:

- image location
- kernel names
- display names
- language support
- available packages
- version information

---

# Step 6 — Kernel Launcher

VS Code cannot directly launch an Apptainer container as a Python or R interpreter.

Instead, the kernelspec launches a small wrapper script.

Example:

```bash
#!/bin/bash
set -euo pipefail

source /etc/profile.d/modules.sh
module load apptainer/1.4.1

IMAGE="$1"
EXECUTABLE="$2"
CONNECTION="$3"

if [[ "$EXECUTABLE" == "R" ]]; then
    exec apptainer exec \
        --writable-tmpfs \
        -B /run/user/$UID:/run/user/$UID \
        "$IMAGE" \
        R --slave -e "IRkernel::main()" --args "$CONNECTION"
else
    exec apptainer exec \
        --writable-tmpfs \
        -B /run/user/$UID:/run/user/$UID \
        "$IMAGE" \
        "$EXECUTABLE" \
        -m ipykernel_launcher \
        -f "$CONNECTION"
fi
```

This wrapper:

- loads the Apptainer module
- starts the container
- launches the requested interpreter
- passes the Jupyter connection file to `ipykernel` or `IRkernel` as required

---

## Step 7 — Configure Jupyter runtime directory

Before registering the container kernel for use in VS Code, ensure that the
Jupyter runtime directory is consistently defined.

Add the following to your shell configuration:

```bash
echo 'export JUPYTER_RUNTIME_DIR=$HOME/.local/share/jupyter/runtime' >> ~/.bashrc
source ~/.bashrc
```

This step only has to be done once and can be skipped in future container registering.

---

# Step 8 — Register the Container

Register the kernels using below post updating paths:

```bash
python register_container_kernel.py \
    registry/sc_basic.yaml
```

The registration script reads the YAML file previously described and automatically creates the appropriate Jupyter kernelspec(s).

Python kernels are written to

```text
~/.local/share/jupyter/kernels/
```

R kernels are registered in the same way.

---

# Step 9 — Using the Container in VS Code

Once registered:

1. Open a notebook
2. Click **Select Another Kernel...**
3. Click **Jupyter Kernal...**
4. Select the desired kernel

```
Python (sc_basic 1.0)
```

or

```
R (sc_basic 1.0)
```

VS Code will then launch the container automatically.

---

## Step 10 — Extract package information for traceability

To make it possible to recreate the container environment in the future—even if the original `.def` file or built `.sif` image is no longer available—extract and archive the following files generated during the container build process:

| File | Purpose |
|------|---------|
| `{container_name}-explicit.txt` | Exact package lock file generated with `micromamba list --explicit`. This records the precise package URLs and package builds required to recreate the environment exactly. |
| `{container_name}-history.yml` | Environment specification generated with `micromamba env export --from-history`. This contains only the packages that were explicitly requested during environment creation, allowing dependencies to be re-resolved. |
| `{container_name}-environment.yml` | Full environment export generated with `micromamba env export`. This records every installed package, including all resolved dependencies, providing a complete description of the final environment. |
| `{container_name}.sif.sha256` | SHA-256 checksum of the built `.sif` image, allowing verification that the container image has not changed or become corrupted. |

These files are produced during the container build using:

```bash
# Save exact package lock for this environment
micromamba list \
    -n ${ENV_NAME} \
    --explicit \
    > /opt/${ENV_NAME}-explicit.txt

# Save environment specification containing only explicitly requested packages
micromamba env export \
    -n ${ENV_NAME} \
    --from-history \
    > /opt/${ENV_NAME}-history.yml

# Save complete environment including all resolved dependencies
micromamba env export \
    -n ${ENV_NAME} \
    > /opt/${ENV_NAME}-environment.yml
```

Archive these files alongside the final `.sif` image (and ideally the corresponding `.def` file) to provide a complete provenance record and maximise the ability to reproduce, verify, or audit the container environment in the future.

---

# Troubleshooting

## Kernel timeout

If VS Code reports

```
Unable to start kernel due to timeout waiting for ports
```

first verify:

- `ipykernel` is installed
- the launcher script is executable

```bash
chmod +x apptainer_kernel_launcher.sh
```

Check the launcher manually:

```bash
apptainer_kernel_launcher.sh \
    image.sif \
    python \
    connection.json
```

The kernel should immediately display

```
To connect another client...
```

---

## Missing runtime directory

If VS Code and Jupyter disagree about the runtime directory, check

```bash
python -m jupyter --paths
```

The runtime directory should exist.

Example:

```text
~/.local/share/jupyter/runtime
```

If necessary

```bash
mkdir -p ~/.local/share/jupyter/runtime
```

---

## Test container startup

Verify container startup time.

```bash
time apptainer exec image.sif python -c "print('hello')"
```

Container startup should normally take well under one second.

---

# Best Practices

- Develop inside a sandbox.
- Only build the final SIF once testing is complete.
- Version both the definition file and the container.
- Keep the YAML registry alongside the image.
- Store launcher scripts under version control.
- Rebuild containers rather than modifying existing SIF files.
- Include `ipykernel` (and `IRkernel` where appropriate) inside the container.
- Keep the definition file as the single source of truth for the software environment.

---

# Files Included

This workflow uses six files:

```
sc_basic.def
sc_basic.yaml
apptainer_kernel_launcher.
build_container.sh
extract_container_provenance.sh
register_container_kernel.py
```

Together these provide:

- reproducible container builds
- automatic kernel registration
- VS Code integration
- reusable Jupyter environments

---

# Appendix

Example files for workflow:

| File | Purpose |
|------|---------|
| [`sc_basic.def`](envs/containers/sc_basic.def) | Apptainer definition file used to build the container |
| [`sc_basic.yaml`](config/kernels/sc_basic.yaml) | Metadata file used for kernel registration |
| [`apptainer_kernel_launcher.sh`](scripts/containers/apptainer_kernel_launcher.sh) | Wrapper script used by Jupyter to launch kernels inside Apptainer |
| [`build_container.sh`](scripts/containers/build_container.sh) | Wrapper script to assist apptainer image construction |
| [`extract_container_provenance.sh`](scripts/containers/extract_container_provenance.sh) | Wrapper script to extract environment details |
| [`register_container_kernel.py`](scripts/containers/register_container_kernel.py) | Python utility to register container kernels |
