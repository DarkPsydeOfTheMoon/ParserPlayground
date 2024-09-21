from enum import Enum
from .exbip.Serializable import Serializable
from .FTD import WeatherTypes


class CalendarWeather(Serializable):

	MONTH_NAMES = [
		"April", "May", "June", "July",
		"August", "September", "October", "November",
		"December", "January", "February", "March",
	]

	MONTH_DAYS = [
		30, 31, 30, 31,
		31, 30, 31, 30,
		31, 31, 28, 31,
	]

	def __init__(self):
		self.Months = [None]*12

	def __rw_hook__(self, rw):
		for i in range(12):
			self.Months[i] = rw.rw_objs(self.Months[i], DailyWeather, self.MONTH_DAYS[i])

		failed = False
		try:
			rw.assert_eof()
		except Exception:
			print("Failed to read file!")
			remainder = rw._bytestream.peek()
			print(len(remainder), remainder)

	def pretty_print(self):
		for i in range(12):
			print(f"{self.MONTH_NAMES[i]}:")
			for j in range(self.MONTH_DAYS[i]):
				print("  {} ({}): {} morning, {} afternoon, {} evening".format(
					j+1, UnkMode(self.Months[i][j].CalendarMode).name,
					WeatherTypes(self.Months[i][j].MorningWeather).name,
					WeatherTypes(self.Months[i][j].AfternoonWeather).name,
					WeatherTypes(self.Months[i][j].EveningWeather).name,
				))
			print()

class DailyWeather(Serializable):

	def __init__(self):
		self.CalendarMode		= None
		self.MorningWeather		= None
		self.AfternoonWeather	= None
		self.EveningWeather		= None

	def __rw_hook__(self, rw):
		self.CalendarMode = rw.rw_uint8(self.CalendarMode)
		self.MorningWeather = rw.rw_uint8(self.MorningWeather)
		self.AfternoonWeather = rw.rw_uint8(self.AfternoonWeather)
		self.EveningWeather = rw.rw_uint8(self.EveningWeather)


class UnkMode(Enum):
	UnkMode0	= 0
	UnkMode1	= 1

