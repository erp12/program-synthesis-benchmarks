from pathlib import Path

from program_synthesis_benchmarks import download_datasets, read_dataset


class TestDownloadDatasets:

    def test_empty(self, tmp_path: Path):
        # Empty list should do nothing.
        download_datasets(tmp_path, [])
        assert list(tmp_path.iterdir()) == []

    def test_download_one(self, tmp_path: Path):
        download_datasets(tmp_path, ["gcd"])
        problem_dir = tmp_path / "gcd"
        assert list(tmp_path.iterdir()) == [problem_dir]
        files = list(problem_dir.iterdir())
        files.sort()
        assert files == [problem_dir / "gcd-edge.json", problem_dir / "gcd-random.json"]


class TestReadDataset:

    def test_local_cache(self):
        df = read_dataset("gcd", cache_dir="tests/test_data/")
        assert df.shape == (16, 4)
        assert df.dtypes.index.to_list() == ["input1", "input2", "output", "edge_case"]
        assert df.edge_case.dtype == bool
        assert df.loc[df.edge_case].shape[0] == 6

    def test_dataset_with_stdout(self):
        df = read_dataset("replace-space-with-newline", cache_dir="tests/test_data/")
        assert df.shape == (40, 4)
        assert df.dtypes.index.to_list() == ["input1", "output", "stdout", "edge_case"]
        assert df.edge_case.dtype == bool
        assert df.output.dtype == int
        assert df.stdout.dtype == object  # AKA str
        assert df.loc[df.edge_case].shape[0] == 30
