# Seperate file for functions

def line_color(Open, Close):
	diff = Close - Open
	if diff >= 0:
		return 'g'
	if diff < 0:
		return 'r'