from enum import Enum
from .exbip.Serializable import Serializable
from .exbip.Descriptors import StreamHandlers


class Table(Serializable):

	def __init__(self):
		self.Version		= None
		self.Magic			= None
		self.Endianness		= None
		self.FileSize		= None
		self.DataType		= None
		self.DataCount		= None
		self.DataOffsets	= None

		self.Entries		= None
		self.EntryPads		= None
		self.Padding		= None

	def update_offsets(self, filename):
		self.tobytes(filename=filename)
		# sometimes needs to be done twice, apparently, to make all the padding work....
		self.tobytes(filename=filename)

	def write_right(self, path, filename):
		self.update_offsets(filename=filename)
		self.write(path, filename=filename)

	def pretty_print(self, indent_level=0):
		for i in range(self.DataCount):
			print("{}TABLE ENTRY {}:".format(" "*indent_level, i))
			if self.DataType:
				print("{}{}".format(" "*(indent_level+1), self.Entries[i].Data))
			else:
				self.Entries[i].pretty_print(indent_level=indent_level+1)
			print()

	def __rw_hook__(self, rw, filename):

		rw.endianness = ">"
		with rw.relative_origin():

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

			# some tables pad when rw.tell % 8 == 0... others don't. cool. cool cool cool.
			paddingSize = (8 - (rw.tell() % 8)) if (rw.tell() % 8) else 0
			if rw.is_parselike:
				self.Padding = b"\x00"*paddingSize
			self.Padding = rw.rw_bytestring(self.Padding, paddingSize)
			assert self.Padding == b"\x00"*paddingSize
			if rw.is_parselike:
				self.FileSize = rw.tell()
			# the FileSize stuff is just a mess...
			# I suspect it's just not actually used in the readers and thus not inherently updated
			#assert rw.tell() == self.FileSize or rw.tell() == self.FileSize - 8 or rw.tell() == self.FileSize + 8

		"""failed = False
		try:
			rw.assert_eof()
		except Exception:
			print("Failed to read file!")
			remainder = rw._bytestream.peek()
			print(len(remainder), remainder)"""


class FtdString(Serializable):

	def __init__(self):
		self.Length = None
		self.Data = None
		self.UNK = None
		self.RESERVE = None

	def __rw_hook__(self, rw):

		if rw.is_parselike:
			self.Length = len(self.Data)
		self.Length = rw.rw_uint8(self.Length)

		self.UNK = rw.rw_uint8(self.UNK)
		assert self.UNK == 1

		self.RESERVE = rw.rw_uint16(self.RESERVE)
		assert self.RESERVE == 0

		#self.Data = rw.rw_string(self.Data, self.Length, encoding="ascii")
		self.Data = rw.rw_bytestring(self.Data, self.Length)


class FtdList(Serializable):

	def __init__(self):
		self.RESERVE1 = None

		self.DataSize = None
		self.EntryCount = None
		self.EntryType = None

		self.RESERVE2 = None

		self.Entries = None

	def pretty_print(self, indent_level=0):
		for i in range(self.EntryCount):
			if FtdListType(self.EntryType) == FtdListType.DataEntries:
				print("{}({}) {}".format(" "*indent_level, i, self.Entries[i].stringify()))
			else:
				print("{}LIST ENTRY {}:".format(" "*indent_level, i))
				self.Entries[i].pretty_print(indent_level=indent_level+1)

	def __rw_hook__(self, rw, filename):

		self.RESERVE1 = rw.rw_uint32(self.RESERVE1)
		assert self.RESERVE1 == 0

		self.DataSize = rw.rw_uint32(self.DataSize)

		if rw.is_parselike:
			self.EntryCount = len(self.Entries)
		self.EntryCount = rw.rw_uint32(self.EntryCount)
		self.EntryType = rw.rw_uint16(self.EntryType)
		assert self.EntryType == 0 or self.EntryType == 1

		self.RESERVE2 = rw.rw_uint16(self.RESERVE2)
		assert self.RESERVE2 == 0

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


	class cmmMemberName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmmMemberName, self).__init__()


	class cmmPC_PARAM_Name(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmmPC_PARAM_Name, self).__init__()


	class DATENCOUNTPACK(Serializable):

		def __init__(self):
			self.DngId					= None
			self.RESERVE1				= None
			self.AmbushEncounterIds		= None
			self.NormalEncounters		= None
			self.NormalPinchEncounters	= None
			self.Unk1Encounters			= None
			self.Unk2Encounters			= None
			self.StrongEncounters		= None
			self.StrongPinchEncounters	= None
			self.TreasureEncounters		= None
			self.ReaperEncounter		= None
			self.RESERVE2				= None

		def __rw_hook__(self, rw, datasize):
			self.DngId		= rw.rw_uint8(self.DngId)
			self.RESERVE1	= rw.rw_uint8s(self.RESERVE1, 7)
			assert all(elem == 0 for elem in self.RESERVE1)

			self.AmbushEncounterIds		= rw.rw_uint16s(self.AmbushEncounterIds, 8)
			self.NormalEncounters		= rw.rw_objs(self.NormalEncounters, ENC, 13)
			self.NormalPinchEncounters	= rw.rw_objs(self.NormalPinchEncounters, ENC, 5)
			self.Unk1Encounters			= rw.rw_objs(self.Unk1Encounters, ENC, 5)
			self.Unk2Encounters			= rw.rw_objs(self.Unk2Encounters, ENC, 5)
			self.StrongEncounters		= rw.rw_objs(self.StrongEncounters, ENC, 5)
			self.StrongPinchEncounters	= rw.rw_objs(self.StrongPinchEncounters, ENC, 5)
			self.TreasureEncounters		= rw.rw_objs(self.TreasureEncounters, ENC, 5)

			self.ReaperEncounter		= rw.rw_obj(self.ReaperEncounter, ENC)

			assert sum(enc.Weight for enc in self.NormalEncounters) in {0, 100}
			assert sum(enc.Weight for enc in self.NormalPinchEncounters) in {0, 100}
			assert sum(enc.Weight for enc in self.Unk1Encounters) in {0, 100}
			assert sum(enc.Weight for enc in self.Unk2Encounters) in {0, 100}
			assert sum(enc.Weight for enc in self.StrongEncounters) in {0, 100}
			assert sum(enc.Weight for enc in self.StrongPinchEncounters) in {0, 100}
			assert sum(enc.Weight for enc in self.TreasureEncounters) in {0, 100}

			self.RESERVE2				= rw.rw_uint32(self.RESERVE2)
			assert self.RESERVE2 == 0

		def stringify(self):
			lines = list()
			lines.append(f"DNG ID: {self.DngId}")
			if any(encId != 0 for encId in self.AmbushEncounterIds):
				lines.append("    Ambush Encounter IDs: {}".format(", ".join(str(encId) for encId in self.AmbushEncounterIds if encId != 0)))
			if any(enc.EncounterId != 0 for enc in self.NormalEncounters):
				lines.append("    Normal Encounters:")
				for i in range(len(self.NormalEncounters)):
					if self.NormalEncounters[i].EncounterId != 0:
						lines.append("      ({}) {}".format(i+1, self.NormalEncounters[i].stringify()))
			if any(enc.EncounterId != 0 for enc in self.NormalPinchEncounters):
				lines.append("    Normal Pinch Encounters:")
				for i in range(len(self.NormalPinchEncounters)):
					if self.NormalPinchEncounters[i].EncounterId != 0:
						lines.append("      ({}) {}".format(i+1, self.NormalPinchEncounters[i].stringify()))
			if any(enc.EncounterId != 0 for enc in self.Unk1Encounters):
				lines.append("    UNK #1 Encounters:")
				for i in range(len(self.Unk1Encounters)):
					if self.Unk1Encounters[i].EncounterId != 0:
						lines.append("      ({}) {}".format(i+1, self.Unk1Encounters[i].stringify()))
			if any(enc.EncounterId != 0 for enc in self.Unk2Encounters):
				lines.append("    UNK #2 Encounters:")
				for i in range(len(self.Unk2Encounters)):
					if self.Unk2Encounters[i].EncounterId != 0:
						lines.append("      ({}) {}".format(i+1, self.Unk2Encounters[i].stringify()))
			if any(enc.EncounterId != 0 for enc in self.StrongEncounters):
				lines.append("    Strong Encounters:")
				for i in range(len(self.StrongEncounters)):
					if self.StrongEncounters[i].EncounterId != 0:
						lines.append("      ({}) {}".format(i+1, self.StrongEncounters[i].stringify()))
			if any(enc.EncounterId != 0 for enc in self.StrongPinchEncounters):
				lines.append("    Strong Pinch Encounters:")
				for i in range(len(self.StrongPinchEncounters)):
					if self.StrongPinchEncounters[i].EncounterId != 0:
						lines.append("      ({}) {}".format(i+1, self.StrongPinchEncounters[i].stringify()))
			if any(enc.EncounterId != 0 for enc in self.TreasureEncounters):
				lines.append("    Treasure Encounters:")
				for i in range(len(self.TreasureEncounters)):
					if self.TreasureEncounters[i].EncounterId != 0:
						lines.append("      ({}) {}".format(i+1, self.TreasureEncounters[i].stringify()))
			lines.append("    Reaper Encounter: {}".format(self.ReaperEncounter.stringify()))
			return "\n".join(lines)


	class FLDACTMOVELEN(Serializable):

		def __init__(self):
			self.MoveLength = None

		def __rw_hook__(self, rw, datasize):
			self.MoveLength = rw.rw_int16(self.MoveLength)

		def stringify(self):
			return f"Move Length: {self.MoveLength}"


	class FLDADDACTANIM(Serializable):

		def __init__(self):
			self.FieldObjMajorId	= None
			self.FieldObjMinorId	= None
			self.FieldAnimGapId		= None
			self.UNK1				= None
			self.UNK2				= None
			self.UNK3				= None
			self.UNK4				= None
			self.UNK5				= None
			self.UNK6				= None
			self.UNK7				= None
			self.UNK8				= None
			self.UNK9				= None

		def __rw_hook__(self, rw, datasize):
			self.FieldObjMajorId	= rw.rw_int16(self.FieldObjMajorId)
			self.FieldObjMinorId	= rw.rw_int16(self.FieldObjMinorId)
			self.FieldAnimGapId		= rw.rw_uint8(self.FieldAnimGapId)
			self.UNK1				= rw.rw_uint8(self.UNK1)
			self.UNK2				= rw.rw_int16(self.UNK2)
			self.UNK3				= rw.rw_int16(self.UNK3)
			self.UNK4				= rw.rw_int16(self.UNK4)
			self.UNK5				= rw.rw_int32(self.UNK5)
			self.UNK6				= rw.rw_int16(self.UNK6)
			self.UNK7				= rw.rw_int16(self.UNK7)
			self.UNK8				= rw.rw_int32(self.UNK8)
			self.UNK9				= rw.rw_int16(self.UNK9)

		def stringify(self):
			return "FieldObj Major ID: {}, FieldObj Minor ID: {}, FieldAnim GAP ID: {}, UNK 1: {}, UNK 2: {}, UNK 3: {}, UNK 4: {}, UNK 5: {}, UNK 6: {}, UNK 7: {}, UNK 8: {}, UNK 9: {}".format(
				self.FieldObjMajorId, self.FieldObjMinorId,
				self.FieldAnimGapId, self.UNK1, self.UNK2, self.UNK3, self.UNK4,
				self.UNK5, self.UNK6, self.UNK7, self.UNK8, self.UNK9,
			)


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


	class FLDDNGPACK(Serializable):

		def __init__(self):
			self.EncountPackEntry	= None
			self.ObjFlagEntry		= None
			self.TboxRndEntry		= None
			self.RESERVE			= None

		def __rw_hook__(self, rw, datasize):
			self.EncountPackEntry	= rw.rw_uint16(self.EncountPackEntry)
			self.ObjFlagEntry		= rw.rw_uint16(self.ObjFlagEntry)
			self.TboxRndEntry		= rw.rw_uint16(self.TboxRndEntry)

			self.RESERVE = rw.rw_bytestring(self.RESERVE, 10)
			assert self.RESERVE == b"\0"*10

		def stringify(self):
			return "Encounter Pack Entry: {}, Object Flag Entry: {}, Treasurebox Entry: {}".format(
				self.EncountPackEntry, self.ObjFlagEntry, self.TboxRndEntry
			)


	class FLDFOOTSTEPCND(Serializable):

		def __init__(self):
			self.FieldMajorId	= None
			self.FieldMinorId	= None
			self.FootstepType	= None
			self.RoomId			= None
			self.RESERVE		= None

		def __rw_hook__(self, rw, datasize):
			self.FieldMajorId	= rw.rw_uint16(self.FieldMajorId)
			self.FieldMinorId	= rw.rw_uint16(self.FieldMinorId)
			self.FootstepType	= rw.rw_uint16(self.FootstepType)
			self.RoomId			= rw.rw_uint8(self.RoomId)

			self.RESERVE = rw.rw_uint8(self.RESERVE)
			assert self.RESERVE == 0

		def stringify(self):
			return "Field Major ID: {}, Field Minor ID: {}, Footstep Type {}, Room ID: {}".format(
				#self.FieldMajorId, self.FieldMinorId, self.FootstepType, self.RESERVE,
				self.FieldMajorId, self.FieldMinorId, FootstepTypes(self.FootstepType).name, self.RoomId,
		)


	class FLDPLACENO(Serializable):

		def __init__(self):
			self.FieldNameIndex = None
			self.Room1NameIndex = None
			self.Room2NameIndex = None
			self.Room3NameIndex = None

		def __rw_hook__(self, rw, datasize):
			self.FieldNameIndex = rw.rw_uint16(self.FieldNameIndex)
			self.Room1NameIndex = rw.rw_uint16(self.Room1NameIndex)
			self.Room2NameIndex = rw.rw_uint16(self.Room2NameIndex)
			self.Room3NameIndex = rw.rw_uint16(self.Room2NameIndex)

		def stringify(self):
			return "Field Name Index: {}, Room 1 Name Index: {}, Room 2 Name Index: {}, Room 3 Name Index: {}".format(
				self.FieldNameIndex, self.Room1NameIndex, self.Room2NameIndex, self.Room3NameIndex
			)


	class FLDPLAYERSPEED(Serializable):

		def __init__(self):
			self.FieldMajorId		= None
			self.FieldMinorId		= None
			self.WalkSpeed			= None
			self.RunSpeed			= None
			self.AccelFrames		= None
			self.DecelFrames		= None
			self.StaticTurnFrames	= None
			self.RESERVE			= None

		def __rw_hook__(self, rw, datasize):
			self.FieldMajorId		= rw.rw_int16(self.FieldMajorId)
			self.FieldMinorId		= rw.rw_int16(self.FieldMinorId)
			self.WalkSpeed			= rw.rw_int16(self.WalkSpeed)
			self.RunSpeed			= rw.rw_int16(self.RunSpeed)
			self.AccelFrames		= rw.rw_uint8(self.AccelFrames)
			self.DecelFrames		= rw.rw_uint8(self.DecelFrames)
			self.StaticTurnFrames	= rw.rw_uint8(self.StaticTurnFrames)

			self.RESERVE = rw.rw_uint8(self.RESERVE)
			assert self.RESERVE == 0

		def stringify(self):
			return "Field Major ID: {}, Field Minor ID: {}, Walk Speed: {}, Run Speed: {}, Accel Frames: {}, Decel Frames: {}, Static Turn Frames: {}".format(
				self.FieldMajorId, self.FieldMinorId,
				self.WalkSpeed, self.RunSpeed,
				self.AccelFrames, self.DecelFrames, self.StaticTurnFrames,
			)


	class FLDSYMMODELNO(Serializable):

		def __init__(self):
			self.ShadowOffset = None


		def __rw_hook__(self, rw, datasize):
			self.ShadowOffset = rw.rw_uint16(self.ShadowOffset)

		def stringify(self):
			return "Shadow Offset: {}".format(
				self.ShadowOffset,
			)


	class FLDSYMMODELSCL(Serializable):

		def __init__(self):
			self.ShadowID	= None
			self.ModelScale	= None


		def __rw_hook__(self, rw, datasize):
			self.ShadowID	= rw.rw_uint16(self.ShadowID)
			self.ModelScale	= rw.rw_uint16(self.ModelScale)

		def stringify(self):
			return "Shadow ID: {}, Model Scale: {}".format(
				self.ShadowID, self.ModelScale,
			)


class ENC(Serializable):

	def __init__(self):
		self.EncounterId	= None
		self.Weight			= None
		self.RESERVE		= None

	def __rw_hook__(self, rw):
		self.EncounterId	= rw.rw_uint16(self.EncounterId)
		self.Weight			= rw.rw_uint8(self.Weight)

		self.RESERVE = rw.rw_uint8(self.RESERVE)
		assert self.RESERVE == 0

	def stringify(self):
		return "ID = {} ({}%)".format(
			self.EncounterId, self.Weight
		)


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


class FootstepTypes(Enum):
	Silence			= 0
	Wood			= 1
	Stone			= 2
	# not actually used
	Grass			= 3
	Soil			= 4
	Carpet			= 5
	Metal			= 6
	Bare			= 7
	# not actually used
	Crawl			= 8
	Sand			= 9
	# not actually used
	Wet				= 10
	# not actually used
	Creak			= 11
	# not actually used
	WoodAndCreak	= 12
	Thin_Metal		= 14
