def smooth_trajectory(df, window_size=5):
    """
    Smooth the vehicle trajectory using
    a moving average.

    X and Y coordinates are smoothed separately.
    """

    df = df.copy()

    # Smooth X coordinate
    df["X_smooth"] = (
        df["X"]
        .rolling(
            window=window_size,
            center=True,
            min_periods=1
        )
        .mean()
    )

    # Smooth Y coordinate
    df["Y_smooth"] = (
        df["Y"]
        .rolling(
            window=window_size,
            center=True,
            min_periods=1
        )
        .mean()
    )

    return df
