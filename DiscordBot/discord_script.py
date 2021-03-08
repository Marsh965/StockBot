import discord
from discord_keys import bot_token
from discord.ext import commands
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from functions import line_color
from numerize import numerize
import os


TOKEN = bot_token
bot = commands.Bot(command_prefix='!')
style.use('fivethirtyeight')


# Notifies when bot is live
@bot.event
async def on_ready():
	print(f'{bot.user} has connected successfully')


# Command for Stock updates	
@bot.command(
	name = 'stock',
	help = 'Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,max\n'
		   'Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo'
      		)

async def getPrice(ctx, stock_name, period, interval):
	tickr = yf.Ticker(stock_name)
	tick = tickr.history(period=period, interval=interval)
	day_tick = tickr.history(period='1d') # creates new db for 24hr Volume

	tick = tick.dropna() # drops missing values


	OPEN = tick['Open'].iloc[0]
	CLOSE = tick['Close'].iloc[-1]
	VOLUME = day_tick['Volume'].iloc[0]

	color = line_color(OPEN, CLOSE) # Selects Red or Green 
	per_Change = round((CLOSE-OPEN)/OPEN * 100, 2)

	plt.clf() # Clears previous chart
	plt.plot(tick['Close'], color)
	plt.text(0.1, 0.9, str(per_Change)+'%', transform=plt.gca().transAxes, color=color)
	plt.title(stock_name.upper())
	plt.ylabel('Closing Price')
	plt.xticks(rotation=45)
	plt.tight_layout()

	plt.savefig('chart.png')
	file = discord.File('chart.png', filename='chart.png')
	await ctx.send('online.png', file=file)


	price = round(CLOSE, 2)
	_10dayVol = numerize.numerize(tickr.info['averageDailyVolume10Day'], 2)
	_24hrVol = numerize.numerize(int(VOLUME), 2)
	market_cap = numerize.numerize(tickr.info['marketCap'], 2)

	await ctx.send(f"""
Stock Price: ${price}
Market Cap: {market_cap}

24 Hour Vol: {_24hrVol}
10 Day Vol: {_10dayVol}""")


bot.run(TOKEN)