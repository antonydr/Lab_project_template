# Data

This directory contains all datasets used or produced by the project, together with the metadata and provenance required to understand, reproduce, and trace them.

## Structure

### `raw/`

Original, immutable data acquired from instruments, collaborators, repositories, or other external sources.

**Examples**
- FASTQ files
- Imaging data
- Instrument output
- Downloaded datasets

**Rules**
- Never modify raw data.
- Preserve original filenames where practical.
- Record the source and acquisition details in `provenance/`.

---

### `processed/`

Data derived from raw inputs through cleaning, transformation, analysis, or aggregation.

**Examples**
- Count matrices
- Normalised expression matrices
- Feature tables
- Analysis-ready datasets

**Rules**
- Generated from data in `raw/` or other processed datasets.
- Should be reproducible from the recorded provenance.
- Avoid storing intermediate files unless they are required for reproducibility.

---

### `provenance/`

Records the origin, history, and transformation of datasets, including laboratory procedures, computational workflows, and manual interventions.

See `provenance/README.md` for details.

---

### `metadata/`

Structured information describing datasets, samples, and data files.

**Examples**
- Sample metadata
- Dataset manifests
- Data dictionaries
- Variable definitions
- Experimental design tables

**Rules**
- Metadata should describe data without duplicating it.
- Prefer structured, machine-readable formats where possible.
- Keep metadata versioned alongside the datasets it describes.

---

### `external/`

References to external data resources that are not stored within the repository.

**Examples**
- Repository accessions
- Download manifests
- Checksums
- Data source documentation
- Scripts for retrieving public datasets

**Rules**
- Do not commit large third-party datasets unless necessary.
- Record stable identifiers (e.g. accession numbers or DOIs).
- Ensure external datasets can be retrieved and verified.

## General Rules

- Organise data according to its role rather than file type.
- Maintain clear relationships between raw data, processed outputs, metadata, and provenance.
- Preserve reproducibility by documenting every transformation applied to the data.
- Avoid unnecessary duplication of datasets.
- Exclude sensitive or restricted data unless explicitly permitted and appropriately protected.
