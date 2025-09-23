# kubhist2

This repo contains scripts to download and transform the Språkbanken Text (SBX) Kubhist 2 collection of files into a huggingface dataset.

The resulting dataset is available on the huggingface hub at https://huggingface.co/datasets/iguanodon-ai/kubhist2.

### Steps

1. `poetry run python main.py get-data`
2. `poetry run python main.py process-data`

### Short description

In a nutshell, this hugginface dataset version offers:

- only the OCRed text
- available in decadal subsets

Load the whole corpus using `dataset = load_dataset("iguanodon-ai/kubhist2")`, or a decadal subset using `dataset = load_dataset("`iguanodon-ai/`/kubhist2", "decade")` where `decade` is a string in `range(1640, 1910, 10)`.

Concatenate several decades like so:

```python
from datasets import load_dataset, concatenate_datasets

ds_1800 = load_dataset("iguanodon-ai/kubhist2", "1800")
ds_1810 = load_dataset("iguanodon-ai/kubhist2", "1810")
ds_1820 = load_dataset("iguanodon-ai/kubhist2", "1820")

ds_1800_1820 = concatenate_datasets([
                        ds_1800["train"],
                        ds_1810["train"],
                        ds_1820["train"]
                        ])
```

### Acknowledgments

Many thanks go to Språkbanken Text for creating and curating this resource.
