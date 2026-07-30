# Running Nextflow on the HPC

If you are running Nextflow on a HPC, the usually HPC provides Nextflow and container modules such as Apptainer as environment modules. The commands below demonstrate how to load the required software, obtain a pipeline, and execute a test run.

## Load Required Modules

Load the available Nextflow and Apptainer modules:

```bash
module load Nextflow/24.10.2
module load apptainer
```

## Download a Pipeline

Pull the latest copy of the nf-core RNA-seq pipeline into your local Nextflow cache:

```bash
nextflow pull nf-core/rnaseq
```

You can verify the pipeline is available and inspect its metadata using:

```bash
nextflow info nf-core/rnaseq
```

## Run the Test Dataset

The following command executes the built-in test dataset using Apptainer containers:

```bash
nextflow run nf-core/rnaseq \
    -r 3.19.0 \
    -profile test,apptainer \
    --outdir test_results
```

### Command Options

| Option | Description |
|--------|-------------|
| `-r 3.19.0` | Runs a specific version of the pipeline for reproducibility. |
| `-profile test,apptainer` | Uses the pipeline's test dataset and executes tasks within Apptainer containers. |
| `--outdir test_results` | Writes pipeline outputs to the `test_results` directory. |

## Notes

- Load the required modules at the start of each new HPC session.
- The first execution may take longer while Nextflow downloads the pipeline and Apptainer retrieves the required container images.
- For production analyses, replace the `test` profile with the appropriate configuration and provide your own input samplesheet and pipeline parameters.
