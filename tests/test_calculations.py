import pandas as pd
import numpy as np

def test_mom_yoy_calculations():
    # Create a sample monthly dataframe for 15 months
    dates = pd.date_range(start='2023-01-01', periods=15, freq='MS')
    data = {
        'series1': np.arange(15, dtype=float),
        'series2': np.arange(30, 45, dtype=float)
    }
    df = pd.DataFrame(data, index=dates)

    # Calculate Month-over-Month (MoM) percentage change
    mom = df.pct_change(1)

    # Calculate Year-over-Year (YoY) percentage change
    yoy = df.pct_change(12)

    # Test: The first MoM value should be NaN because no prior month exists
    assert pd.isna(mom.iloc[0]['series1'])

    # Test: Check a sample MoM calculation is correct
    expected_mom = (df.iloc[1]['series1'] - df.iloc[0]['series1']) / df.iloc[0]['series1']
    assert mom.iloc[1]['series1'] == expected_mom

    # Test: The first 12 YoY values should be NaN because no prior year exists
    assert all(pd.isna(yoy.iloc[:12, 0]))

    # Test: Check a sample YoY calculation is correct at month 13
    expected_yoy = (df.iloc[12]['series1'] - df.iloc[0]['series1']) / df.iloc[0]['series1']
    assert yoy.iloc[12]['series1'] == expected_yoy
