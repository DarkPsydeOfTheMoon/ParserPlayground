from enum import Enum
from .exbip.Serializable import Serializable
from .exbip.Descriptors import StreamHandlers
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


class Table(Serializable):

	def __init__(self):
		self.Version		= None
		self.Magic			= None
		self.Endianness		= None
		self.FileSize		= None
		self.DataType		= None
		self.DataCount		= None
		self.DataOffsets	= None

		self.UNK1			= None
		self.UNK2			= None
		self.RESERVE		= None

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

		#print(rw.tell(), rw.peek_bytestream(256))

		if rw.is_constructlike:
			magic_peek = rw.peek_bytestream(8)[-4:]
			#0DT. = <; .TD0 = >
			if magic_peek.startswith(b"0DT"):
				self.Endianness = "<"
			elif magic_peek.endswith(b"TD0"):
				self.Endianness = ">"
			else:
				raise ValueError(f"Unexpected magic string: {self.Magic}")

		with EndiannessManager(rw, self.Endianness), rw.relative_origin():

			self.Version = rw.rw_uint32(self.Version)
			self.Magic = rw.rw_string(self.Magic, 4, encoding="ascii")
			if rw.is_parselike: # writer
				self.Magic = self.Magic.decode()
			assert self.Magic.startswith("0DT") or self.Magic.endswith("TD0")
			self.FileSize = rw.rw_uint32(self.FileSize)

			if self.Endianness == ">":
				self.DataType = rw.rw_int16(self.DataType)
				assert self.DataType == 0 or self.DataType == 1
				if rw.is_parselike:
					self.DataCount = len(self.Entries) if self.Entries else 0
				self.DataCount = rw.rw_int16(self.DataCount)
				self.DataOffsets = rw.rw_uint32s(self.DataOffsets, self.DataCount)
			else:
				# idk about these ones, bois
				self.UNK1 = rw.rw_uint32(self.UNK1)
				assert self.UNK1 == 1
				self.UNK2 = rw.rw_uint32(self.UNK2)
				assert self.UNK2 == 32
				self.RESERVE = rw.rw_bytestring(self.RESERVE, 12)
				assert self.RESERVE == b"\0"*12
				self.DataType = 0
				self.DataCount = 1
				self.DataOffsets = [rw.tell()]

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

			# for some reason the ttr tables repeat the header (0-16) at the footer.................
			if rw.is_parselike and self.Endianness == "<":
				self.Version = rw.rw_uint32(self.Version)
				self.Magic = rw.rw_string(self.Magic, 4, encoding="ascii")
				if rw.is_parselike: # writer
					self.Magic = self.Magic.decode()
				assert self.Magic.startswith("0DT") or self.Magic.endswith("TD0")
				self.FileSize = rw.rw_uint32(self.FileSize)
				self.UNK1 = rw.rw_uint32(self.UNK1)

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

		if rw.is_parselike: # writer
			self.Data = (self.Data + (b"\0"*self.Length))[:self.Length]
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
		self.Padding = None

	def pretty_print(self, indent_level=0):
		if FtdListTypes(self.EntryType) == FtdListTypes.DataEntries:
			for i in range(self.EntryCount):
				print("{}({}) {}".format(" "*indent_level, i, self.Entries[i].stringify()))
		else:
			self.Entries.pretty_print(indent_level=indent_level+1)

	def __rw_hook__(self, rw, filename):

		self.RESERVE1 = rw.rw_uint32(self.RESERVE1)
		assert self.RESERVE1 == 0

		self.DataSize = rw.rw_uint32(self.DataSize)

		if rw.is_parselike:
			if FtdListTypes(self.EntryType) == FtdListTypes.DataEntries:
				self.EntryCount = len(self.Entries) if self.Entries else 0
			else:
				self.EntryCount = self.Entries.DataCount
		self.EntryCount = rw.rw_uint32(self.EntryCount)
		self.EntryType = rw.rw_uint16(self.EntryType)
		assert self.EntryType == 0 or self.EntryType == 1

		self.RESERVE2 = rw.rw_uint16(self.RESERVE2)
		assert self.RESERVE2 == 0

		with rw.relative_origin():
			if self.EntryCount:
				if FtdListTypes(self.EntryType) == FtdListTypes.DataEntries:
					self.Entries = rw.rw_objs(self.Entries, FtdEntryTypes.__dict__.get(filename, FtdEntryTypes.Generic), self.EntryCount, self.DataSize//self.EntryCount)
				else:
					self.Entries = rw.rw_obj(self.Entries, Table, filename)
					assert self.Entries.DataCount == self.EntryCount
					paddingSize = rw.tell() % 16
					if rw.is_parselike:
						self.Padding = b"\0"*paddingSize
						self.DataSize = rw.tell() + paddingSize
					assert paddingSize == self.DataSize - rw.tell()
					self.Padding = rw.rw_bytestring(self.Padding, paddingSize)
					assert self.Padding == b"\0"*paddingSize
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
				#self.Data = (self.Data + ("\0"*datasize))[:datasize]
				self.Data = (self.Data + (b"\0"*datasize))[:datasize]
			#self.Data = rw.rw_string(self.Data, datasize, encoding="ascii")
			self.Data = rw.rw_bytestring(self.Data, datasize)
			"""if rw.is_parselike: # writer
				self.Data = self.Data.decode()
			if rw.is_constructlike: # reader
				#self.Data = self.Data.replace("\0", "")
				self.Data = self.Data.replace(b"\0", b"")"""

		def stringify(self):
			return self.Data.replace(b"\0", b"")


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
			self.ConfidantId	= rw.rw_uint16(self.ConfidantId)
			self.EventType		= rw.rw_uint8(self.EventType)
			self.PriorRank		= rw.rw_uint8(self.PriorRank)
			self.MajorId		= rw.rw_uint16(self.MajorId)
			self.MinorId		= rw.rw_uint16(self.MinorId)

			self.RESERVE = rw.rw_uint32(self.RESERVE)
			assert self.RESERVE == 0

			self.Prerequisites = rw.rw_uint32(self.Prerequisites)

		def stringify(self):
			return "Confidant ID: {}, Event Type: {}, Rank: {}, Event Major ID: {}, Event Minor ID: {}, Conditions: {}".format(
				self.ConfidantId, EventTypes(self.EventType).name, self.PriorRank, self.MajorId, self.MinorId, EventConditions(self.Prerequisites).name
			)


	class cmmFormat(Serializable):

		def __init__(self):
			self.ConfidantListIndex		= None
			self.UNK1					= None
			self.ConfidantId			= None
			self.UNK2					= None
			self.RESERVE2				= None
			self.RESERVE3				= None
			self.PointsForRank			= None
			self.RESERVE4				= None
			self.ConfidantTableIndex	= None
			self.Padding				= None

		def __rw_hook__(self, rw, datasize):
			self.ConfidantListIndex		= rw.rw_int32(self.ConfidantListIndex)
			self.UNK1					= rw.rw_int32(self.UNK1)
			self.ConfidantId			= rw.rw_uint8(self.ConfidantId)
			self.UNK2					= rw.rw_uint8(self.UNK2)

			self.RESERVE2 = rw.rw_uint16(self.RESERVE2)
			assert self.RESERVE2 == 0
			self.RESERVE3 = rw.rw_int32(self.RESERVE3)
			assert self.RESERVE3 == 0

			self.PointsForRank			= rw.rw_uint16s(self.PointsForRank, 10)

			self.RESERVE4 = rw.rw_int32(self.RESERVE4)
			assert self.RESERVE4 == 0
			#print(self.RESERVE1, self.RESERVE2, self.RESERVE3, self.RESERVE4)

			self.ConfidantTableIndex	= rw.rw_int32(self.ConfidantTableIndex)

			self.Padding = rw.rw_bytestring(self.Padding, 144)
			# there's a single \x12 in Strength's padding... why....
			#assert self.RESERVE == b"\0"*144

		def stringify(self):
			return "Confidant List Index: {}, UNK1: {}, Confidant ID: {}, UNK2: {}, Confidant Table Index: {}, Points For Rank: {}".format(
				self.ConfidantListIndex, self.UNK1, self.ConfidantId, self.UNK2, self.ConfidantTableIndex,
				", ".join(f"{i+1}={p}" for i, p in enumerate(self.PointsForRank)),
			)


	class cmmMemberName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmmMemberName, self).__init__()


	class cmmName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmmName, self).__init__()


	class cmmPC_PARAM_Name(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmmPC_PARAM_Name, self).__init__()


	class cmpArbeitName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpArbeitName, self).__init__()


	class cmpCalName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpCalName, self).__init__()


	class cmpConfigHelp(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigHelp, self).__init__()


	class cmpConfigHelpNx(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigHelpNx, self).__init__()


	class cmpConfigHelpPs5(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigHelpPs5, self).__init__()


	class cmpConfigHelpSteam(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigHelpSteam, self).__init__()


	class cmpConfigHelpXbox(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigHelpXbox, self).__init__()


	class cmpConfigItem(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigItem, self).__init__()


	class cmpConfigItemNx(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigItemNx, self).__init__()


	class cmpConfigItemPs5(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigItemPs5, self).__init__()


	class cmpConfigItemSteam(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigItemSteam, self).__init__()


	class cmpConfigItemXbox(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpConfigItemXbox, self).__init__()


	class cmpDifficultName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpDifficultName, self).__init__()


	class cmpMoneyPanelString(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpMoneyPanelString, self).__init__()


	class cmpPersonaParam(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpPersonaParam, self).__init__()


	class cmpQuestName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpQuestName, self).__init__()


	class cmpQuestTargetName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpQuestTargetName, self).__init__()


	class cmpSystemHelp(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpSystemHelp, self).__init__()


	class cmpSystemMenu(JustAString):

		def __init__(self):
			super(FtdEntryTypes.cmpSystemMenu, self).__init__()


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


	class fclCmbComText(JustAString):

		def __init__(self):
			super(FtdEntryTypes.fclCmbComText, self).__init__()


	class fclCustomPartsName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.fclCustomPartsName, self).__init__()


	class fclGunTypeName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.fclGunTypeName, self).__init__()


	class fclInjectionName(JustAString):

		def __init__(self):
			super(FtdEntryTypes.fclInjectionName, self).__init__()


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


	class FLDBGLAYOUTSE(Serializable):

		def __init__(self):
			self.FieldMajorId	= None
			self.FieldMinorId	= None
			self.UNK			= None

		def __rw_hook__(self, rw, datasize):
			self.FieldMajorId	= rw.rw_int16(self.FieldMajorId)
			self.FieldMinorId	= rw.rw_int16(self.FieldMinorId)
			self.UNK			= rw.rw_int32(self.UNK)

		def stringify(self):
			return "Field Major ID: {}, Field Minor ID: {}, ???: {}".format(
				self.FieldMajorId, self.FieldMinorId, self.UNK
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


	class FLDDNGPLACENO(Serializable):

		def __init__(self):
			self.MajorNameIndex	= None
			self.MinorNameIndex	= None
			self.RESERVE		= None

		def __rw_hook__(self, rw, datasize):
			self.MajorNameIndex	= rw.rw_uint16(self.MajorNameIndex)
			self.MinorNameIndex	= rw.rw_uint16(self.MinorNameIndex)

			self.RESERVE = rw.rw_uint32(self.RESERVE)
			assert self.RESERVE == 0

		def stringify(self):
			return "Major Name Index: {}, Minor Name Index: {}".format(
				self.MajorNameIndex, self.MinorNameIndex
			)


	class FLDATDNGPLACENO(FLDDNGPLACENO):

		def __init__(self):
			super(FtdEntryTypes.FLDATDNGPLACENO, self).__init__()


	class FLDTESTDNGPLACENO(FLDDNGPLACENO):

		def __init__(self):
			super(FtdEntryTypes.FLDTESTDNGPLACENO, self).__init__()


	class FLDDOORANIM(Serializable):

		def __init__(self):
			self.DoorObjMajorId	= None
			self.DoorObjMinorId	= None
			self.FldAnimGapId	= None
			self.PlayerOffset1	= None
			self.PlayerOffset2	= None
			self.UnkBitField	= None

		def __rw_hook__(self, rw, datasize):
			self.DoorObjMajorId	= rw.rw_uint16(self.DoorObjMajorId)
			self.DoorObjMinorId	= rw.rw_uint16(self.DoorObjMinorId)
			self.FldAnimGapId	= rw.rw_uint16(self.FldAnimGapId)
			self.PlayerOffset1	= rw.rw_int16s(self.PlayerOffset1, 3)
			self.PlayerOffset2	= rw.rw_int16s(self.PlayerOffset2, 3)
			self.UnkBitField	= rw.rw_uint16(self.UnkBitField)

		def stringify(self):
			return "Door Major ID: {}, Door Minor ID: {}, FieldAnim GAP ID: {}, Player Offset 1: ({}, {}, {}), Player Offset 2: ({}, {}, {}), BitField: {}".format(
				self.DoorObjMajorId, self.DoorObjMinorId, self.FldAnimGapId,
				self.PlayerOffset1[0], self.PlayerOffset1[1], self.PlayerOffset1[2],
				self.PlayerOffset2[0], self.PlayerOffset2[1], self.PlayerOffset2[2],
				self.UnkBitField,
			)


	class FLDDOORSE(Serializable):

		def __init__(self):
			self.DoorObjMajorId		= None
			self.DoorObjMinorId		= None
			# these "cue ids" don't actually match anything so like. idk about this one
			self.DungeonAcbCueId	= None
			self.SecondaryCueId		= None

		def __rw_hook__(self, rw, datasize):
			self.DoorObjMajorId		= rw.rw_uint16(self.DoorObjMajorId)
			self.DoorObjMinorId		= rw.rw_uint16(self.DoorObjMinorId)
			self.DungeonAcbCueId	= rw.rw_int32(self.DungeonAcbCueId)
			self.SecondaryCueId		= rw.rw_int32(self.SecondaryCueId)


		def stringify(self):
			return "Door Major ID: {}, Door Minor ID: {}, Dungeon ACB Cue ID: {}, Secondary Cue ID: {}".format(
				self.DoorObjMajorId, self.DoorObjMinorId,
				self.DungeonAcbCueId, self.SecondaryCueId,
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
				self.FieldMajorId, self.FieldMinorId, FootstepTypes(self.FootstepType).name, self.RoomId,
			)


	class FLDGIMMICKSE(Serializable):

		def __init__(self):
			self.fldObjMajorId	= None
			self.fldObjMinorId	= None
			self.AnimationId	= None
			self.CueId			= None

		def __rw_hook__(self, rw, datasize):
			self.fldObjMajorId	= rw.rw_int16(self.fldObjMajorId)
			self.fldObjMinorId	= rw.rw_int16(self.fldObjMinorId)
			self.AnimationId	= rw.rw_uint32(self.AnimationId)
			self.CueId			= rw.rw_uint32(self.CueId)

		def stringify(self):
			return "FieldObj Major ID: {}, FieldObj Minor ID: {}, Animation ID: {}, Cue ID: {}".format(
				self.fldObjMajorId, self.fldObjMinorId,
				self.AnimationId, self.CueId,
			)


	class FLDLMAPFARE(Serializable):

		def __init__(self):
			self.TravelCosts = None

		def __rw_hook__(self, rw, datasize):
			self.TravelCosts = rw.rw_int32s(self.TravelCosts, 36)

		def stringify(self):
			return "Travel Costs: {}".format(
				", ".join(f"¥{i}" for i in self.TravelCosts)
			)

	class FLDMODELSE(Serializable):

		def __init__(self):
			self.fldObjMajorId		= None
			self.fldObjMinorId		= None
			self.AnimationId		= None
			self.UNKNOWN1			= None
			self.UNKNOWN2			= None
			self.UNKNOWN3			= None
			self.UNKNOWN4			= None
			self.UNKNOWN5			= None
			self.DungeonAcbCueId	= None
			self.UNKNOWN6			= None

		def __rw_hook__(self, rw, datasize):
			self.fldObjMajorId		= rw.rw_uint16(self.fldObjMajorId)
			self.fldObjMinorId		= rw.rw_uint16(self.fldObjMinorId)
			self.AnimationId		= rw.rw_uint16(self.AnimationId)

			self.UNKNOWN1			= rw.rw_uint8(self.UNKNOWN1)
			self.UNKNOWN2			= rw.rw_uint8(self.UNKNOWN2)
			self.UNKNOWN3			= rw.rw_int32(self.UNKNOWN3)
			self.UNKNOWN4			= rw.rw_int32(self.UNKNOWN4)
			self.UNKNOWN5			= rw.rw_int32s(self.UNKNOWN5, 4)

			self.DungeonAcbCueId	= rw.rw_uint32(self.DungeonAcbCueId)
			self.UNKNOWN6			= rw.rw_int32s(self.UNKNOWN6, 7)

		def stringify(self):
			return "fldObjMajorId: {}, DoorObjMinorId: {}, AnimationId: {}, UNKNOWN 1: {}, UNKNOWN 2: {}, UNKNOWN 3: {}, UNKNOWN 4: {}, UNKNOWN 5: {}, DungeonAcb Cue Id: {}, UNKNOWN 6: {}".format(
				self.fldObjMajorId, self.fldObjMinorId, self.AnimationId,
				self.UNKNOWN1, self.UNKNOWN2, self.UNKNOWN3, self.UNKNOWN4,
				self.UNKNOWN5, self.DungeonAcbCueId, self.UNKNOWN6,
			)


	class FLDOBJFLAG(Serializable):

		def __init__(self):
			self.FldObj = None

		def __rw_hook__(self, rw, datasize):
			self.FldObj = rw.rw_objs(self.FldObj, FieldTreasureObject, 10)

		def stringify(self):
			lines = list()
			for i in range(10):
				if any(ind != 0 for ind in self.FldObj[i].TboxIndices):
					lines.append("     ({}) {}".format(i, self.FldObj[i].stringify()))
			if lines:
				lines.insert(0, "Field Treasure Objects:")
			else:
				lines.append("(nothing)")
			return "\n".join(lines)


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


	class FLDSAVEDATAPLACE(JustAString):

		def __init__(self):
			super(FtdEntryTypes.FLDSAVEDATAPLACE, self).__init__()


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


	class FLDWHOLEMAPTABLE(Serializable):

		def __init__(self):
			self.Entries	= None
			self.UNK		= None
			self.RESERVE	= None

		def __rw_hook__(self, rw, datasize):
			entryCount		= (datasize - 4) // 56
			self.Entries	= rw.rw_objs(self.Entries, FieldMapEntry, entryCount)

			self.UNK		= rw.rw_uint16(self.UNK)
			self.RESERVE	= rw.rw_uint16(self.RESERVE)
			assert self.RESERVE == 0

		def stringify(self):
			lines = list()
			lines.append(f"UNK: {self.UNK}")
			for i in range(len(self.Entries)):
				lines.append("    Entry {}: {}".format(i, self.Entries[i].stringify()))
			return "\n".join(lines)


	class FLDWHOLEMAPTABLEDNG(FLDWHOLEMAPTABLE):

		def __init__(self):
			super(FtdEntryTypes.FLDWHOLEMAPTABLEDNG, self).__init__()


	class mypAwardNameTable(JustAString):

		def __init__(self):
			super(FtdEntryTypes.mypAwardNameTable, self).__init__()


	class mypImageNameTable(JustAString):

		def __init__(self):
			super(FtdEntryTypes.mypImageNameTable, self).__init__()


	class teamNameEntryNGWord(JustAString):

		def __init__(self):
			super(FtdEntryTypes.teamNameEntryNGWord, self).__init__()


	class ttrTitleName_STORY(JustAString):

		def __init__(self):
			super(FtdEntryTypes.ttrTitleName_STORY, self).__init__()


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


class FieldMapEntry(Serializable):

	def __init__(self):
		self.Name			= None
		self.FieldMajorId	= None
		self.FieldMinorId	= None
		self.EntranceId		= None
		self.RoomId			= None
		self.HoverProcInd	= None
		self.TravelType		= None
		self.UNK1			= None
		self.UNK2			= None

	def __rw_hook__(self, rw):
		self.Name			= rw.rw_bytestring(self.Name, 40)
		self.FieldMajorId	= rw.rw_uint16(self.FieldMajorId)
		self.FieldMinorId	= rw.rw_uint16(self.FieldMinorId)
		self.EntranceId		= rw.rw_uint16(self.EntranceId)
		self.RoomId			= rw.rw_uint16(self.RoomId)
		self.HoverProcInd	= rw.rw_uint16(self.HoverProcInd)
		self.TravelType		= rw.rw_uint16(self.TravelType)
		self.UNK1			= rw.rw_uint16(self.UNK1)
		assert self.UNK1 == 2
		self.UNK2			= rw.rw_uint16(self.UNK2)

	def stringify(self):
		return "MAP ENTRY: {} (F{:03d}_{:03d}_{}, ENTRANCE {}) -- PROC: {}, VIA: {}, UNK: {}".format(
			self.Name.replace(b"\0", b""), self.FieldMajorId, self.FieldMinorId,
			self.RoomId, self.EntranceId,
			self.HoverProcInd, TravelTypes(self.TravelType).name, self.UNK2,
		)


class FieldTreasureObject(Serializable):

	def __init__(self):
		self.BitFlag		= None
		self.TboxIndices	= None

	def __rw_hook__(self, rw):
		self.BitFlag		= rw.rw_uint32(self.BitFlag)
		self.TboxIndices	= rw.rw_uint16s(self.TboxIndices, 6)

	def stringify(self):
		return "BitFlag: {} + {}, Treasurebox Indices: {}".format(
			hex(self.BitFlag & 0xF0000000), self.BitFlag & 0x0FFFFFFF,
			", ".join(str(ind) for ind in self.TboxIndices if ind != 0),
		)


class FtdListTypes(Enum):
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
	Clear				= 0
	Rainy				= 1
	Cloudy				= 2
	Snow				= 3
	RainySeason			= 4
	TyphoonWarning		= 5
	PollenWarningClear	= 6
	PollenWarningCloudy	= 7
	TorrentialRain		= 8
	HeatWaveHotNight	= 9
	FluSeasonClear		= 10
	FluSeasonCloudy		= 11
	ColdWave			= 12
	ANY					= 255


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


class TravelTypes(Enum):
	TokyoNull			= 2   # unsure
	TokyoCancel			= 3   # unsure
	PalaceNull			= 4   # unsure; seems like palace equivalent of 2
	MementosMap			= 9
	PalaceMap			= 10
	#MementosMap		= 11
	SafeRoom			= 12
	MementosEscalator	= 13
	PalaceCancel		= 14
	PalaceGoBack		= 18  # unsure
	Field				= 27
	TokyoGoBack			= 28  # unsure
	KFEvent				= 29  # unsure
	Hideout				= 33
	Leave				= 35  # whatever that means? lol
	ThievesDen			= 38
	TokyoMap			= 34
	ThirdSem			= 48  # first week of thirdsem???
