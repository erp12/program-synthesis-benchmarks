from typing import Iterable, Optional, Union
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from program_synthesis_benchmarks._impl import (
    DownloadJob,
    download_all,
    read_edge_and_random,
)


__version__ = "0.0.0"


PSB1_PROBLEMS = frozenset(
    [
        "collatz-numbers",
        "compare-string-lengths",
        "count-odds",
        "digits",
        "double-letters",
        "even-squares",
        "for-loop-index",
        "grade",
        "last-index-of-zero",
        "median",
        "mirror-image",
        "negative-to-zero",
        "number-io",  # @TODO There are no edge cases for this problem.
        "pig-latin",
        "replace-space-with-newline",
        "scrabble-score",
        "small-or-large",
        "smallest",
        "string-differences",
        "string-lengths-backwards",
        "sum-of-squares",
        "super-anagrams",
        "syllables",
        "vector-average",
        "vectors-summed",
        "wallis-pi",
        "word-stats",
        "x-word-lines",
    ]
)


PSB2_PROBLEMS = frozenset(
    [
        "basement",
        "bouncing-balls",
        "bowling",
        "camel-case",
        "coin-sums",
        "cut-vector",
        "dice-game",
        "find-pair",
        "fizz-buzz",
        "fuel-cost",
        "gcd",
        "indices-of-substring",
        "leaders",
        "luhn",
        "mastermind",
        "middle-character",
        "paired-digits",
        "shopping-list",
        "snow-day",
        "solve-boolean",
        "spin-words",
        "square-digits",
        "substitution-cipher",
        "twitter",
        "vector-distance",
        "checksum",
    ]
)


ALL_PROBLEMS = PSB1_PROBLEMS | PSB2_PROBLEMS


def download_datasets(
    local_dir: Union[str, Path],
    datasets: Iterable[str],
):
    """Downloads edge and random data files for all datasets to the local directory.

    Will download up to 8 files in parallel. If fewer than 8 core are available, the number of files downloaded in parallel will equal the number of cores.
    
    Args:
        local_dir: The directory under which to download dataset files. Will be created if it does not exist.
        datasets: The names of the datasets to download.

    """
    dl_jobs = []
    for dataset in datasets:
        root = "PSB1" if dataset in PSB1_PROBLEMS else "PSB2"
        dl_jobs.extend(
            [
                DownloadJob(
                    s3_bucket="psb2-datasets",
                    s3_key=f"{root}/datasets/{dataset}/{dataset}-edge.json",
                    local_filename=os.path.join(
                        local_dir, f"{dataset}/{dataset}-edge.json"
                    ),
                ),
                DownloadJob(
                    s3_bucket="psb2-datasets",
                    s3_key=f"{root}/datasets/{dataset}/{dataset}-random.json",
                    local_filename=os.path.join(
                        local_dir, f"{dataset}/{dataset}-random.json"
                    ),
                ),
            ]
        )
    download_all(dl_jobs)


def read_dataset(
    dataset: str,
    *,
    cache_dir: Optional[Union[str, Path]] = None,
    force_download: bool = False,
) -> pd.DataFrame:
    """Reads a dataset into a `DataFrame`.

    If `cache_dir` is not `None`, reading the dataset from the corresponding sub-directory is attempted first.
    If no files are found, a copy of the dataset is downloaded and stored in a dataset specific sub-directory
    of the `cache_dir` and then these files are read into a DataFrame. If `cache_dir=None`, data files will be downloaded
    to a temporary 

    If `force_download` is `True`, the data will be downloaded regardless if existing files exsit in the cache directory. 
    This is useful when repairing data files or picking up changes that may have been made to the source data.
    Files in the cache directory may be overwritten. `force_download` is ignored if `cache_dir=None`.

    Warning: Please cache your data!
        The providers of this (free) data kindly ask that you avoid repeated re-downloads by using a `cache_dir` whenever possible.
        This data changes extremely rarely. Runtimes will be faster for you (and hosting costs lower for the provider) if you 
        download once and read the data from local storage.

    The returned DataFrame will have the following schema:
     * One column per program input named `input1`, `input2`, and so on. Datatypes vary by dataset.
     * `output` - The expected returned output (aka the label). Datatypes vary by dataset.
     * `stdout` - Optional. The expected printed output. String type.
     * `edge_case` - A boolean indicator. True if the case is a human-written "edge case".

    Args:
        dataset: The name of the dataset to download and/or read into a DataFrame.
        cache_dir: The directory of the local filesystem to store the downloaded copy of the data in.
        force_download: Forces the download of a fresh copy of the data, regardless of what is already in `cache_dir`.

    Returns:
        A pandas DataFrame. Each row is a labeled training case.

    """
    df: Optional[pd.DataFrame] = None
    if cache_dir:
        edge_filename = os.path.join(cache_dir, f"{dataset}/{dataset}-edge.json")
        random_filename = os.path.join(cache_dir, f"{dataset}/{dataset}-random.json")
        if (
            force_download
            or (not os.path.exists(edge_filename))
            or (not os.path.exists(random_filename))
        ):
            download_datasets(cache_dir, [dataset])
        df = read_edge_and_random(cache_dir, dataset)
    else:
        with TemporaryDirectory() as temp_dir:
            download_datasets(temp_dir, [dataset])
            df = read_edge_and_random(temp_dir, dataset)
    df = df.rename(columns={"output1": "output", "output2": "stdout"})
    return df


__all__ = ["__version__", "PSB1_PROBLEMS", "PSB2_PROBLEMS", "ALL_PROBLEMS", "download_datasets", "read_dataset"]


if __name__ == "__main__":
    download_datasets("data/psb/", ALL_PROBLEMS)
