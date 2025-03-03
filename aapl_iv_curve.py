import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Step 1: Define date range and fetch stock data
tick = yf.Ticker("AAPL")
start_date = "2024-06-15"
end_date = "2024-09-30"
hist = tick.history(start=start_date, end=end_date)

# Step 2: Get options data
exp_dates = tick.options
exp = exp_dates[0]
chain = tick.option_chain(exp)

# Step 3: Filter call options by volume
df = chain.calls
df = df[df['volume'] > 10]

# Step 4: Extract key data
X = df['strike']
Y = df['impliedVolatility']
price = hist['Close'].iloc[-1]  # Most recent price in date range

# Step 5: Build the plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=X, y=Y, mode='lines+markers', line=dict(color='#FF6B6B'), name='IV'))
fig.add_vline(x=price, line=dict(color='#FF6B6B', dash='dash', width=1), name=f'Price: ${price:.2f}')

# Step 6: Customize plot layout
fig.update_layout(
    title=f'AAPL IV Curve - Exp: {exp}',
    xaxis_title='Strike ($)',
    yaxis_title='Implied Vol',
    plot_bgcolor='rgb(40, 40, 40)',
    paper_bgcolor='rgb(40, 40, 40)',
    font=dict(color='white'),
    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', gridwidth=0.5),
    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', gridwidth=0.5),
    showlegend=True,
    margin=dict(l=50, r=50, t=50, b=50)
)

# Step 7: Display the plot
fig.show()

# Step 8: Output basic stats
print(f"Exp Date: {exp}")
print(f"Price (as of {end_date}): ${price:.2f}")
print(f"Min IV: {Y.min():.3f} at ${X[Y.idxmin()]:.2f}")
print(f"Max IV: {Y.max():.3f} at ${X[Y.idxmax()]:.2f}")