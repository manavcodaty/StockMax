from beibo import oracle

oracle(
    portfolio=["TSLA", "AAPL", "NVDA", "NFLX"],  # stocks you want to predict
    start_date="2020-01-01",  # date from which it will take data to predict
    # allocate 30% to TSLA and 20% to AAPL...(equal weighting  by default)
    weights=[0.3, 0.2, 0.3, 0.2],
    prediction_days=30,  # number of days you want to predict
)
