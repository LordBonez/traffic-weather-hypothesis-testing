# Traffic and Weather: Hypothesis Testing


## Question and method

Compare mean log-transformed traffic volume between rainy and dry hours:

- Rain: precipitation greater than zero; dry: zero precipitation.
- Response: `log1p(total_vol)`.
- Welch's independent-samples t-test (`equal_var=False`).
- One-way ANOVA for the same two weather categories, preserving the original course analysis.
- Significance threshold: 0.05.

These are comparisons of two groups, not evidence that rain causes a change in traffic.
ANOVA reuses the same observations and is not an independent replication of the t-test.
Hourly observations may be temporally dependent; weather, time of day and other confounders would need
stronger controls for causal or forecasting claims. The original normality/independence assumptions
should be considered when interpreting the reported p-values.

## Run

Use Python 3.10+:

```sh
python -m pip install -r requirements.txt
python hypothesis_tests.py --csv data/merged_traffic_weather.csv --output results/reproduced.json
python -m unittest discover -s tests -v
```

## Results and provenance

The original notebook contains 33,380 records. See `results/reference.json` and VALIDATION.md
for the reproduced local result and validation details. The standalone notebook adapts Section 2
with a data-loading cell and clearer association wording. Reproduced numerical outputs are in the JSON result.
October 2026 packaging adds the CLI, input checks, and automated tests.
This repository covers the hypothesis-testing contribution and makes no claim to the team's model-building work.
