# Provenance

This directory contains metadata describing the origin, history, and transformation of a dataset.

Unlike sample metadata (what the samples are), configuration files (what was intended to be run), or documentation (how methods and pipelines are designed), provenance records what actually happened during sample handling, data generation, and computational processing.

## Examples

### Sample handling
- Tissue dissection or preprocessing performed before sequencing
- Sample collection, storage, and transport conditions
- Processing delays or protocol deviations
- Batch identifiers and processing history

### Data generation
- Library preparation details
- Sequencing instrument and run information
- Failed or repeated sequencing runs
- Operator- or instrument-generated metadata

### Computational processing
- Pipeline versions and parameters used
- Software and environment versions
- Run logs and execution metadata
- QC metrics, thresholds, and decisions
- Dataset lineage and derivation history

## Rules

- Capture metadata automatically where possible.
- Record manual interventions and protocol deviations explicitly.
- Associate provenance with specific samples, runs, or dataset versions.
- Preserve sufficient information for reproducibility, traceability, and auditing.
- Do not duplicate information maintained elsewhere; instead, reference existing sample metadata, configuration files, or documentation where appropriate.
