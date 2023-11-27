from typing import Sequence, Union, Any
from dataclasses import dataclass
import os
from pathlib import Path
import multiprocessing as mp
import pandas as pd  # type: ignore
import boto3  # type: ignore


# Needs to be initialized in each child process for parallel reads.
_s3: Any = None  # type: ignore


def init_s3():
    global _s3
    _s3 = boto3.client("s3")


@dataclass(frozen=True)
class DownloadJob:
    s3_bucket: str
    s3_key: str
    local_filename: str


def download(job: DownloadJob):
    os.makedirs(os.path.dirname(job.local_filename), exist_ok=True)
    try:
        _s3.download_file(job.s3_bucket, job.s3_key, job.local_filename)
    except Exception as e:
        raise Exception(f"Failed to download s3://{job.s3_bucket}/{job.s3_key}.") from e


def download_all(jobs: Sequence[DownloadJob]):
    if len(jobs) == 0:
        return   
    pool = mp.Pool(min(mp.cpu_count(), len(jobs), 8), initializer=init_s3)
    pool.imap_unordered(download, jobs)
    pool.close()
    pool.join()


def read_edge_and_random(root_dir: Union[str, Path], dataset: str) -> pd.DataFrame:
    edge_filename = os.path.join(root_dir, f"{dataset}/{dataset}-edge.json")
    random_filename = os.path.join(root_dir, f"{dataset}/{dataset}-random.json")
    edge = pd.read_json(edge_filename, lines=True).assign(edge_case=True)
    random = pd.read_json(random_filename, lines=True).assign(edge_case=False)
    return pd.concat([edge, random])