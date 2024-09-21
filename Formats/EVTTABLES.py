from enum import Enum
from .exbip.Serializable import Serializable
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


class EvtTable(Serializable):

	def __init__(self):
		self.Entries = list()

	def update_offsets(self):
		self.tobytes()

	def write_right(self, path):
		self.update_offsets()
		self.write(path)

	def __rw_hook__(self, rw, filename):
		with EndiannessManager(rw, ">"):
			entriesSoFar = 0
			while (rw.is_constructlike and rw.peek_bytestream(1)) or (rw.is_parselike and entriesSoFar < len(self.Entries)):
				if rw.is_constructlike:
					self.Entries.append(None)
				self.Entries[entriesSoFar] = rw.rw_obj(self.Entries, EvtTableEntryTypes.__dict__[filename])
				entriesSoFar += 1

	def pretty_print(self):
		for i in range(len(self.Entries)):
			print("({}) {}".format(i, self.Entries[i].stringify()))


class EvtTableEntryTypes:


	class EVTDATETABLE(Serializable):

		def __init__(self):
			self.EventMajorId	= 0
			self.EventMinorId	= 0
			self.Month			= 0
			self.Day			= 0
			self.Time			= 0
			self.RESERVE		= 0

		def __rw_hook__(self, rw):
			self.EventMajorId	= rw.rw_uint16(self.EventMajorId)
			self.EventMinorId	= rw.rw_uint16(self.EventMinorId)
			self.Month			= rw.rw_uint8(self.Month)
			self.Day			= rw.rw_uint8(self.Day)
			self.Time			= rw.rw_uint8(self.Time)

			self.RESERVE = rw.rw_uint8(self.RESERVE)
			assert self.RESERVE == 0

		def stringify(self):
			return "E{:03d}_{:03d}: {}/{} @ {}".format(
				self.EventMajorId, self.EventMinorId,
				self.Month, self.Day, TimesOfDay(self.Time).name,
			)


	class EVTDATEOFFTABLE(Serializable):

		def __init__(self):
			self.EventMajorId	= 0
			self.EventMinorId	= 0

		def __rw_hook__(self, rw):
			self.EventMajorId	= rw.rw_uint16(self.EventMajorId)
			self.EventMinorId	= rw.rw_uint16(self.EventMinorId)

		def stringify(self):
			return "E{:03d}_{:03d}".format(self.EventMajorId, self.EventMinorId)


	class EVTDDDECOTABLE(Serializable):

		def __init__(self):
			self.EventMajorId	= 0
			self.EventMinorId	= 0
			self.RESERVE		= 0

		def __rw_hook__(self, rw):
			self.EventMajorId	= rw.rw_uint16(self.EventMajorId)
			self.EventMinorId	= rw.rw_uint16(self.EventMinorId)

			self.RESERVE = rw.rw_uint32(self.RESERVE)
			assert self.RESERVE == 0

		def stringify(self):
			return "E{:03d}_{:03d}".format(self.EventMajorId, self.EventMinorId)


	class EVTFADEOUTTABLE(Serializable):

		def __init__(self):
			self.EventMajorId	= 0
			self.EventMinorId	= 0
			self.FadeId			= 0
			self.RESERVE		= 0

		def __rw_hook__(self, rw):
			self.EventMajorId	= rw.rw_uint16(self.EventMajorId)
			self.EventMinorId	= rw.rw_uint16(self.EventMinorId)
			self.FadeId			= rw.rw_uint16(self.FadeId)

			self.RESERVE = rw.rw_uint16(self.RESERVE)
			assert self.RESERVE == 0

		# TODO: make an enum for FadeTypes
		def stringify(self):
			return "E{:03d}_{:03d}: {}".format(self.EventMajorId, self.EventMinorId, self.FadeId)


class TimesOfDay(Enum):
	EarlyMorning	= 0
	Morning			= 1
	Daytime			= 2
	Lunchtime		= 3
	Afternoon		= 4
	AfterSchool		= 5
	Evening			= 6
	LateNight		= 7
	InBetween		= 255  # i guess...
