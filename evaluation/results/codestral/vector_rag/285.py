python
   import pandas as pd
   import scipy.stats as stats

   # Assuming we have a DataFrame df with columns 'strategy', 'resultTime' and 'Regulated_indicators'

   # Calculate mean resultTime for each strategy
   mean_results = df.groupby('strategy')['resultTime'].mean()

   # Calculate variance of resultTime for each strategy
   var_results = df.groupby('strategy')['resultTime'].var()

   # Perform ANOVA test to compare means between strategies
   anova_results = stats.f_oneway(*[df[df['strategy'] == s]['resultTime'] for s in df['strategy'].unique()])

   print("Mean resultTimes:\n", mean_results)
   print("\nVariance of resultTimes:\n", var_results)
   print("\nANOVA test results:", anova_results)