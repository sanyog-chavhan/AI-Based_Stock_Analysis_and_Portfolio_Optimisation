# AI-Based Stock Analysis & Portfolio Optimisation

A Streamlit web app that downloads stock market data, calculates common technical indicators, adds a short AI-written explanation for each one, and gives a Buy / Hold / Sell signal for every stock you enter. It can also suggest how to split money across several stocks.

**Live demo:** https://huggingface.co/spaces/sanyog16/AI-Based_Stock_Analysis_and_Portfolio_Optimisation

> **Disclaimer:** This app is for learning only. It is not financial advice. Markets are risky, so do your own research.


## What the app does

1. You enter one or more stock tickers, for example `TSLA, AAPL, DELL, AMD`.
2. You choose a date range, the indicator settings and your risk tolerance.
3. The app shows:
   - Charts for stock price, RSI and MACD, with the indicator values.
   - A one-sentence AI explanation of each indicator (Moving Average, Bollinger Bands, RSI, MACD).
   - A colour-coded Buy / Hold / Sell signal, with the reasons behind it.
   - A suggested allocation across your selected stocks, based on your risk tolerance.

The AI explanations need an OpenAI API key. Everything else works from market data alone.


## How to use it

1. Open the live demo, or run the app locally (see below).
2. Type your tickers, separated by commas. Use the ticker as it appears on Yahoo Finance. Stocks outside the US need a suffix, such as `.NS` for India's NSE.
3. Pick your date range and settings, then run the analysis.
4. Read the charts, the explanations and the signal for each stock.


## Run it on your own computer

You need Python 3 installed.

**1. Get the code and open the project folder.**

**2. Create and activate a virtual environment.**
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install the dependencies.**
```bash
pip install -r requirements.txt
```

**4. Add your OpenAI API key.**

Create a file called `.streamlit/secrets.toml` in the project folder:
```toml
OPENAI_API_KEY = "sk-..."
```
Keep this file private and never upload it to GitHub. The app currently reads the key from this file, so it needs to exist before you run the app.

**5. Start the app.**
```bash
python -m streamlit run app.py
```
Then open http://localhost:8501 in your browser.


## Settings and indicators

| Indicator | What it shows | Default |
|---|---|---|
| Moving Average (MA) | The average price over a set number of days, which smooths out short-term swings | Adjustable |
| RSI | Momentum. Above 70 often means overbought, and below 30 often means oversold | 14 days |
| MACD | Trend and momentum, based on two moving averages and a signal line | 12, 26, 9 |
| Bollinger Bands | A band around the average price that widens when the price is volatile | 20 days, 2 standard deviations |
| Risk tolerance | A number from 0 to 1 that you set. It affects the suggested allocation | You choose |


## How the Buy / Hold / Sell signal works

The signal is a simple point score. It is a transparent rule of thumb, not a prediction.

| Check | Points |
|---|---|
| RSI below 30 (oversold) | +2 |
| RSI above 70 (overbought) | -2 |
| MACD above 0 (bullish) | +1 |
| MACD below 0 (bearish) | -1 |
| Price above the moving average | +1 |
| Price below the moving average | -1 |
| Price below the lower Bollinger Band | +1 |
| Price above the upper Bollinger Band | -1 |

A total of +2 or more gives **Buy**. A total of -2 or less gives **Sell**. Anything in between gives **Hold**.


## Project files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit user interface |
| `data_loader.py` | Downloads price data from Yahoo Finance (yfinance) |
| `indicators.py` | Calculates the indicators and draws the Plotly charts |
| `ai_insights.py` | Asks OpenAI for the one-sentence explanations |
| `investment_signal.py` | Works out the Buy / Hold / Sell signal |
| `portfolio_optimiser.py` | Calculates the suggested portfolio weights |
| `requirements.txt` | The Python packages the app needs |


## Troubleshooting

**`streamlit: command not found`**
Activate your virtual environment, then start the app with `python -m streamlit run app.py`.

**"No secrets found" error**
The file `.streamlit/secrets.toml` is missing. Create it as shown in step 4 above.

**The AI explanations show an error message**
- "Invalid OpenAI API key": check the key in `secrets.toml`.
- "Rate limit exceeded": your OpenAI account may be out of credit, or you are sending too many requests. Check your billing page on the OpenAI platform.

**`pip install` fails when building numpy**
You are probably using a very new Python version with an old numpy. Make sure `requirements.txt` lists `numpy` without a version pin, or use an older Python version.


## Security and data

- Never commit your API key. Keep it in `.streamlit/secrets.toml`, and add that file to `.gitignore`.
- The app only uses public market data and is meant for research and demonstration.


## Licence

MIT. You are free to use this for learning and personal projects. If you build a commercial product, check that your data sources allow it.
