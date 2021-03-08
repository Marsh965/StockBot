import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from numerize import numerize
import numpy
""" period : str
             Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
             Either Use period parameter or use start and end
    interval : str
             Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
             Intraday data cannot extend last 60 days
"""
def line_color(Open, Close):
	diff = Close - Open
	if diff >= 0:
		return 'g'
	if diff < 0:
		return 'r'
	
style.use('fivethirtyeight')

STOCK = 'apha'
PERIOD = '1mo'
INTERVAL = '1d'

if __name__ == '__main__':
	tickr = yf.Ticker(STOCK)
	tick = tickr.history(period=PERIOD, interval=INTERVAL)
	tick = tick.dropna(axis='index', how='any')
	day_tick = tickr.history(period='1d')
	with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		print(tick)
		
		
	VOLUME = tick['Volume'].iloc[-1]
	Open = tick['Open'].iloc[0]
	Close = tick['Close'].iloc[-1]
	per_Change = round((Close-Open)/Open * 100,2)
	color = line_color(Open, Close)

	plt.plot(tick['Close'], color)
	#plt.plot(tick['Volume'])
	plt.text(0.1,0.9, str(per_Change)+'%', transform=plt.gca().transAxes, color=color)
	plt.title(STOCK.upper())
	plt.ylabel('Closing Price')
	plt.xticks(rotation=45)
	plt.tight_layout()
	print(VOLUME)

	plt.show()
	plt.savefig('chart.png')

	print(numpy.__version__)

