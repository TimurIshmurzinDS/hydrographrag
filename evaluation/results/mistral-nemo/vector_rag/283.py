import pandas as pd

def compare_series(series1, series2):
    # Ensure both series have the same index for comparison
    series1 = series1.reindex(series2.index)
    series2 = series2.reindex(series1.index)

    # Calculate absolute difference between two series
    diff = abs(series1 - series2)

    # Create a DataFrame with results
    result = pd.DataFrame({
        'Series 1': series1,
        'Series 2': series2,
        'Difference': diff
    })

    return result

# Example usage:
s1 = pd.Series([1, 2, 3], index=['2022-01-01', '2022-01-02', '2022-01-03'])
s2 = pd.Series([2, 3, 4], index=['2022-01-01', '2022-01-02', '2022-01-03'])

result = compare_series(s1, s2)
print(result)