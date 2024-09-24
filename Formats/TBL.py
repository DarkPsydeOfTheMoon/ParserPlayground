from enum import Enum
from .exbip.Serializable import Serializable
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


class BattleTable(Serializable):

	def __init__(self):
		self.Endianness	= None

		self.FileSizes	= list()
		self.Entries	= list()
		self.Paddings	= list()

	def update_offsets(self):
		self.tobytes()

	def write_right(self, path):
		self.update_offsets()
		self.write(path)

	def __rw_hook__(self, rw, filename):

		if rw.is_constructlike:
			testFileSize = None
			testFileSize = rw.rw_uint32(testFileSize)
			rw.seek(0, 2)
			if testFileSize > rw.tell():
				self.Endianness = ">"
			else:
				self.Endianness = "<"
			rw.seek(0, 0)

		with EndiannessManager(rw, self.Endianness):
			entriesSoFar = 0
			while (rw.is_constructlike and rw.peek_bytestream(1)) or (rw.is_parselike and entriesSoFar < len(self.Entries)):
				if rw.is_constructlike:
					self.FileSizes.append(None)
					self.Entries.append(None)
					self.Paddings.append(None)
				self.FileSizes[entriesSoFar] = rw.rw_uint32(self.FileSizes[entriesSoFar])
				print(filename, self.FileSizes[entriesSoFar])
				#self.Entries[entriesSoFar] = rw.rw_bytestring(self.Entries[entriesSoFar], self.FileSizes[entriesSoFar])
				entryBytes = None
				entryBytes = rw.rw_bytestring(entryBytes, self.FileSizes[entriesSoFar])
				#try:
				segmentType = TblTypes.__dict__[filename].SEGMENTS[entriesSoFar]
				self.Entries[entriesSoFar] = segmentType()
				self.Entries[entriesSoFar].frombytes(entryBytes, endianness=self.Endianness)
				self.pretty_print()
				#except Exception:
				#	self.Entries[entriesSoFar] = entryBytes
				paddingSize = 16 - (rw.tell() % 16)
				self.Paddings[entriesSoFar] = rw.rw_bytestring(self.Paddings[entriesSoFar], paddingSize)
				assert self.Paddings[entriesSoFar] == b"\0"*paddingSize
				entriesSoFar += 1

		failed = False
		try: 
			rw.assert_eof()
		except Exception:
			print("Failed to read file!")
			remainder = rw._bytestream.peek()
			print(len(remainder), remainder)

	def pretty_print(self):
		for i in range(len(self.Entries)):
			print("SEGMENT {}:".format(i))
			print(self.Entries[i].stringify())
			print()


class TblTypes:


	class ENCOUNT:

		class EncounterMain(Serializable):

			def __init__(self):
				self.Encounters = None

			def __rw_hook__(self, rw, endianness):
				with EndiannessManager(rw, endianness):
					self.Encounters = rw.rw_objs(self.Encounters, EncounterEntry, 1000)
				rw.assert_eof()

			def stringify(self):
				lines = list()
				for i in range(1000):
					lines.append("  {:d} (E{:03X}):".format(i, i))
					lines.append(self.Encounters[i].stringify())
				return "\n".join(lines)

		class EncounterUnk1(Serializable):

			def __init__(self):
				self.UNK = None

			def __rw_hook__(self, rw, endianness):
				with EndiannessManager(rw, endianness):
					#self.UNK = rw.rw_objs(self.UNK, UnkEntry, 125)
					#self.UNK = rw.rw_objs(self.UNK, UnkEntry, 250)
					#self.UNK = rw.rw_objs(self.UNK, UnkEntry, 500)
					self.UNK = rw.rw_objs(self.UNK, UnkEntry, 1000)
				rw.assert_eof()

			def stringify(self):
				#return "\n".join(str(unk.Data) for unk in self.UNK)
				lines = list()
				for i in range(1000):
					lines.append("  {:d} (E{:03X}): {}".format(i, i, str(self.UNK[i].Data)))
				return "\n".join(lines)

		class EncounterUnk2(Serializable):

			def __init__(self):
				self.UNK = None

			def __rw_hook__(self, rw, endianness):
				with EndiannessManager(rw, endianness):
					#self.UNK = rw.rw_objs(self.UNK, UnkEntry, 41)
					#self.UNK = rw.rw_objs(self.UNK, UnkEntry, 82)
					#self.UNK = rw.rw_objs(self.UNK, UnkEntry, 164)
					self.UNK = rw.rw_objs(self.UNK, UnkEntry, 328)
				rw.assert_eof()

			def stringify(self):
				return "\n".join(str(unk.Data) for unk in self.UNK)

		SEGMENTS = [EncounterMain, EncounterUnk1, EncounterUnk2]


class EncounterEntry(Serializable):

	def __init__(self):
		self.BitFlags		= None
		self.UNK1			= None
		self.UNK2			= None
		self.BattleUnitIds	= None
		self.FieldId		= None
		self.RoomId			= None
		self.MusicId		= None
		self.UNK3			= None

	def __rw_hook__(self, rw):
		self.BitFlags		= rw.rw_uint32(self.BitFlags)
		self.UNK1			= rw.rw_uint16(self.UNK1)
		self.UNK2			= rw.rw_uint16(self.UNK2)
		self.BattleUnitIds	= rw.rw_uint16s(self.BattleUnitIds, 5)
		self.FieldId		= rw.rw_uint16(self.FieldId)
		self.RoomId			= rw.rw_uint16(self.RoomId)
		self.MusicId		= rw.rw_uint16(self.MusicId)
		self.UNK3			= rw.rw_uint16s(self.UNK3, 10)
		#print("#####", self.__dict__)

	def stringify(self):
		lines = list()
		lines.append("    F{:03d}_{:03d}".format(self.FieldId, self.RoomId))
		if any(unit != 0 for unit in self.BattleUnitIds):
			lines.append("    Battle Unit IDs: {}".format(", ".join(str(unit) for unit in self.BattleUnitIds if unit != 0)))
		lines.append("    BitFlags: {:032b}".format(self.BitFlags))
		lines.append("    Music ID: {}".format(self.MusicId))
		lines.append("    UNK1: {}, UNK2: {}".format(self.UNK1, self.UNK2))
		lines.append("    UNK3: {}".format(", ".join(str(unk) for unk in self.UNK3)))
		return "\n".join(lines)


class UnkEntry(Serializable):

	def __init__(self):
		self.Data = None

	def __rw_hook__(self, rw):
		#self.Data = rw.rw_uint8s(self.Data, 64)
		#self.Data = rw.rw_uint8s(self.Data, 32)
		#self.Data = rw.rw_uint8s(self.Data, 16)
		self.Data = rw.rw_uint8s(self.Data, 8)


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
