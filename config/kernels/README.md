# Container Kernel Configuration

This directory contains YAML configuration files used to register container-based environments as Jupyter kernels.

Each YAML file defines how a container environment is exposed to Jupyter, including:

- container name
- container version
- container image location
- container type
- languages
- executables
- kernel name(s) and display name(s)
- resources which the container should be used with
- key packages
- definition file location

## Directory structure

Example:

```text
config/
└── kernels/
    ├── sc_basic.yaml
    └── other_container.yaml
```

For clarity, each YAML filename should ideally match the container name.

Example:

```text
sc_basic.yaml
sc_basic.sif
sc_basic.def
```

Keeping names consistent allows the container build and registration scripts to locate related files automatically.

`sc_basic.yaml` provided as an example in this directory. 

## Registering a kernel

From the project root:

```bash
python scripts/containers/register_container_kernel.py \
    config/kernels/sc_basic.yaml
```

This creates a Jupyter kernel specification in:

```text
~/.local/share/jupyter/kernels/
```

The registered kernel will then be available in Jupyter interfaces.

## Supported containers

Currently supported:

- Apptainer/Singularity containers

Future support may include:

- Docker
- Podman

The kernel configuration describes how a container is launched.

The container build recipe (e.g. `.def` for apptainer) is stored separately under:

```text
envs/containers/
```

## Relationship to other files

```text
envs/containers/
        |
        | build
        v
container image (.sif / docker image)
        |
        | referenced by
        v
config/kernels/*.yaml
        |
        | registered by
        v
scripts/containers/register_container_kernel.py
        |
        v
Jupyter kernel
```