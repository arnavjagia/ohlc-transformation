# OHLC Transformation and SMA/ EMA computation

## **Project Structure**

```
.
├── data/
│   └── output_file.csv       # Input dataset containing daily stock prices
├── output/                   # Generated result files per ticker
│   ├── result_AAPL.csv
│   ├── result_AMD.csv
│   └── ...
├── playground/               # Jupyter notebooks for rough work and testing
│   └── playground.ipynb
├── data_exploration.ipynb    # Notebook for initial data analysis and exploration
├── main.py                   # Main script containing calculation and file writing logic
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## **Assumptions & Highlights**

- **Data Quality**: 
    - No missing data found in the input set.
    - Exchange holidays are taken into consideration (e.g., New Year's Day).
    - The dataset spans from Jan '18 to Dec '19 (503 trading days).
- **EMA Calculation**:
    - Current price in `EMA = (Current Price - Previous Day's EMA) * Multiplier + Previous Day's EMA` is taken as the corresponding closing price of that month.
    - The EMA calculation uses the standard formula with a smoothing factor of `2 / (N + 1)`.
    - The initial EMA value is seeded with the SMA of the same window size.
- **Adjusted Close**: use of `adjclose` inplace of `close` may be better indicative when used for SMA and EMA for monthly aggregation
