# kubhist2

This repo contains scripts to download and transform the Språkbanken Text (SBX) Kubhist 2 collection of files into a huggingface dataset.

The resulting dataset is available on the huggingface hub at https://huggingface.co/datasets/iguanodon-ai/kubhist2.

This repo contains code originally written in May 2023, and cleaned/updated today (commit date).

### Steps

1. `poetry run python main.py get-data`
2. `poetry run python main.py process-data`

If you have lots of CPU (and by extension disk space), you can use the `--n-cores NUMBER` here to specify how many threads you want and bypass the default (default is how many cores you have minus 4).


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



# License and contact

<a href="https://iguanodon.ai"><img src="./img/iguanodon.ai.png" width="125" height="125" align="right" /></a>

This code was written by Simon Hengchen ([https://iguanodon.ai](https://iguanodon.ai)). The code is made available to the public [under the permissive CC BY-SA 4.0 license](http://creativecommons.org/licenses/by-sa/4.0/). If you use the data that running this script provides, include the following citations in your paper:

```bibtex
@misc{kubhist,
  doi = {10.23695/h7qd-bj40},
  url = {https://spraakbanken.gu.se/resurser/kubhist},
  author = {{Språkbanken Text}},
  keywords = {Language Technology (Computational Linguistics)},
  language = {swe},
  title = {Kubhist},
  publisher = {Språkbanken Text},
  year = {2025}
}
```


<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
