# -*- coding: utf-8 -*-
"""Shenshu-Task1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t_zlprEmxz88aIvzm3J5xqoVhT7MQ0EQ
"""

import pandas as pd
import numpy as np

df = pd.read_csv('/content/tradelog.csv')
df.head()

import pandas as pd

# Load the trade log CSV file
df = pd.read_csv('/content/tradelog.csv')

# Calculate profit/loss for each trade
df['Profit'] = (df['Exit Price'] - df['Entry Price']) * 100  # Assuming quantity is 100 shares

# Parameters
initial_portfolio = 6500 * 100  # Convert to paise
risk_free_rate = 0.05 / 100  # Convert to a percentage

# 1. Total Trades
total_trades = len(df)

# 2. Profitable Trades
profitable_trades = len(df[df['Profit'] > 0])

# 3. Loss-Making Trades
loss_making_trades = total_trades - profitable_trades

# 4. Win rate
win_rate = profitable_trades / total_trades

# 5. Average Profit per trade
average_profit = df[df['Profit'] > 0]['Profit'].mean()

# 6. Average Loss per trade
average_loss = df[df['Profit'] < 0]['Profit'].mean()

# 7. Risk Reward ratio
risk_reward_ratio = abs(average_profit / average_loss)

# 8. Expectancy
expectancy = (win_rate * average_profit) - ((1 - win_rate) * abs(average_loss))

# 9. Average ROR per trade
average_ror_per_trade = df['Profit'].mean() / initial_portfolio

# 10. Sharpe Ratio
sharpe_ratio = (df['Profit'].mean() - (risk_free_rate * initial_portfolio)) / df['Profit'].std()

# 11. Max Drawdown
df['cumulative_profit'] = df['Profit'].cumsum()
peak = df['cumulative_profit'].cummax()
drawdown = peak - df['cumulative_profit']
max_drawdown = drawdown.max()

# 12. Max Drawdown Percentage
max_drawdown_percentage = (max_drawdown / peak.max()) * 100

# 13. CAGR
# Assuming the periods are in days and the trades are over one year.
ending_value = initial_portfolio + df['Profit'].sum()
df['Entry Time'] = pd.to_datetime(df['Entry Time'])
df['Exit Time'] = pd.to_datetime(df['Exit Time'])
years = (df['Exit Time'].iloc[-1] - df['Entry Time'].iloc[0]).days / 365.25
cagr = ((ending_value / initial_portfolio) ** (1/years)) - 1

# 14. Calmar Ratio
calmar_ratio = cagr / abs(max_drawdown_percentage)

# Create a DataFrame to hold the results
results = pd.DataFrame({
    'Parameter': ['Total Trades', 'Profitable Trades', 'Loss-Making Trades', 'Win Rate',
                  'Average Profit per Trade', 'Average Loss per Trade', 'Risk Reward Ratio',
                  'Expectancy', 'Average ROR per Trade', 'Sharpe Ratio', 'Max Drawdown',
                  'Max Drawdown Percentage', 'CAGR', 'Calmar Ratio'],
    'Value': [total_trades, profitable_trades, loss_making_trades, win_rate,
              average_profit, average_loss, risk_reward_ratio, expectancy,
              average_ror_per_trade, sharpe_ratio, max_drawdown,
              max_drawdown_percentage, cagr, calmar_ratio]
})

# Save the results to a CSV file
results.to_csv('results2.csv', index=False)

# Print the results
print(results)