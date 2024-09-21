from Formats import CalendarWeather


def main():
	"""
	Just print out the weather!
	"""

	cwPath = "Scripts/Assets/VANILLA_CLDWEATHER.BIN"
	cw = CalendarWeather()
	cw.read(cwPath)
	cw.pretty_print()


if __name__ == "__main__":
	main()
