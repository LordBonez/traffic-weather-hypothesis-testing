# Validation - October 15, 2026

- Five Python unit tests pass, covering balanced groups and invalid inputs.
- The CLI reproduced the original notebook's Welch t-test and ANOVA results on the local team dataset.
- Rows: 33,380; rainy: 4,681; dry: 28,699.
- Welch t: -3.95457254394; p = 7.75259667588e-05.
- ANOVA F: 16.3734760896; p = 5.2124972605e-05.
- Response: log1p(total_vol); significance threshold 0.05.
- Dataset SHA-256: `a085219a06fa69395c149b7d4b423e25614086a0bffc68587b2ab3965fbc5f6a`. Dataset is not included in this repository.
- Tested with Python 3.12 and SciPy 1.16.2.
- See README for statistical assumptions and interpretation limits.
