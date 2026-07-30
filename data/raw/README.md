# Raw Data

This directory contains immutable, source-level data directly generated from upstream pipelines or external providers (e.g. CellRanger, Spaceranger, FASTQ).

## Key properties
- Never modified after ingestion
- Mirrors original output structure where possible
- Reproducible from upstream pipeline or original source

## Examples
- CellRanger outputs per sample
- FASTQ-derived count matrices before harmonisation
- Spatial transcriptomics raw outputs (e.g. Visium, Xenium)

## Rules
- Do NOT edit files in this directory
- Do NOT store analysis-ready objects here
- Treat as read-only input for all pipelines
