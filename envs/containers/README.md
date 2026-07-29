# Container Build Definitions

This directory contains container build recipes used to create reproducible computational environments.

Container definitions are source files and should be tracked in version control.

Built container images are generated artefacts and should not be stored in this repository.

## Directory structure

Example:

```text
envs/
└── containers/
    ├── sc_basic.def
    ├── pytorch_gpu.Dockerfile
    └── README.md
```

`sc_basic.def` is provided as an example. This has a focus on basic single cell/nuclei and spatial environments for single cell analysis work but can be used as a guidance. As it uses many packages, `micromamba` is used internally. 

## Supported definition formats

### Apptainer / Singularity

Definition file:

```text
sc_basic.def
```

Builds an image:

```text
sc_basic.sif
```

Example:

```bash
./scripts/containers/build_container.sh sc_basic
```

---

### Docker

Definition file:

```text
pytorch_gpu.Dockerfile
```

Builds a Docker image:

```text
pytorch_gpu:latest
```

Docker images are managed by the Docker image store and are not stored as files in this directory.

---

### Podman

Definition file:

```text
tool.Containerfile
```

Podman follows a similar workflow to Docker while using its own image storage.

## Naming conventions

Container names should match across related files.

Example:

```text
Container name:
sc_basic

Definition:
envs/containers/sc_basic.def

Kernel configuration:
config/kernels/sc_basic.yaml

Apptainer image:
sc_basic.sif
```

Keeping names consistent allows scripts to automatically locate related files.

## Building containers

Containers can be built manually or can be built using the project container scripts.

Example:

```bash
./scripts/containers/build_container.sh sc_basic
```

The build script will:

1. Locate the matching container definition
2. Check the corresponding kernel configuration exists
3. Build the container image
4. Store the image according to `config/containers.yaml`

## Container storage

Container images are generated artefacts and should not be committed to Git.

Examples:

```text
*.sif
Docker images
Podman images
```

Image locations and container storage settings are controlled through:

```text
config/containers.yaml
```

This keeps storage locations separate from project code.