from enum import Enum
from .exbip.Serializable import Serializable
from .exbip.Descriptors import StreamHandlers


class Table(Serializable):

	def __init__(self):
		# variables
		self.TableStart = None
		self.Version = None
		self.Magic = None
		self.Endianness = None
		self.FileSize = None
		self.DataType = None
		self.DataCount = None
		self.DataOffsets = None

		self.Entries = None
		self.EntryPads = None
		self.Padding = None

	def update_offsets(self, filename):
		self.tobytes(filename=filename)

	def write_right(self, path, filename):
		self.update_offsets(filename=filename)
		# sometimes needs to be done twice, apparently, to make all the padding work....
		self.update_offsets(filename=filename)
		self.write(path, filename=filename)

	def pretty_print(self, indent_level=0):
		for i in range(self.DataCount):
			print("{}TABLE ENTRY {}:".format(" "*indent_level, i+1))
			if self.DataType:
				print("{}{}".format(" "*(indent_level+1), self.Entries[i].Data))
			else:
				self.Entries[i].pretty_print(indent_level=indent_level+1)
			print()

	def __rw_hook__(self, rw, filename):

		self.TableStart = rw.tell()

		rw.endianness = ">"
		self.Version = rw.rw_uint32(self.Version)
		self.Magic = rw.rw_string(self.Magic, 3)
		if rw.is_parselike: # writer
			self.Magic = self.Magic.decode()
		assert self.Magic == "FTD"
		self.Endianness = rw.rw_uint8(self.Endianness)
		if (self.Endianness == 0):
			rw.endianness = "<"

		self.FileSize = rw.rw_uint32(self.FileSize)
		self.DataType = rw.rw_int16(self.DataType)
		assert self.DataType == 0 or self.DataType == 1

		if rw.is_parselike:
			self.DataCount = len(self.Entries)
		self.DataCount = rw.rw_int16(self.DataCount)
		self.DataOffsets = rw.rw_uint32s(self.DataOffsets, self.DataCount)

		self.EntryPads = [None]*self.DataCount
		if rw.is_constructlike: # reader
			self.Entries = [None]*self.DataCount
		elif rw.is_parselike:
			self.DataOffsets = [None]*self.DataCount
		for i in range(self.DataCount):
			if rw.is_constructlike:
				paddingSize = self.DataOffsets[i] - rw.tell()
			elif rw.is_parselike:
				self.DataOffsets[i] = rw.tell()
				paddingSize = 0
				self.EntryPads[i] = b""
			self.EntryPads[i] = rw.rw_bytestring(self.EntryPads[i], paddingSize)
			assert self.EntryPads[i] == b"\x00"*paddingSize
			assert rw.tell() == self.DataOffsets[i]
			if self.DataType:
				self.Entries[i] = rw.rw_obj(self.Entries[i], FtdString)
			else:
				self.Entries[i] = rw.rw_obj(self.Entries[i], FtdList, filename)


class FtdString(Serializable):

	def __init__(self):
		self.Length = None
		self.Data = None
		self.UNK = [None]*1
		self.DUMMY = [None]*2

	def __rw_hook__(self, rw):

		if rw.is_parselike:
			self.Length = len(self.Data)
		self.Length = rw.rw_uint8(self.Length)

		self.UNK[0] = rw.rw_uint8(self.UNK[0])

		self.DUMMY[0] = rw.rw_uint8(self.DUMMY[0])
		assert self.DUMMY[0] == 0

		self.DUMMY[1] = rw.rw_uint8(self.DUMMY[1])
		assert self.DUMMY[1] == 0

		#self.Data = rw.rw_string(self.Data, self.Length, encoding="ascii")
		self.Data = rw.rw_bytestring(self.Data, self.Length)


class FtdList(Serializable):

	def __init__(self):
		self.DataSize = None
		self.EntryCount = None
		self.EntryType = None

		self.Entries = None

		self.UNK = [None]*1
		self.DUMMY = [None]*1

	def pretty_print(self, indent_level=0):
		for i in range(self.EntryCount):
			if FtdListType(self.EntryType) == FtdListType.DataEntries:
				print("{}({}) {}".format(" "*indent_level, i, self.Entries[i].stringify()))
			else:
				print("{}LIST ENTRY {}:".format(" "*indent_level, i+1))
				self.Entries[i].pretty_print(indent_level=indent_level+1)

	def __rw_hook__(self, rw, filename):

		self.DUMMY[0] = rw.rw_uint32(self.DUMMY[0])
		assert self.DUMMY[0] == 0

		self.DataSize = rw.rw_uint32(self.DataSize)

		if rw.is_parselike:
			self.EntryCount = len(self.Entries)
		self.EntryCount = rw.rw_uint32(self.EntryCount)
		self.EntryType = rw.rw_uint16(self.EntryType)
		assert self.EntryType == 0 or self.EntryType == 1

		self.UNK[0] = rw.rw_uint16(self.UNK[0])

		with rw.relative_origin():
			if self.EntryCount:
				if FtdListType(self.EntryType) == FtdListType.DataEntries:
					self.Entries = rw.rw_objs(self.Entries, FtdEntryTypes.__dict__.get(filename, FtdEntryTypes.Generic), self.EntryCount, self.DataSize//self.EntryCount)
				else:
					if rw.is_constructlike: # reader
						self.Entries = [None]*self.EntryCount
					for i in range(self.EntryCount):
						self.Entries[i] = rw.rw_obj(self.Entries[i], Table)
			if rw.is_parselike:
				self.DataSize = rw.tell()
			assert rw.tell() == self.DataSize


class FtdEntryTypes(Serializable):


	class Generic(Serializable):

		def __init__(self):
			self.Data = None

		def __rw_hook__(self, rw, datasize):
			self.Data = rw.rw_uint8s(self.Data, datasize)

		def stringify(self):
			return str(self.Data)


	class JustAString(Serializable):

		def __init__(self):
			self.Data = None

		def __rw_hook__(self, rw, datasize):
			if rw.is_parselike: # writer
				self.Data = (self.Data + ("\0"*datasize))[:datasize]
			self.Data = rw.rw_string(self.Data, datasize, encoding="ascii")
			if rw.is_parselike: # writer
				self.Data = self.Data.decode()
			if rw.is_constructlike: # reader
				self.Data = self.Data.replace("\0", "")

		def stringify(self):
			return self.Data


	class chatDataTable(Serializable):

		def __init__(self):
			self.IconId = None

		def __rw_hook__(self, rw, datasize):
			self.IconId = rw.rw_uint16(self.IconId)

		def stringify(self):
			return "Chat Icon: {}".format(IconTypes(self.IconId).name)


	class chatTitleName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.chatTitleName, self).__init__()


	class cmmMemberName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmmMemberName, self).__init__()


	class cmmEventNo(Serializable):

		def __init__(self):
			self.ConfidantId	= None
			self.EventType		= None
			self.PriorRank		= None
			self.MajorId		= None
			self.MinorId		= None
			self.RESERVE		= None
			self.Prerequisites	= None

		def __rw_hook__(self, rw, datasize):
			self.ConfidantId = rw.rw_uint16(self.ConfidantId)
			self.EventType = rw.rw_uint8(self.EventType)
			self.PriorRank = rw.rw_uint8(self.PriorRank)
			self.MajorId = rw.rw_uint16(self.MajorId)
			self.MinorId = rw.rw_uint16(self.MinorId)

			self.RESERVE = rw.rw_uint32(self.RESERVE)
			assert self.RESERVE == 0

			self.Prerequisites = rw.rw_uint32(self.Prerequisites)

		def stringify(self):
			return "Confidant ID: {}, Event Type: {}, Rank: {}, Event Major ID: {}, Event Minor ID: {}, Conditions: {}".format(
				self.ConfidantId, EventTypes(self.EventType).name, self.PriorRank, self.MajorId, self.MinorId, EventConditions(self.Prerequisites).name
			)
			#return ",\t".join("{}: {}".format(key, self.__dict__[key]) for key in self.__dict__)


	class FLDBGMCND(Serializable):

		def __init__(self):
			self.FieldMajorId	= None
			self.FieldMinorId	= None
			self.MinMonth		= None
			self.MinDay			= None
			self.MaxMonth		= None
			self.MaxDay			= None
			self.UnknownType	= None
			self.WeatherType	= None
			self.FieldType		= None
			self.RESERVE1		= None
			self.RESERVE2		= None
			self.BgmCueId		= None
			self.BitFlagSection	= None
			self.BitFlagId		= None

		def __rw_hook__(self, rw, datasize):
			self.FieldMajorId	= rw.rw_int16(self.FieldMajorId)
			self.FieldMinorId	= rw.rw_int16(self.FieldMinorId)
			self.MinMonth		= rw.rw_uint8(self.MinMonth)
			self.MinDay			= rw.rw_uint8(self.MinDay)
			self.MaxMonth		= rw.rw_uint8(self.MaxMonth)
			self.MaxDay			= rw.rw_uint8(self.MaxDay)
			self.UnknownType	= rw.rw_uint8(self.UnknownType)
			self.WeatherType	= rw.rw_uint8(self.WeatherType)
			self.FieldType		= rw.rw_uint8(self.FieldType)

			self.RESERVE1 = rw.rw_uint8(self.RESERVE1)
			assert self.RESERVE1 == 0xFF
			self.RESERVE2 = rw.rw_uint16(self.RESERVE2)
			assert self.RESERVE2 == 0

			self.BgmCueId		= rw.rw_int16(self.BgmCueId)
			self.BitFlagSection	= rw.rw_uint16(self.BitFlagSection)
			self.BitFlagId		= rw.rw_uint16(self.BitFlagId)

		def stringify(self):
			return "Field Major ID: {}, Field Minor ID: {}, Date Range: {:02d}/{:02d} - {:02d}/{:02d}, Unknown Type: {}, Weather Type: {}, Field Type: {}, BGM Cue ID: {}, BitFlag: {} + {}".format(
				self.FieldMajorId, self.FieldMinorId,
				self.MinMonth, self.MinDay, self.MaxMonth, self.MaxDay,
				UnknownTypes(self.UnknownType).name, WeatherTypes(self.WeatherType).name, FieldTypes(self.FieldType).name,
				self.BgmCueId, hex(self.BitFlagSection << 16), self.BitFlagId,
			)
			#return ",  ".join("{}: {}".format(key, self.__dict__[key]) for key in self.__dict__)


class FtdListType(Enum):
	DataEntries	= 0
	EmbeddedFtd	= 1


class IconTypes(Enum):
	Alibaba			= 0
	PhantomThieves	= 1
	Ryuji			= 2
	# in SCRIPTCHAT_1001
	UNUSED1			= 3
	Ann				= 4
	Yusuke			= 5
	Makoto			= 6
	Haru			= 7
	Futaba			= 8
	Akechi			= 9
	Kasumi			= 10
	# UNUSED RANGE
	Sojiro			= 16
	Chihaya			= 17
	# UNUSED RANGE
	Iwai			= 20
	Takemi			= 21
	Kawakami		= 22
	Ohya			= 23
	Shinya			= 24
	Hifumi			= 25
	Mishima			= 26
	Yoshida			= 27
	# in SCRIPTCHAT_840
	SaeUnused		= 28
	# UNUSED RANGE
	Maruki			= 31
	Sumire			= 32
	# UNUSED RANGE
	Nanami			= 43
	OreNoBeko		= 44
	Hanasaki		= 45
	LalaEscargot	= 46
	Becky			= 47
	# in SCRIPTCHAT_984
	RyujiYusuke		= 48
	# in SCRIPTCHAT_323
	UNK4			= 49


class EventTypes(Enum):
	BetweenRanks	= 1
	RankUp			= 2
	ConfidantStart	= 3
	Unk1			= 4
	Unk2			= 5
	RankMax			= 6
	Unk3			= 7
	Unk4			= 8


class EventConditions(Enum):
	Points	= 0
	Auto	= 1
	Date	= 2


class UnknownTypes(Enum):
	Unk1	= 1
	Unk2	= 2
	ANY		= 255


class WeatherTypes(Enum):
	Sunny			= 0
	Rain			= 1
	Sunny2			= 2
	Snow			= 3
	RainySeason		= 4
	TyphoonWarning	= 5
	PollenWarning	= 6
	PollenWarning2	= 7
	TorrentialRain	= 8
	HeatWave		= 9
	FluSeason		= 10
	FluSeason2		= 11
	ANY				= 255


class FieldTypes(Enum):
	Overworld	= 0
	Metaverse	= 1
	ANY			= 255
