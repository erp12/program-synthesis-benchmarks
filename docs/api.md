# API

The `program_synthesis_benchmarks` library provides immutable (fozen) sets of the dataset names which it can download and read. There are sets for each version of the PSB suite and a set that provides the union of all suites. 

```python
import program_synthesis_benchmarks as psb

print(psb.PSB1_PROBLEMS)
# frozenset({'collatz-numbers', 'compare-string-lengths', 'count-odds', 'digits', ... 

print(psb.PSB2_PROBLEMS)
# frozenset({'basement', 'bouncing-balls', 'bowling', 'camel-case', 'coin-sums', ...

print(psb.ALL_PROBLEMS)
# frozenset({'collatz-numbers', 'compare-string-lengths', 'count-odds', 'digits', ... 
```

The rest of the API is composed of two functions documented below.

::: program_synthesis_benchmarks
    handler: python
    options:
        members:
            - download_datasets
            - read_dataset
