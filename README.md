# Program Synthesis Benchmarks

A Python library for downloading and reading the datasets from the Program Synthesis Benchmark Suite ([v1](https://cs.hamilton.edu/~thelmuth/Pubs/2015-GECCO-benchmark-suite.pdf) and [v2](https://arxiv.org/abs/2106.06086)). Downloaded datasets are stored as parquet, and read into
pandas DataFrames.

## Rationale

The _Program Synthesis Benchmark Suite_ is a set of general programming tasks used to evaluate program synthesis systems. The authors of the PSB suites provide canonical datasets of over 1 million labeled cases per problem for use in inductive program synthesis systems. These datasets have been used to standardize development and evaluation many methods.

A unique feature of the PSB suite dtasets is their complex schemas. Many problems involve complex data types, such as collection types, and occastionally specify both returned and printed (stdout) outputs. Additionally, a small subset of training cases (so called "edge cases") are considred critical to the evaluation of synthesized programs and are often handled differently during synthesis. For these reasons, and others implied below, the `program_synthesis_benchmarks` library is tool that helps practitioners manage these datasets.

The `program_synthesis_benchmarks` library provides functionality for downloading and reading data files. It uses parquet files (read as Pandas DataFrames) to take advantage of explicit schemas and complex column types. The library also caches data locally (at a location of your choosing) to avoid repeated downloads.

### Prior Art

The predesessor of this library is [psb2-python](https://github.com/thelmuth/psb2-python), a library for fetching PSB2 datasets from the same source. `psb2-python` has a slightly different abstraction from `program_synthesis_benchmarks` and there are a few trade-offs that motivated the creation of the new library.

|  | **`psb-python`** | **`program_synthesis_benchmarks`** |
|---|---|---|
| **PSB1** | :x: | :white_check_mark: |
| **PSB2** | :white_check_mark: | :white_check_mark: |
| **Representation** | 3 "formats" that organize data into nested python collections. | [Pandas](https://pandas.pydata.org/) DataFrame |
| **Sampling** | Forces sampling and train-test split. | Reads entire dataset. |
| **Storage format** | Uncompressed JSON lines files | Parquet |
| **Metadata - Data types** | :x: | Parquet and DataFrame have explicit schema (dtypes). |
| **Metadata - Edge cases** | :x: | Includes indicators of human-written "edge cases" versus randomly generated cases. |
| **Metadata - Return vs Stdout** | :x: | Separate columns named `output` and `stdout` |
| **Concurrent Downloads** | Serial | Up to 8 files in parallel |

> :no_entry_sign: This library is currently using JSON lines files while we work on getting parquet data files hosted.

The read-or-download pattern for libraries that provide data for experimentation was popularized by [Penn Machine Learning Benchmarks](https://github.com/EpistasisLab/pmlb). PMLB focuses on classification and regression tasks, while this library provides datasets for program synthesis.

## Getting Started

Install `program-synthesis-benchmarks` from [pypi](https://pypi.org/project/program-synthesis-benchmarks/) using pip. Using a virtual environment is recommended in most cases.

```commandline
pip install program-synthesis-benchmarks
```

To get a frozenset of supported datasets, use `ALL_PROBLEMS`. For just PSB1 or PSB2 use `PSB1_PROBLEMS` or `PSB2_PROBLEMS` respectively.

```python
from program_synthesis_benchmarks import PSB1_PROBLEMS

print(PSB1_PROBLEMS)
# frozenset({'collatz-numbers', 'compare-string-lengths', 'count-odds', 'digits', ... 
```

To download the parquet data files for a set of problem, provide a path and collection of datasets to `download_datasets`.

``` py
from program_synthesis_benchmarks import download_datasets
download_datasets("./path/to/data", ["fizz-buzz", "gcd", "replace-space-with-newline"])
```

After all donwloads are complete, the file system will contain one directory per dataset containing 2 parquet files each. One file contains human written "edge" cases, the other contains 1 million randomly generated cases.

```
path
└── to
    └── data
        ├── fizz-buzz
        │   ├── fizz-buzz-edge.parquet
        │   └── fizz-buzz-random.parquet
        ├── gcd
        │   ├── gcd-edge.parquet
        │   └── gcd-random.parquet
        └── replace-space-with-newline
            ├── replace-space-with-newline-edge.parquet
            └── replace-space-with-newline-random.parquet
```

To read the data of a specific problem, use `read_dataset`. If you have previously download the data for this problem you can specify a `cache_dir` to read from local storage. Otherwise the datasets will be downloaded.

``` py
from program_synthesis_benchmarks import read_dataset

read_dataset("gcd", cache_dir="./path/to/data")
#          input1  input2  output  edge_case
#  0            1       1       1       True
#  1            4  400000       4       True
#  2           54      24       6       True
#  3         4200    3528     168       True
#  4       820000   63550    2050       True
#  ...        ...     ...     ...        ...
#  999995  793436  643541       1      False
#  999996  382449  108033       3      False
#  999997  910646  435802       2      False
#  999998  347104  474860       4      False
#  999999  375006  743332       2      False
#
#  [1000006 rows x 4 columns]

```

More detailed documentation can be found in the [API docs](api/).


## Citation

If you use these datasets in a publication, please cite the paper *PSB2: The Second Program Synthesis Benchmark Suite*.

BibTeX entry for paper:

```bibtex
@InProceedings{Helmuth:2021:GECCO,
  author =	"Thomas Helmuth and Peter Kelly",
  title =	"{PSB2}: The Second Program Synthesis Benchmark Suite",
  booktitle =	"2021 Genetic and Evolutionary Computation Conference",
  series = {GECCO '21},
  year = 	"2021",
  isbn13 = {978-1-4503-8350-9},
  address = {Lille, France},
  size = {10 pages},
  doi = {10.1145/3449639.3459285},
  publisher = {ACM},
  publisher_address = {New York, NY, USA},
  month = {10-14} # jul,
  doi-url = {https://doi.org/10.1145/3449639.3459285},
  URL = {https://dl.acm.org/doi/10.1145/3449639.3459285},
}
```

## To Do

- Download parquet files for better compression and faster reading.
- Liscence and code of conduct
