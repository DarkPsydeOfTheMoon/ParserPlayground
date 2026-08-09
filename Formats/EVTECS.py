
import array

from .exbip.Serializable import Serializable
from .exbip.Descriptors import StreamHandlers
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


class EVT(Serializable):

	# constants
	ENTRY_SIZE = 0x30

	def __init__(self):
		# variables
		self.Magic = None
		self.Endianness = "<"
		self.IsBigEndian = None
		self.Version = None
		self.MajorId = None
		self.MinorId = None
		self.Rank = None
		self.Level = None
		self.FileSize = None
		self.FileHeaderSize = None

		self.Bitfield = None
		self.EditorDelayedStartEnabled = None
		self.InitScriptEnabled = None
		self.UnkBool1 = None
		self.CinemascopeEnabled = None
		self.CinemascopeAnimationEnabled = None
		self.UseCustomBmdPath = None
		self.UseCustomBfPath = None
		self.UnkBool2 = None

		self.FrameCount = None
		self.FrameRate = None
		self.InitScriptIndex = None
		self.EditorStartingFrame = None
		self.CinemascopeStartingFrame = None
		self.InitEnvAssetID = None
		self.InitDebugEnvAssetID = None
		self.ObjectCount = None
		self.ObjectOffset = None
		self.ObjectSize = None
		self.CommandCount = None
		self.CommandOffset = None
		self.CommandSize = None
		self.BmdPathPointer = None
		self.BmdPathLength = None
		self.EmbeddedBmdOffset = None
		self.EmbeddedBmdSize = None
		self.BfPathPointer = None
		self.BfPathLength = None
		self.EmbeddedBfOffset = None
		self.EmbeddedBfSize = None
		self.MarkerFrameCount = None
		self.MarkerFrames = None

		self.BmdPath = None
		self.BfPath = None

		self.Objects = list()
		self.Commands = list()

		self.UNUSED = [None]*4

	def update_offsets(self):
		self.tobytes()

	def write_right(self, path):
		self.update_offsets()
		self.write(path)

	def __rw_hook__(self, rw):

		self.Endianness = "<"
		self.Magic = rw.rw_string(self.Magic, 3)
		if rw.is_parselike: # writer
			self.Magic = self.Magic.decode()
		assert self.Magic == "EVT"
		self.IsBigEndian = rw.rw_uint8(self.IsBigEndian)
		if (self.IsBigEndian == 1):
			self.Endianness = ">"

		with EndiannessManager(rw, self.Endianness):
			self.Version = rw.rw_uint32(self.Version)
			# 0-999; seems automatically derived from name!
			self.MajorId = rw.rw_uint16(self.MajorId)
			# 0-999; seems automatically derived from name!
			self.MinorId = rw.rw_uint16(self.MinorId)

			# 0 = None, 1 = S, 2 = A, 3 = B, 4 = C, 5 = D
			self.Rank = rw.rw_uint8(self.Rank)
			# 0 = TemporaryGroup, 1 = Alpha, 2 = ???, 3 = ??? (not in editor)
			self.Level = rw.rw_uint8(self.Level)

			self.UNUSED[0] = rw.rw_uint16(self.UNUSED[0])

			self.FileSize = rw.rw_uint32(self.FileSize)
			self.FileHeaderSize = rw.rw_uint32(self.FileHeaderSize)

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.EditorDelayedStartEnabled = self.Bitfield & 0x1
			self.InitScriptEnabled = (self.Bitfield >> 1) & 0x1
			# royal only...?
			self.UnkBool1 = (self.Bitfield >> 6) & 0x1
			self.CinemascopeEnabled = (self.Bitfield >> 8) & 0x1
			self.CinemascopeAnimationEnabled = (self.Bitfield >> 9) & 0x1
			self.UseCustomBmdPath = (self.Bitfield >> 12) & 0x1
			self.UseCustomBfPath = (self.Bitfield >> 14) & 0x1
			# royal only...?
			self.UnkBool2 = (self.Bitfield >> 16) & 0x1

			# 0-99999
			self.FrameCount = rw.rw_uint32(self.FrameCount)
			# always 30
			self.FrameRate = rw.rw_uint8(self.FrameRate)
			# 0-255
			self.InitScriptIndex = rw.rw_uint8(self.InitScriptIndex)
			# 0-99999, since it's a frame (but it's not really set that way in the beta)
			self.EditorStartingFrame = rw.rw_uint16(self.EditorStartingFrame)
			# 0-9999
			self.CinemascopeStartingFrame = rw.rw_uint16(self.CinemascopeStartingFrame)

			self.UNUSED[1] = rw.rw_uint16(self.UNUSED[1])

			# 0-9999
			self.InitEnvAssetID = rw.rw_uint32(self.InitEnvAssetID)
			# 0-9999 (setting prev automatically sets this, too)
			self.InitDebugEnvAssetID = rw.rw_uint32(self.InitDebugEnvAssetID)

			self.ObjectCount = rw.rw_uint32(self.ObjectCount)
			self.ObjectOffset = rw.rw_uint32(self.ObjectOffset)
			self.ObjectSize = rw.rw_uint32(self.ObjectSize)
			#assert self.ObjectSize == self.ENTRY_SIZE

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			self.CommandCount = rw.rw_uint32(self.CommandCount)
			self.CommandOffset = rw.rw_uint32(self.CommandOffset)
			self.CommandSize = rw.rw_uint32(self.CommandSize)
			assert self.CommandSize == self.ENTRY_SIZE

			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])

			self.BmdPathPointer = rw.rw_uint32(self.BmdPathPointer)
			self.BmdPathLength = rw.rw_uint32(self.BmdPathLength)
			self.EmbeddedBmdOffset = rw.rw_uint32(self.EmbeddedBmdOffset)
			self.EmbeddedBmdSize = rw.rw_uint32(self.EmbeddedBmdSize)

			self.BfPathPointer = rw.rw_uint32(self.BfPathPointer)
			self.BfPathLength = rw.rw_uint32(self.BfPathLength)
			self.EmbeddedBfOffset = rw.rw_uint32(self.EmbeddedBfOffset)
			self.EmbeddedBfSize = rw.rw_uint32(self.EmbeddedBfSize)

			self.MarkerFrameCount = (self.FileHeaderSize - rw.tell()) // 4
			self.MarkerFrames = rw.rw_int32s(self.MarkerFrames, self.MarkerFrameCount)

			if rw.is_parselike:
				self.ObjectOffset = rw.tell()
			assert rw.tell() == self.ObjectOffset
			#rw.seek(self.ObjectOffset, 0)
			self.Objects = rw.rw_objs(self.Objects, Object, self.ObjectCount, self.ObjectSize)
			assert len(self.Objects) == self.ObjectCount

			if rw.is_parselike:
				self.CommandOffset = rw.tell()
			assert rw.tell() == self.CommandOffset
			#rw.seek(self.CommandOffset, 0)
			self.Commands = rw.rw_objs(self.Commands, Command, self.CommandCount)
			assert len(self.Commands) == self.CommandCount

			for i in range(len(self.Commands)):
				if rw.is_parselike:
					self.Commands[i].DataOffset = rw.tell()
				#assert rw.tell() == self.Commands[i].DataOffset
				rw.seek(self.Commands[i].DataOffset, 0)
				#if rw.is_parselike: # writer
				#	self.Commands[i].Type = self.Commands[i].Type.decode()
				if self.Commands[i].Type in DataContainer.__dict__:
					dataClassName = self.Commands[i].Type
				else:
					dataClassName = "Unk_"
				if self.Commands[i].DataSize:
					self.Commands[i].Data = rw.rw_obj(self.Commands[i].Data, DataContainer.__dict__[dataClassName], self.Commands[i].DataSize)
				if self.Commands[i].DataOffset + self.Commands[i].DataSize != rw.tell():
					print(self.Commands[i].Type, self.Commands[i].DataSize, self.Commands[i].DataOffset + self.Commands[i].DataSize, rw.tell())
					print(self.MajorId, self.MinorId)
					rw.seek(self.Commands[i].DataOffset + self.Commands[i].DataSize, 0)
				assert self.Commands[i].DataOffset + self.Commands[i].DataSize == rw.tell()

			if self.UseCustomBmdPath: #self.BmdPathPointer:
				if rw.is_parselike:
					self.BmdPathPointer = rw.tell()
				assert rw.tell() == self.BmdPathPointer
				#rw.seek(self.BmdPathPointer, 0)
				##if rw.is_constructlike: # reader
				##self.BmdPath = rw.rw_cbytestring(self.BmdPath)
				##elif rw.is_parselike: # writer
				self.BmdPath = rw.rw_string(self.BmdPath, self.BmdPathLength)

			if self.UseCustomBfPath: #self.BfPathPointer:
				if rw.is_parselike:
					self.BfPathPointer = rw.tell()
				assert rw.tell() == self.BfPathPointer
				#rw.seek(self.BfPathPointer, 0)
				self.BfPath = rw.rw_string(self.BfPath, self.BfPathLength)

			if rw.is_parselike:
				self.FileSize = rw.tell()
			assert rw.tell() == self.FileSize

			failed = False
			try:
				rw.assert_eof()
			except Exception:
				failed = True

			if failed:
				print("Failed to read file!")
				#print(rw._bytestream.peek())
			"""else:
				if rw.is_constructlike:
					print("Read file successfully!")
				elif rw.is_parselike:
					print("Wrote file successfully!")"""

	def from_existing_event(self, extractedDir, majorId, minorId):
		event_id = f"E{majorId:03d}_{minorId:03d}"
		evt_path = "{}/EVENT/{}00/{}0/{}.EVT".format(extractedDir, event_id[:2], event_id[:3], event_id)
		self.read(evt_path)

	def to_new_event(self, extractedDir, majorId, minorId):
		event_id = f"E{majorId:03d}_{minorId:03d}"
		evt_path = "{}/EVENT/{}00/{}0/{}.EVT".format(extractedDir, event_id[:2], event_id[:3], event_id)
		self.write(evt_path)

	def del_object(self, ind):
		assert ind >= 0 and ind < len(self.Objects)
		del self.Objects[ind]
		self.ObjectCount -= 1
		assert len(self.Objects) == self.ObjectCount
		self.CommandOffset -= self.ObjectSize
		for i in range(len(self.Commands)):
			self.Commands[i].DataOffset -= self.ObjectSize

	def del_command(self, ind):
		assert ind >= 0 and ind < len(self.Commands)
		del self.Commands[ind]
		self.CommandCount -= 1
		assert len(self.Commands) == self.CommandCount

	def add_object(self, ind, obj):
		assert ind >= 0 and ind < len(self.Objects)
		self.Objects.insert(ind, obj)
		self.ObjectCount += 1
		assert len(self.Objects) == self.ObjectCount
		self.CommandOffset -= self.ObjectSize
		for i in range(len(self.Commands)):
			self.Commands[i].DataOffset += self.ObjectSize

	def add_command(self, ind, command):
		assert ind >= 0 and ind < len(self.Commands)
		for i in range(len(self.Commands)):
			self.Commands[i].DataOffset += self.CommandSize
			if i > ind:
				self.Commands[i].DataOffset += command.DataSize
		self.Commands.insert(ind, command)
		self.CommandCount += 1
		assert len(self.Commands) == self.CommandCount

	def mod_object(self, ind, **kwargs):
		assert ind >= 0 and ind < len(self.Objects)
		for key in kwargs:
			assert key in self.Objects[ind].__dict__
			self.Objects[ind].__dict__[key] = kwargs[key]

	def mod_command_base(self, ind, **kwargs):
		assert ind >= 0 and ind < len(self.Commands)
		for key in kwargs:
			assert key in self.Commands[ind].__dict__
			self.Commands[ind].__dict__[key] = kwargs[key]

	def mod_command_data(self, ind, **kwargs):
		assert ind >= 0 and ind < len(self.Commands)
		for key in kwargs:
			assert key in self.Commands[ind].Data.__dict__
			if isinstance(self.Commands[ind].Data.__dict__[key], array.array) or isinstance(self.Commands[ind].Data.__dict__[key], list):
				assert len(self.Commands[ind].Data.__dict__[key]) == len(kwargs[key])
			self.Commands[ind].Data.__dict__[key] = kwargs[key]


class ECS(Serializable):

	ENTRY_OFFSET = 0x10
	ENTRY_SIZE   = 0x30
	RESERVE      = 0

	def __init__(self):
		self.Endianness = None
		self.CommandCount = None
		self.CommandOffset = None
		self.CommandSize = None
		self.Reserve = None
		self.Commands = list()

	def update_offsets(self):
		self.tobytes()

	def write_right(self, path):
		self.update_offsets()
		self.write(path)

	def __rw_hook__(self, rw):

		if rw.is_constructlike:
			rw.endianness = ">";
			self.CommandCount = rw.rw_uint32(self.CommandCount)
			self.CommandOffset = rw.rw_uint32(self.CommandOffset)
			self.CommandSize = rw.rw_uint32(self.CommandSize)
			if self.CommandSize != self.ENTRY_SIZE:
				rw.endianness = "<"
			self.Endianness = rw.endianness
			rw.seek(0, 0)
		elif rw.is_parselike:
			rw.endianness = self.Endianness

		self.CommandCount = rw.rw_uint32(self.CommandCount)
		self.CommandOffset = rw.rw_uint32(self.CommandOffset)
		assert self.CommandOffset == self.ENTRY_OFFSET
		self.CommandSize = rw.rw_uint32(self.CommandSize)
		assert self.CommandSize == self.ENTRY_SIZE
		self.Reserve = rw.rw_uint32(self.Reserve)
		assert self.Reserve == self.RESERVE

		if rw.is_parselike:
			self.CommandOffset = rw.tell()
		assert rw.tell() == self.CommandOffset
		if rw.is_parselike:
			self.CommandCount = len(self.Commands)
		self.Commands = rw.rw_objs(self.Commands, Command, self.CommandCount)
		assert len(self.Commands) == self.CommandCount

		for i in range(len(self.Commands)):
			if rw.is_parselike:
				self.Commands[i].DataOffset = rw.tell()
			assert rw.tell() == self.Commands[i].DataOffset
			#rw.seek(self.Commands[i].DataOffset, 0)
			if self.Commands[i].Type in DataContainer.__dict__:
				dataClassName = self.Commands[i].Type
			else:
				dataClassName = "Unk_"
			startPos = rw.tell()
			if self.Commands[i].DataSize:
				self.Commands[i].Data = rw.rw_obj(self.Commands[i].Data, DataContainer.__dict__[dataClassName], self.Commands[i].DataSize)
			assert startPos + self.Commands[i].DataSize == rw.tell()

		failed = False
		try:
			rw.assert_eof()
		except Exception:
			failed = True

		if failed:
			print("Failed to read file!")
			print(rw._bytestream.peek())
		#else:
		#	if rw.is_constructlike:
		#		print("Read file successfully!")
		#	elif rw.is_parselike:
		#		print("Wrote file successfully!")


class Object(Serializable):

	def __init__(self):
		self.Id = None
		self.Type = None
		self.ResourceCategory = None
		self.DuplicateObjectIndex = None
		self.ResourceMajorId = None
		self.ResourceSubId = None
		self.ResourceMinorId = None

		self.Bitfield = None
		self.IsCommon = None
		self.UnkBool1 = None

		self.BaseAnimationID = None
		self.ExtBaseAnimationID = None
		self.ExtAdditiveAnimationID = None
		self.UnkBool2 = None
		self.UNUSED = None

	def __rw_hook__(self, rw, objectSize):
		self.Id = rw.rw_int32(self.Id)
		# 0x0000000 = Null
		# 0x1000101 = Character
		# 0x2000101 = FieldCharacter
		# 0x4000201 = Persona
		# 0x0000301 = Enemy
		# 0x0000401 = SymShadow
		# 0x0000601 = Item
		# 0x0000003 = Field
		# 0x2000701 = FieldObject
		# 0x1000002 = Effect
		# 0x0000005 = Texture
		# 0x0000006 = Sprite
		# 0x0000007 = Camera
		# 0x0000009	= EventCamera
		# 0x0000008 = Movie
		# 0x0000004 = Environment
		# 0x0020101 = CrowdNPC
		self.Type = rw.rw_uint32(self.Type)
		# 0 = Null, 1 = Event, 2 = Field, 3 = Battle, 4 = Scr...ipt?, 5 = Other
		self.ResourceCategory = rw.rw_uint32(self.ResourceCategory)
		# 0-9999; called "UNIQ" in editor... the number of unique copies...? idk, you see it in duplicated objects but i don't really know what it does
		self.DuplicateObjectIndex = rw.rw_uint32(self.DuplicateObjectIndex)
		# 0-9999
		self.ResourceMajorId = rw.rw_uint32(self.ResourceMajorId)
		# 0-255
		self.ResourceSubId = rw.rw_uint16(self.ResourceSubId)
		# 0-255
		self.ResourceMinorId = rw.rw_uint16(self.ResourceMinorId)

		self.Bitfield = rw.rw_uint32(self.Bitfield)
		self.IsCommon = self.Bitfield & 0x1
		self.UnkBool1 = (self.Bitfield >> 31) & 0x1

		# -1 to 9999; default = -1
		self.BaseAnimationID = rw.rw_int32(self.BaseAnimationID)
		if objectSize == 48:
			# -1 to 9999; default = -1
			self.ExtBaseAnimationID = rw.rw_int32(self.ExtBaseAnimationID)
			# -1 to 9999; default = -1
			self.ExtAdditiveAnimationID = rw.rw_int32(self.ExtAdditiveAnimationID)
			self.UnkBool2 = rw.rw_uint32(self.UnkBool2)
			assert self.UnkBool2 == 0 or self.UnkBool2 == 1

			self.UNUSED = rw.rw_int32(self.UNUSED)
			assert self.UNUSED == 0


class Command(Serializable):

	def __init__(self):
		self.Type = None
		self.CommandVersion = None
		self.CommandType = None
		self.ObjectId = None

		self.Bitfield = None
		self.ForceSkipCommand = None
		self.WaitWhileFrameIsStopped = None

		self.StartingFrame = None
		self.FrameCount = None
		self.DataOffset = None
		self.DataSize = None
		self.EvtFlagType = None
		self.EvtFlagId = None
		self.EvtFlagSection = None
		self.EvtFlagIdWithinSection = None
		self.EvtFlagValue = None
		self.EvtFlagConditionalType = None
		self.Data = None

	def __rw_hook__(self, rw):
		self.Type = rw.rw_string(self.Type, 4, encoding="ascii")
		if rw.is_parselike: # writer
			self.Type = self.Type.decode()

		# 0-3 for the beta; 0-4 for royal
		# probably corresponds to the different dataSizes seen in the beta, honestly -- should take note
		self.CommandVersion = rw.rw_int16(self.CommandVersion)
		# corresponds to Type in beta and ECSs, defaults to zero otherwise... also dependent on version? best to leave it at zero...
		self.CommandType = rw.rw_int16(self.CommandType)

		self.ObjectId = rw.rw_int32(self.ObjectId)

		self.Bitfield = rw.rw_int32(self.Bitfield)
		self.ForceSkipCommand = self.Bitfield & 0x1
		self.WaitWhileFrameIsStopped = (self.Bitfield >> 1) & 0x1

		# 0-999999
		self.StartingFrame = rw.rw_int32(self.StartingFrame)
		# 0-999999
		self.FrameCount = rw.rw_int32(self.FrameCount)
		self.DataOffset = rw.rw_int32(self.DataOffset)
		self.DataSize = rw.rw_int32(self.DataSize)

		# 0 = AlwaysRun, 1 = NeverRun, 2 = ReferenceLocalData, 3 = ReferenceGlobalFlags, 4 = ReferenceGlobalCounters, 5 = ReferenceAnimationCounters
		self.EvtFlagType = rw.rw_int32(self.EvtFlagType)
		# (above is in the UI and affects the number below) ... in practice this can be huge, so like... 99999999?
		self.EvtFlagId = rw.rw_uint32(self.EvtFlagId)
		if self.EvtFlagType == 3:
			# 0 = EventFlag, 1 = CommunityFlag, 2 = FieldFlag, 3 = BattleFlag, 4 = SystemFlag, 5 = ProgramFlag
			self.EvtFlagSection = self.EvtFlagId >> 24
			# EventFlag => 0-3071, CommunityFlag => 0-3071, FieldFlag => 0-5119, BattleFlag => 0-511, SystemFlag => 0-511, ProgramFlag => 0-511
			self.EvtFlagIdWithinSection = self.EvtFlagId & 0xFFFFFF
		# 0-999
		self.EvtFlagValue = rw.rw_int32(self.EvtFlagValue)
		# 0 (==), 1 (!=), 2 (>), 3 (<), 4 (>=), 5 (<=)
		self.EvtFlagConditionalType = rw.rw_int32(self.EvtFlagConditionalType)


class DataContainer:


	class AlEf(Serializable):

		def __init__(self):
			self.EffectType = None
			# actually all unused, apparently
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			with EndiannessManager(rw, "<"):
				self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
				# 1 = Bloom/Light, 2 = Overlay
				self.EffectType = rw.rw_uint32(self.EffectType)
				self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
				self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
				for unused in self.UNUSED:
					assert unused == 0


	# Camera: Additive Animation
	class CAA_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.LoopPlayback = None
			self.EnableViewAngleUpdate = None

			self.AssetID = None
			self.AnimationID = None
			self.PlaybackSpeed = None

			self.UNUSED = [None]*8

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_int32(self.Bitfield)
			self.LoopPlayback = self.Bitfield & 0x1
			self.EnableViewAngleUpdate = (self.Bitfield >> 2) & 0x1

			# 0-999
			self.AssetID = rw.rw_int32(self.AssetID)
			# 0-999
			self.AnimationID = rw.rw_int32(self.AnimationID)
			# 0-10; default = 1
			self.PlaybackSpeed = rw.rw_float32(self.PlaybackSpeed)

			for i in range(8):
				self.UNUSED[i] = rw.rw_int32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Camera: Reset
	class CAR_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.ResetCommand = None
			self.ResetParameters = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_int32(self.Bitfield)
			self.ResetCommand = self.Bitfield & 0x1
			self.ResetParameters = (self.Bitfield >> 1) & 0x1
			for i in range(3):
				self.UNUSED[i] = rw.rw_int32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Camera: Clipping Distance
	class CClp(Serializable):

		def __init__(self):
			self.NearClip = None
			self.FarClip = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			for i in range(2):
				self.UNUSED[i] = rw.rw_int32(self.UNUSED[i])
				assert self.UNUSED[i] == 0
			# 1-1000; default = 1
			self.NearClip = rw.rw_float32(self.NearClip)
			# 1-999999; default = 60000 ... actually i see 1000000 in there...
			self.FarClip = rw.rw_float32(self.FarClip)


	class Chap(Serializable):

		def __init__(self):
			self.WaitingFramesEnabled = None
			self.WaitingFrameCount = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			# unclear if these actually get used, but they are in the beta editor, sooo
			# (bool)
			self.WaitingFramesEnabled = rw.rw_uint32(self.WaitingFramesEnabled)
			# 0-120
			self.WaitingFrameCount = rw.rw_uint32(self.WaitingFrameCount)
			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	class Cht_(Serializable):

		def __init__(self):
			self.Action = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			# 0 = None, 1 = SendOn, 2 = SendOff, 3 = DisplayOn, 4 = DisplayOff, 5 = Clear
			self.Action = rw.rw_int32(self.Action)
			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_int32(self.UNUSED[2])


	# Cut-in Start!
	class CiSt(Serializable):

		def __init__(self):
			self.CharacterCategory = None
			self.CharacterNumber = None
			self.FacialExpressionType = None
			self.LocationType = None

			self.UNUSED = [None]*8

		def __rw_hook__(self, rw, dataSize):
			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# 0 = PartyConfidant, 1 = AllyConfidant, 2 = Enemy
			self.CharacterCategory = rw.rw_uint32(self.CharacterCategory)
			# 0-10 if Party; 0-13 if Ally; 0-6 if Enemy
			self.CharacterNumber = rw.rw_uint32(self.CharacterNumber)
			# 0-21
			self.FacialExpressionType = rw.rw_uint32(self.FacialExpressionType)
			# 0 = Left, 1 = Center, 2 = Right
			self.LocationType = rw.rw_uint32(self.LocationType)

			for i in range(2, 8):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Camera Movement: Character
	class CMC_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.DepthOfFieldEnabled = None
			self.IndividualDepthOfFieldSettingsEnabled = None
			#self.UnkBool = None
			self.DirectlySpecifyMessageCoordinates = None

			self.InterpolationParameters = None
			self.InterpolationType = None
			self.InGradientType = None
			self.OutGradientType = None

			self.StartCorrectionFrameNumber = None
			self.AssetID = None
			self.ShotType = None
			self.AngleNumber = None

			self.DistanceOfFarBlurSurface = None
			self.FocalPlaneDistance = None
			self.DistanceOfNearBlurSurface = None
			self.BlurStrength = None
			self.BlurType = None

			self.MessageCoordinateType = None
			self.MessageCoordinates = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 48 or dataSize == 64

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.DepthOfFieldEnabled = self.Bitfield & 0x1
			self.IndividualDepthOfFieldSettingsEnabled = (self.Bitfield >> 1) & 0x1
			#self.UnkBool = (self.Bitfield >> 4) & 0x1
			self.DirectlySpecifyMessageCoordinates = (self.Bitfield >> 5) & 0x1

			self.InterpolationParameters = rw.rw_uint32(self.InterpolationParameters)
			# 0 = Linear, 1 = Step, 2 = Hermitian; default = 2 (always 2 lol)
			self.InterpolationType = self.InterpolationParameters & 0xFF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.InGradientType = (self.InterpolationParameters >> 8) & 0xF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.OutGradientType = (self.InterpolationParameters >> 12) & 0xF

			# 0-60; must not exceed number of frames in the command, or else be invalid
			self.StartCorrectionFrameNumber = rw.rw_uint16(self.StartCorrectionFrameNumber)

			self.UNUSED[0] = rw.rw_uint16(self.UNUSED[0])
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])

			# 0-999
			self.AssetID = rw.rw_uint32(self.AssetID)
			# 0 = FaceCloseUp, 1 = BustUp, 2 = WholeBody, 3 = OverheadView / BirdsEyeView
			self.ShotType = rw.rw_uint32(self.ShotType)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			# 0 = FrontRightCheek, 1 = FrontDirect, 2 = FrontLeftCheek, 3 = BackRightCheek, 4 = BackDirect, 5 = BackLeftCheek
			self.AngleNumber = rw.rw_uint32(self.AngleNumber)

			# 0-5000; default = 120 (???) ... actually default = 215 when DOF enabled
			self.FocalPlaneDistance = rw.rw_float32(self.FocalPlaneDistance)
			# 0-5000 ... except i actually do see larger numbers so maybe it was expanded; default = 116 (???) ... actually default = 110 when DOF enabled
			self.DistanceOfNearBlurSurface = rw.rw_float32(self.DistanceOfNearBlurSurface)
			# 0-5000; default = 0 (???) ... actually default = 220 when DOF enabled
			self.DistanceOfFarBlurSurface = rw.rw_float32(self.DistanceOfFarBlurSurface)
			# 0-1; default = 2 (??????) ... actually default = 1 when DOF enabled
			self.BlurStrength = rw.rw_float32(self.BlurStrength)
			if dataSize > 48:
				# 0 = 5x5GaussianFilter, 1 = 2IterationGaussian, 2 = 3IterationGaussian, 3 = 5IterationGaussian, 4 = 7IterationGaussian
				self.BlurType = rw.rw_uint32(self.BlurType)
				# 0 = UpperLeft, 1 = UpperCenter, 2 = UpperRight, 3 = LowerLeft, 4 = LowerCenter, 5 = LowerRight; default = 4/BottomCenter
				self.MessageCoordinateType = rw.rw_uint32(self.MessageCoordinateType)
				# -9999 to +9999; default = 375, 528
				self.MessageCoordinates = rw.rw_float32s(self.MessageCoordinates, 2)

			for unused in self.UNUSED:
				assert unused == 0


	# Camera Movement: Continuous
	# (info from EvtTool)
	class CMCn(Serializable):

		def __init__(self):
			self.Direction = None
			self.Distance = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# 0 = None, 1 = Forward, 2 = Back, 3 = Left, 4 = Right, 5 = Up, 6 = Down
			self.Direction = rw.rw_uint32(self.Direction)
			self.Distance = rw.rw_float32(self.Distance)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])

			for i in range(2):
				assert self.UNUSED[i] == 0


	class CMD_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.UnkBool1 = None
			self.UnkBool2 = None
			self.UnkBool3 = None
			self.UnkBool4 = None
			self.DepthOfFieldEnabled = None

			self.ViewportCoordinates = None
			self.Yaw = None
			self.Pitch = None
			self.Roll = None
			self.AngleOfView = None

			self.InterpolationParameters = None
			self.InterpolationType = None
			self.InGradientType = None
			self.OutGradientType = None

			self.FocalPlaneDistance = None
			self.DistanceOfNearBlurSurface = None
			self.DistanceOfFarBlurSurface = None
			self.BlurStrength = None
			self.BlurType = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 48 or dataSize == 64

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# the first few are always 1......
			self.UnkBool1 = self.Bitfield & 0x1
			self.UnkBool2 = (self.Bitfield >> 1) & 0x1
			self.UnkBool3 = (self.Bitfield >> 2) & 0x1
			self.UnkBool4 = (self.Bitfield >> 3) & 0x1
			self.DepthOfFieldEnabled = (self.Bitfield >> 4) & 0x1

			# all initialized to whatever the last CSD_ had them at lol...
			# -99999 to +99999
			self.ViewportCoordinates = rw.rw_float32s(self.ViewportCoordinates, 3)
			# -180 to +180
			self.Yaw = rw.rw_float32(self.Yaw)
			self.Pitch = rw.rw_float32(self.Pitch)
			self.Roll = rw.rw_float32(self.Roll)
			# 1-180... 45 seems like a good default
			self.AngleOfView = rw.rw_float32(self.AngleOfView)

			self.InterpolationParameters = rw.rw_uint32(self.InterpolationParameters)
			# 0 = Linear, 1 = Step, 2 = Hermitian; default = 2 (always 2 lol)
			self.InterpolationType = self.InterpolationParameters & 0xFF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.InGradientType = (self.InterpolationParameters >> 8) & 0xF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.OutGradientType = (self.InterpolationParameters >> 12) & 0xF

			# 0-5000 ... tbh, probably 999999
			self.FocalPlaneDistance = rw.rw_float32(self.FocalPlaneDistance)
			# 0-5000 ... except i actually do see larger numbers so maybe it was expanded ... probably 999999
			self.DistanceOfNearBlurSurface = rw.rw_float32(self.DistanceOfNearBlurSurface)
			# 0-5000 ... probably 999999
			self.DistanceOfFarBlurSurface = rw.rw_float32(self.DistanceOfFarBlurSurface)
			if dataSize > 48:
				# 0-1; default = 1
				self.BlurStrength = rw.rw_float32(self.BlurStrength)
				# 0 = 5x5GaussianFilter, 1 = 2IterationGaussian, 2 = 3IterationGaussian, 3 = 5IterationGaussian, 4 = 7IterationGaussian
				self.BlurType = rw.rw_uint32(self.BlurType)
				for i in range(2):
					self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
					assert self.UNUSED[i] == 0


	class CQuk(Serializable):

		def __init__(self):
			self.StrengthOfShaking = None
			self.DegreeOfPitch = None
			self.FadeInFrames = None
			self.FadeOutFrames = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0-100
			self.StrengthOfShaking = rw.rw_float32(self.StrengthOfShaking)
			# 0-1
			self.DegreeOfPitch = rw.rw_float32(self.DegreeOfPitch)
			# 0-10000
			self.FadeInFrames = rw.rw_uint32(self.FadeInFrames)
			# 0-10000
			self.FadeOutFrames = rw.rw_uint32(self.FadeOutFrames)

			for i in range(1, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Camera Set Asset / Animation...
	class CSA_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.LoopPlayback = None
			# / updated parameters...?
			self.CorrectionParametersEnabled = None
			self.DepthOfFieldEnabled = None
			self.UnkBool1 = None
			self.DirectlySpecifyMessageCoordinates = None
			self.UnkBool2 = None

			self.AssetID = None
			self.AnimationID = None
			self.PlaybackSpeed = None
			self.StartingFrame = None

			self.ViewportCoordinates = None
			self.ViewportRotation = None

			self.FocalPlaneDistance = None
			self.DistanceOfNearBlurSurface = None
			self.DistanceOfFarBlurSurface = None
			self.BlurStrength = None
			self.BlurType = None
			self.MessageCoordinateType = None
			self.MessageCoordinates = None

			self.Unk1 = None
			self.Unk2 = None
			self.UNUSED = [None]*5

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 48 or dataSize == 80 or dataSize == 96

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.LoopPlayback = self.Bitfield & 0x1
			self.CorrectionParametersEnabled = (self.Bitfield >> 1) & 0x1
			self.DepthOfFieldEnabled = (self.Bitfield >> 2) & 0x1
			# always == 1
			self.UnkBool1 = (self.Bitfield >> 4) & 0x1
			# on by default?? well that's stupid
			self.DirectlySpecifyMessageCoordinates = (self.Bitfield >> 5) & 0x1
			self.UnkBool2 = (self.Bitfield >> 8) & 0x1

			# 0-999
			self.AssetID = rw.rw_uint32(self.AssetID)
			# 0-999
			self.AnimationID = rw.rw_uint32(self.AnimationID)
			# 0-10; default = 1
			self.PlaybackSpeed = rw.rw_float32(self.PlaybackSpeed)
			# 0-99999
			self.StartingFrame = rw.rw_uint32(self.StartingFrame)

			# -99999 to +99999
			self.ViewportCoordinates = rw.rw_float32s(self.ViewportCoordinates, 3)
			# -180 to +180
			self.ViewportRotation = rw.rw_float32s(self.ViewportRotation, 3)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			if dataSize > 48:
				# 0-5000; default = 1.01
				self.FocalPlaneDistance = rw.rw_float32(self.FocalPlaneDistance)
				# 0-5000 ... except i actually do see larger numbers so maybe it was expanded; default = 1.01
				self.DistanceOfNearBlurSurface = rw.rw_float32(self.DistanceOfNearBlurSurface)
				# 0-5000; default = 1.01
				self.DistanceOfFarBlurSurface = rw.rw_float32(self.DistanceOfFarBlurSurface)
				# 0-1; default = 1
				self.BlurStrength = rw.rw_float32(self.BlurStrength)
				# 0 = 5x5GaussianFilter, 1 = 2IterationGaussian, 2 = 3IterationGaussian, 3 = 5IterationGaussian, 4 = 7IterationGaussian
				self.BlurType = rw.rw_uint32(self.BlurType)
				# 0 = UpperLeft, 1 = UpperCenter, 2 = UpperRight, 3 = LowerLeft, 4 = LowerCenter, 5 = LowerRight; default = 4/BottomCenter
				self.MessageCoordinateType = rw.rw_uint32(self.MessageCoordinateType)
				# -9999 to +9999; default = 375, 528 ... weirdly 375, 565 sometimes?? hrm.
				self.MessageCoordinates = rw.rw_float32s(self.MessageCoordinates, 2)

				if dataSize > 80:
					# still might be a bitfield tbh but :shrug:
					# 0, 1, 2... 0 by far most frequent
					self.Unk1 = rw.rw_uint8(self.Unk1)
					# a few different low numbers... most frequent is 2
					self.Unk2 = rw.rw_uint8(self.Unk2)
					self.UNUSED[1] = rw.rw_uint16(self.UNUSED[1])
					assert self.UNUSED[1] == 0
					for i in range(2, 5):
						self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
						assert self.UNUSED[i] == 0


	class CSD_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.DepthOfFieldEnabled = None
			self.UnkBool1 = None
			self.DirectlySpecifyMessageCoordinates = None
			self.UnkBool2 = None

			self.ViewpointCoordinates = None
			self.Yaw = None
			self.Pitch = None
			self.Roll = None
			self.AngleOfView = None
			self.DistanceOfFarBlurSurface = None
			self.FocalPlaneDistance = None
			self.DistanceOfNearBlurSurface = None
			self.BlurStrength = None
			self.BlurType = None
			self.MessageCoordinateType = None
			self.MessageCoordinates = None

			self.UnkEnum = None
			self.UnkCount1 = None
			self.UnkCount2 = None
			self.UnkCount3 = None
			self.UnkPosition = None

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 32 or dataSize == 48 or dataSize == 64 or dataSize == 80

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.DepthOfFieldEnabled = self.Bitfield & 0x1
			# always == 1
			self.UnkBool1 = (self.Bitfield >> 4) & 0x1
			self.DirectlySpecifyMessageCoordinates = (self.Bitfield >> 5) & 0x1
			self.UnkBool2 = (self.Bitfield >> 8) & 0x1

			# -99999 to +99999; default X=0 Y=500 Z=1000
			self.ViewpointCoordinates = rw.rw_float32s(self.ViewpointCoordinates, 3)
			# -180 to +180
			self.Yaw = rw.rw_float32(self.Yaw)
			# default = -26.57
			self.Pitch = rw.rw_float32(self.Pitch)
			self.Roll = rw.rw_float32(self.Roll)
			# 1-180; default = 55
			self.AngleOfView = rw.rw_float32(self.AngleOfView)
			if dataSize > 32:
				# 0-5000; default = 1.01
				self.DistanceOfFarBlurSurface = rw.rw_float32(self.DistanceOfFarBlurSurface)
				# 0-5000; default = 1.01
				self.FocalPlaneDistance = rw.rw_float32(self.FocalPlaneDistance)
				# 0-5000 ... except i actually do see larger numbers so maybe it was expanded; default = 1.01
				self.DistanceOfNearBlurSurface = rw.rw_float32(self.DistanceOfNearBlurSurface)
				# 0-1; default = 1
				self.BlurStrength = rw.rw_float32(self.BlurStrength)
				if dataSize > 48:
					# 0 = 5x5GaussianFilter, 1 = 2IterationGaussian, 2 = 3IterationGaussian, 3 = 5IterationGaussian, 4 = 7IterationGaussian
					self.BlurType = rw.rw_uint32(self.BlurType)
					# 0 = UpperLeft, 1 = UpperCenter, 2 = UpperRight, 3 = LowerLeft, 4 = LowerCenter, 5 = LowerRight; default = 4/BottomCenter
					self.MessageCoordinateType = rw.rw_uint32(self.MessageCoordinateType)
					# -9999 to +9999; default = 375, 528
					self.MessageCoordinates = rw.rw_float32s(self.MessageCoordinates, 2)
					if dataSize > 64:
						# 0-2
						self.UnkEnum = rw.rw_uint8(self.UnkEnum)
						# 0, 2, 5
						self.UnkCount1 = rw.rw_uint8(self.UnkCount1)
						self.UnkCount2 = rw.rw_uint8(self.UnkCount2)
						self.UnkCount3 = rw.rw_uint8(self.UnkCount3)
						self.UnkPosition = rw.rw_float32s(self.UnkPosition, 3)


	class CSDD(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.DepthOfFieldEnabled = None
			self.UnkBool = None

			self.Position = None
			self.Yaw = None
			self.Pitch = None
			self.Roll = None
			self.AngleOfView = None
			self.FocalPlaneDistance = None
			self.DistanceOfNearBlurSurface = None
			self.DistanceOfFarBlurSurface = None
			self.BlurStrength = None

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.DepthOfFieldEnabled = self.Bitfield & 0x1
			self.UnkBool = (self.Bitfield >> 1) & 0x1

			self.Position = rw.rw_float32s(self.Position, 3)
			# -180 - 180
			self.Yaw = rw.rw_float32(self.Yaw)
			self.Pitch = rw.rw_float32(self.Pitch)
			self.Roll = rw.rw_float32(self.Roll)
			# 1-180
			self.AngleOfView = rw.rw_float32(self.AngleOfView)
			# 0-5000
			self.FocalPlaneDistance = rw.rw_float32(self.FocalPlaneDistance)
			# 0-5000 ... except i actually do see larger numbers so maybe it was expanded
			self.DistanceOfNearBlurSurface = rw.rw_float32(self.DistanceOfNearBlurSurface)
			# 0-5000
			self.DistanceOfFarBlurSurface = rw.rw_float32(self.DistanceOfFarBlurSurface)
			# 0-1
			self.BlurStrength = rw.rw_float32(self.BlurStrength)


	# Camera Set Editor...? EVTCMR?
	class CSEc(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.EditingEnabled = None
			self.UnkBool1 = None
			self.UnkBool2 = None
			self.MessageCoordinateTypeSpecification = None
			self.MessageCoordinateDirectSpecification = None
			self.UnkBool3 = None

			self.AssetID = None
			self.MessageCoordinateType = None
			self.MessageCoordinates = None

			self.UnkBool4 = None
			self.UnkEnum = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# always 0 in practice
			self.EditingEnabled = self.Bitfield & 0x1
			# always 1
			self.UnkBool1 = (self.Bitfield >> 1) & 0x1
			# always 1 in beta
			self.UnkBool2 = (self.Bitfield >> 2) & 0x1
			self.MessageCoordinateTypeSpecification = (self.Bitfield >> 3) & 0x1
			self.MessageCoordinateDirectSpecification = (self.Bitfield >> 4) & 0x1
			# always 1 in royal
			self.UnkBool3 = (self.Bitfield >> 5) & 0x1

			# 0-999
			self.AssetID = rw.rw_uint32(self.AssetID)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# 0 = UpperLeft, 1 = UpperCenter, 2 = UpperRight, 3 = LowerLeft, 4 = LowerCenter, 5 = LowerRight; default = 4/BottomCenter
			self.MessageCoordinateType = rw.rw_uint32(self.MessageCoordinateType)
			# -9999 to +9999; default = 375, 528 ... or 565? nope. 528...
			self.MessageCoordinates = rw.rw_float32s(self.MessageCoordinates, 2)

			self.UnkBool4 = rw.rw_uint8(self.UnkBool4)
			self.UnkEnum = rw.rw_uint8(self.UnkEnum)

			self.UNUSED[2] = rw.rw_uint16(self.UNUSED[2])
			#assert self.UNUSED[2] == 0


	class CShk(Serializable):

		def __init__(self):
			self.Mode = None
			self.Type = None
			self.Magnitude = None
			self.Speed = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			#assert self.UNUSED[0] == 0

			# 0 = Start, 1 = Stop
			self.Mode = rw.rw_uint32(self.Mode)
			# 0 = Basic ("Test Data"), 1 = TrainCar, 2 = CloseUp
			self.Type = rw.rw_uint32(self.Type)
			# 0-100
			self.Magnitude = rw.rw_float32(self.Magnitude)
			# 0-100
			self.Speed = rw.rw_float32(self.Speed)

			for i in range(1, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	class CSk_(Serializable):

		def __init__(self):
			self.VibrationMode = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# 0 = None, 1 = Stop, 2 = Off, 3 = Low, 4 = Middle, 5 = High
			self.VibrationMode = rw.rw_uint32(self.VibrationMode)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			for unused in self.UNUSED:
				assert unused == 0


	# Crowd Clip (I'm guessing)
	class CwCl(Serializable):

		def __init__(self):
			self.CrowdMin = None
			self.CrowdMax = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			# always 1
			self.CrowdMin = rw.rw_uint32(self.CrowdMin)
			# min = 0, max = 1114... usually in the low hundreds
			self.CrowdMax = rw.rw_uint32(self.CrowdMax)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Crowd... Data?
	class CwD_(Serializable):

		def __init__(self):
			self.UNK = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# observed: 51, 100
			self.UNK = rw.rw_uint32(self.UNK)

			for i in range(1, 3):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Crowd... Hit? Hideout?
	class CwHt(Serializable):

		def __init__(self):
			self.UnkBool = None
			self.UnkEnum = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UnkBool = rw.rw_uint32(self.UnkBool)
			# observed: 3, 4, 5, 6
			self.UnkEnum = rw.rw_uint32(self.UnkEnum)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Crowd... Person?
	# show/hide crowd models
	class CwP_(Serializable):

		def __init__(self):
			self.Mode = None
			self.CrowdPersonID = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			# 0 = Hide, 1 = Show
			self.Mode = rw.rw_uint32(self.Mode)
			self.CrowdPersonID = rw.rw_int32(self.CrowdPersonID)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	class Date(Serializable):

		def __init__(self):
			self.Toggle = None
			self.AnimationType = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# could also be a bitfield, i suppose
			# 0 = None, 1 = On, 2 = Off
			self.Toggle = rw.rw_uint8(self.Toggle)
			# 0 = Inward/Fast, 1 = Outward/Slow
			self.AnimationType = rw.rw_uint8(self.AnimationType)

			self.UNUSED[1] = rw.rw_uint16(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])


	# Effect: Transparency
	class EAlp(Serializable):

		def __init__(self):
			#self.AlphaLevel = None
			self.RGBA = None

			self.InterpolationParameters = None
			self.InterpolationType = None
			self.InGradientType = None
			self.OutGradientType = None

			self.TranslucentMode = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			#with EndiannessManager(rw, ">"):
			#	# 0-255; default = 255
			#	self.AlphaLevel = rw.rw_uint32(self.AlphaLevel)
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)
			assert not any(self.RGBA[:3])

			self.InterpolationParameters = rw.rw_uint32(self.InterpolationParameters)
			# 0 = Linear, 1 = Step, 2 = Hermitian; default = 2 (always 2 lol)
			self.InterpolationType = self.InterpolationParameters & 0xFF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.InGradientType = (self.InterpolationParameters >> 8) & 0xF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.OutGradientType = (self.InterpolationParameters >> 12) & 0xF

			# might not actually be used tbh, stole this from MAlp, but it's always 0
			# 0 = Normal, 1 = Mask, 2 = PostMask
			self.TranslucentMode = rw.rw_uint8(self.TranslucentMode)

			self.UNUSED[1] = rw.rw_uint8(self.UNUSED[1])
			assert self.UNUSED[1] == 0
			self.UNUSED[2] = rw.rw_uint16(self.UNUSED[2])
			assert self.UNUSED[2] == 0


	# Effect: Load
	class ELd_(Serializable):

		def __init__(self):
			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			for i in range(4):
				self.UNUSED[i] = rw.rw_int32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Effect: Movement
	class EMD_(Serializable):

		def __init__(self):
			self.MovementType = None
			self.NumberOfControlGroups = None
			self.Coordinates = [None]*24
			self.MovementSpeed = None
			self.AutoFrameCountIGuess = None
			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			# 0 = StraightLine, 1 = BezierCurve
			self.MovementType = rw.rw_int32(self.MovementType)
			# 1-8
			self.NumberOfControlGroups = rw.rw_int32(self.NumberOfControlGroups)
			for i in range(24):
				self.Coordinates[i] = rw.rw_float32s(self.Coordinates[i], 3)

			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 1-50; default = 1
			self.MovementSpeed = rw.rw_float32(self.MovementSpeed)
			# number of frames...? seems auto-calculated but also inconsistent. roughly 50*self.NumberOfControlGroups//self.MovementSpeed
			self.AutoFrameCountIGuess = rw.rw_int32(self.AutoFrameCountIGuess)
			for i in range(1, 4):
				self.UNUSED[i] = rw.rw_int32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: Background Color
	class EnBc(Serializable):

		def __init__(self):
			self.RGBA = 0x202020FF
			self.Unk = 4354
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			# always 4354
			self.Unk = rw.rw_uint32(self.Unk)
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			# shown in editor as HSL + alpha but stored as RGBA
			# default = 32, 32, 32, 255
			#self.RGBA = rw.rw_uint8s(self.RGBA, 4)
			self.RGBA = rw.rw_uint32(self.RGBA)


	# Environment: Color Correction
	class EnCc(Serializable):

		def __init__(self):
			self.Enable = None
			self.Unk1 = None

			self.Cyan = None
			self.Magenta = None
			self.Yellow = None
			self.Dodge = None
			self.Burn = None

			self.UNUSED = [None]*5

		def __rw_hook__(self, rw, dataSize):

			self.Enable = rw.rw_uint32(self.Enable)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# -1 to 1; default = 0
			self.Cyan = rw.rw_float32(self.Cyan)
			# -1 to 1; default = 0
			self.Magenta = rw.rw_float32(self.Magenta)
			# -1 to 1; default = 0
			self.Yellow = rw.rw_float32(self.Yellow)
			# 0-0.99; default = 0
			self.Dodge = rw.rw_float32(self.Dodge)
			# 0-0.99; default = 0
			self.Burn = rw.rw_float32(self.Burn)

			for i in range(2, 5):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: DOF (Depth of Field)
	class EnDf(Serializable):

		def __init__(self):
			self.Unk1 = None
			self.Unk2 = None
			self.Unk3 = None

			self.FocalPlaneDistance = None
			self.DistanceOfNearBlurSurface = None
			self.DistanceOfFarBlurSurface = None
			self.DistanceBlurLimit = None
			self.BlurStrength = None
			self.BlurType = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			# 0, 3 (but always 0 in the beta; 3 appears in royal)
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# 0, 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)
			# 0, 4354
			self.Unk3 = rw.rw_uint32(self.Unk3)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0-100; default = 0.5
			self.FocalPlaneDistance = rw.rw_float32(self.FocalPlaneDistance)
			# 0-100; default = 1.0
			self.DistanceOfNearBlurSurface = rw.rw_float32(self.DistanceOfNearBlurSurface)
			# 0-100; default = 1.0
			self.DistanceOfFarBlurSurface = rw.rw_float32(self.DistanceOfFarBlurSurface)
			# 0-100; default = 0.75
			self.DistanceBlurLimit = rw.rw_float32(self.DistanceBlurLimit)
			# 0.5-1.0; default = 1.0 ... except one time it's 100??? but that's the limit in the UI anyway
			self.BlurStrength = rw.rw_float32(self.BlurStrength)
			# 0 = 5x5GaussianFilter, 1 = 2IterationGaussian, 2 = 3IterationGaussian, 3 = 5IterationGaussian, 4 = 7IterationGaussian
			self.BlurType = rw.rw_uint32(self.BlurType)

			for i in range(1, 3):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: Distance Fog
	class EnFD(Serializable):

		def __init__(self):
			self.Bitfield = 65537
			self.MatchWithCameraClips = 1
			self.Unk1 = 1

			self.Unk2 = 4354

			self.Mode = 0
			self.StartDistance = 5
			self.EndDistance = 2000
			self.RGBA = 0x7F7F7F00

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# always 1
			self.Unk1 = self.Bitfield & 0x1
			# default = 1
			self.MatchWithCameraClips = (self.Bitfield >> 16) & 0x1

			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# 0 = Linear, 1 = Exponential, 2 = Exponential2
			self.Mode = rw.rw_uint32(self.Mode)

			# -9999999 to 9999999; default = 5
			self.StartDistance = rw.rw_float32(self.StartDistance)
			# -9999999 to 9999999; default = 2000
			self.EndDistance = rw.rw_float32(self.EndDistance)

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 127, 127, 127, 0
			self.RGBA = rw.rw_uint32(self.RGBA)


	# Environment: Height Fog
	class EnFH(Serializable):

		def __init__(self):

			self.Unk1 = None
			self.Unk2 = None

			self.StartHeight = None
			self.EndHeight = None
			self.RGBA = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			# always 1
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# -9999999 to 9999999; default = 5
			self.StartHeight = rw.rw_float32(self.StartHeight)
			# -9999999 to 9999999; default = 2000
			self.EndHeight = rw.rw_float32(self.EndHeight)

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 127, 127, 127, 0
			self.RGBA = rw.rw_uint32(self.RGBA)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			assert self.UNUSED[2] == 0


	# Environment: HDR (High Dynamic Range)
	class EnHd(Serializable):

		def __init__(self):

			self.Bitfield = None
			self.EnableToneMap = None
			self.EnableStarFilter = None
			self.UnkBool = None

			self.Unk1 = None

			self.ToneMapMediumBrightness = None
			self.ToneMapBloomStrength = None
			self.ToneMapAdaptiveBrightness = None
			self.ToneMapAdaptiveBloom = None

			self.StarFilterNumberOfLines = None
			self.StarFilterLength = None
			self.StarFilterStrength = None
			self.StarFilterGlareChromaticAberration = None
			self.StarFilterGlareTilt = None

			self.Unk2 = None
			self.Unk3 = None
			self.Unk4 = None

			self.UnkEnum = None
			self.UnkColor1 = None
			self.UnkColor2 = None
			self.UnkColor3 = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			assert dataSize == 64 or dataSize == 80

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.EnableToneMap = (self.Bitfield >> 16) & 0x1
			self.EnableStarFilter = (self.Bitfield >> 17) & 0x1
			# always 0 in beta, sometimes 1 in royal
			self.UnkBool = (self.Bitfield >> 18) & 0x1

			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# 0-10
			self.ToneMapMediumBrightness = rw.rw_float32(self.ToneMapMediumBrightness)
			# 0-4; default = 0.3
			self.ToneMapBloomStrength = rw.rw_float32(self.ToneMapBloomStrength)
			# 0-1
			self.ToneMapAdaptiveBrightness = rw.rw_float32(self.ToneMapAdaptiveBrightness)
			# looks like 0-1.5...? default = 0.01666, highest observed is 1.4099999...
			self.ToneMapAdaptiveBloom = rw.rw_float32(self.ToneMapAdaptiveBloom)

			# 2-4; default = 4
			self.StarFilterNumberOfLines = rw.rw_uint32(self.StarFilterNumberOfLines)
			# 0.1-2.0; default = 1.0
			self.StarFilterLength = rw.rw_float32(self.StarFilterLength)
			# 0-4; default = 0.5
			self.StarFilterStrength = rw.rw_float32(self.StarFilterStrength)
			# 0-5; default = 1.5
			self.StarFilterGlareChromaticAberration = rw.rw_float32(self.StarFilterGlareChromaticAberration)
			# 0-360; default = 25.0
			self.StarFilterGlareTilt = rw.rw_float32(self.StarFilterGlareTilt)

			# 0-100; seems like default is 3.8
			self.Unk2 = rw.rw_float32(self.Unk2)
			# 0-6; seems like default is 0.35
			self.Unk3 = rw.rw_float32(self.Unk3)
			# 0-2; seems like default is 0.03
			self.Unk4 = rw.rw_float32(self.Unk4)

			if dataSize > 64:
				# 1, 2; guessing 1 is the default
				self.UnkEnum = rw.rw_uint32(self.UnkEnum)
				# might be RGBAs somewhere in here? i truly have no idea
				self.UnkColor1 = rw.rw_uint32(self.UnkColor1)
				self.UnkColor2 = rw.rw_uint32(self.UnkColor2)
				self.UnkColor3 = rw.rw_uint32(self.UnkColor3)


	# Environment: Light 0 (Item Lighting)
	class EnL0(Serializable):

		def __init__(self):

			self.Unk1 = None
			self.Unk2 = None

			self.AmbientRGBA = None
			self.DiffuseRGBA = None
			self.SpecularRGBA = None

			self.Direction = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):

			# always 1
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 191, 191, 191, 255 (0xbfbfbfff)
			self.AmbientRGBA = rw.rw_uint32(self.AmbientRGBA)
			# default = 229, 229, 229, 255 (0xe5e5e5ff)
			self.DiffuseRGBA = rw.rw_uint32(self.DiffuseRGBA)
			# default = 255, 255, 255, 255 (0xffffffff)
			self.SpecularRGBA = rw.rw_uint32(self.SpecularRGBA)

			# -1 to 1
			self.Direction = rw.rw_float32s(self.Direction, 3)

			for i in range(2, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: Independent Light (Character Lighting)
	class EnLI(Serializable):

		def __init__(self):

			self.Unk1 = None
			self.Unk2 = None

			self.AmbientRGBA = None
			self.DiffuseRGBA = None
			self.SpecularRGBA = None

			self.Direction = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):

			# always 1
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 191, 191, 191, 255
			self.AmbientRGBA = rw.rw_uint32(self.AmbientRGBA)
			# default = 229, 229, 229, 255
			self.DiffuseRGBA = rw.rw_uint32(self.DiffuseRGBA)
			# default = 255, 255, 255, 255
			self.SpecularRGBA = rw.rw_uint32(self.SpecularRGBA)

			# -1 to 1
			self.Direction = rw.rw_float32s(self.Direction, 3)

			for i in range(2, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: Outline
	# not in the beta -- could be in final vanilla? but def in royal
	class EnOl(Serializable):

		def __init__(self):

			self.Unk1 = None
			self.Unk2 = None

			self.Opacity = None
			self.Width = None
			self.Brightness = None
			self.RangeMin = None
			self.RangeMax = None

			self.UNUSED = [None]*1

		def __rw_hook__(self, rw, dataSize):

			# always 1
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			# 0-9999
			self.Opacity = rw.rw_float32(self.Opacity)
			# always 1.01
			self.Width = rw.rw_float32(self.Width)
			# 0-1
			self.Brightness = rw.rw_float32(self.Brightness)
			# 0-9999
			self.RangeMin = rw.rw_float32(self.RangeMin)
			# 0-9999
			self.RangeMax = rw.rw_float32(self.RangeMax)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0


	# Environment: Physics
	class EnPh(Serializable):

		def __init__(self):
			self.Enable = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			# default = 1
			self.Enable = rw.rw_uint32(self.Enable)

			for i in range(3):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: Shadow
	class EnSh(Serializable):

		def __init__(self):
			self.Unk1 = None
			self.Unk2 = None

			self.Bitfield = None
			self.SetCameraFarClipToDepthRange = None
			self.UnkBool1 = None
			self.UnkBool2 = None
			self.BackSideDrawingEnabled = None

			self.DepthRange = None
			self.Bias = None
			self.Ambient = None
			self.Diffuse = None
			self.CascadingShadowMapSplitRate = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):

			# always 0... guess it could be unused
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.SetCameraFarClipToDepthRange = self.Bitfield & 0x1
			# always 1
			self.UnkBool1 = (self.Bitfield >> 1) & 0x1
			# always 1
			self.UnkBool2 = (self.Bitfield >> 2) & 0x1
			self.BackSideDrawingEnabled = (self.Bitfield >> 3) & 0x1

			# 0-9999; default = 2000
			self.DepthRange = rw.rw_float32(self.DepthRange)
			# -3 to +3; default = 0
			self.Bias = rw.rw_float32(self.Bias)
			# 0-1; default = 1
			self.Ambient = rw.rw_float32(self.Ambient)
			# 0-1; default = 1
			self.Diffuse = rw.rw_float32(self.Diffuse)
			# 0.01-0.99; default = 0.12
			self.CascadingShadowMapSplitRate = rw.rw_float32(self.CascadingShadowMapSplitRate)

			for i in range(2, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: SSAO (Screen Space Ambient Occlusion)
	# in the editor, but never used, even in the beta! fascinating...
	class EnSs(Serializable):

		def __init__(self):

			self.Enable = None
			self.Unk = None

			self.Range = None
			self.Radius = None
			self.Attenuation = None
			self.Concentration = None
			self.Blur = None

			self.UNUSED = [None]*5

		def __rw_hook__(self, rw, dataSize):

			self.Enable = rw.rw_uint32(self.Enable)
			# always 4354
			self.Unk = rw.rw_uint32(self.Unk)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# 0-1000; default = 545
			self.Range = rw.rw_float32(self.Range)
			# 0-3; default = 1.15
			self.Radius = rw.rw_float32(self.Radius)
			# 0.01-1.0; default = 0.45
			self.Attenuation = rw.rw_float32(self.Attenuation)
			# 0.01-5.0; default = 1.0
			self.Concentration = rw.rw_float32(self.Concentration)
			# 0-5; default = 1.5
			self.Blur = rw.rw_float32(self.Blur)

			for i in range(2, 5):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Environment: Load
	class Env_(Serializable):

		def __init__(self):
			self.ObjectID = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			self.ObjectID = rw.rw_uint32(self.ObjectID)
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			for unused in self.UNUSED:
				assert unused == 0


	# Effect: Register
	class ERgs(Serializable):

		def __init__(self):
			self.DisplayType = None
			self.Scene = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# 0 = None, 1 = On, 2 = Off
			self.DisplayType = rw.rw_uint32(self.DisplayType)
			# 0 = Scene 0, 1 = Scene 1 (but it's always 0 so idfk what this means)
			self.Scene = rw.rw_uint32(self.Scene)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			for unused in self.UNUSED:
				assert unused == 0


	# Effect: Scale
	class EScl(Serializable):

		def __init__(self):
			self.ScaleValue = None
			self.InterpolationType = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0 = Linear, 1 = Step, 4354 = Hermitian (why not 2????? beats me)
			self.InterpolationType = rw.rw_uint32(self.InterpolationType)
			# 0-100; default = 1
			self.ScaleValue = rw.rw_float32(self.ScaleValue)

			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])
			assert self.UNUSED[1] == 0


	# Effect: Placement (Coordinates)
	class ESD_(Serializable):

		def __init__(self):
			self.Coordinates = None
			#self.Rotation = None
			# I could be wrong here... it seems to be up-down, left-right, front-back axis... that's right, isn't it?
			self.Pitch = None
			self.Yaw = None
			self.Roll = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			# X, Y, Z; -99999 to +99999
			self.Coordinates = rw.rw_float32s(self.Coordinates, 3)
			# -180 to +180
			#self.Rotation = rw.rw_float32s(self.Rotation, 3)
			self.Pitch = rw.rw_float32(self.Pitch)
			self.Yaw = rw.rw_float32(self.Yaw)
			self.Roll = rw.rw_float32(self.Roll)
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			for unused in self.UNUSED:
				assert unused == 0


	# Effect: Placement (Helper/Bone)
	class ESH_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.FrameEnabled = None
			self.AlwaysSynchronize = None

			self.StartCorrectionFrameNumber = None
			self.EndCorrectionFrameNumber = None
			self.StartInterpolationType = None
			self.EndInterpolationType = None
			self.ModelAssetID = None
			self.HelperID = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# always 0
			self.FrameEnabled = self.Bitfield & 0x1
			self.AlwaysSynchronize = (self.Bitfield >> 1) & 0x1

			# 0-60
			self.StartCorrectionFrameNumber = rw.rw_uint16(self.StartCorrectionFrameNumber)
			# 0-60
			self.EndCorrectionFrameNumber = rw.rw_uint16(self.EndCorrectionFrameNumber)
			# always 4354
			# 0 = Linear, 4354 = HermiteSlowToSlow, 4610 = HermiteFastToSlow, 8450 = HermiteSlowToFast; default = 4354/HermiteSlowToSlow
			#self.Unk1 = rw.rw_uint32(self.Unk1)
			self.StartInterpolationType = rw.rw_uint32(self.StartInterpolationType)
			# always 4354
			# 0 = Linear, 4354 = HermiteSlowToSlow, 4610 = HermiteFastToSlow, 8450 = HermiteSlowToFast; default = 4354/HermiteSlowToSlow
			#self.Unk2 = rw.rw_uint32(self.Unk2)
			self.EndInterpolationType = rw.rw_uint32(self.EndInterpolationType)
			# 0-999
			self.ModelAssetID = rw.rw_uint32(self.ModelAssetID)
			# 0-9999
			self.HelperID = rw.rw_uint32(self.HelperID)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Field: Additive Animation
	class FAA_(Serializable):

		def __init__(self):
			self.Unk = None
			self.ObjectIndex = None

			self.Bitfield = None
			self.SecondAnimationDisabled = None
			self.FirstAnimationFrameBlendEnabled = None
			self.SecondAnimationFrameBlendEnabled = None
			self.DebugFrameForward = None

			self.FirstAnimationID = None
			self.FirstAnimationStartingFrame = None
			self.FirstAnimationEndFrame = None
			self.FirstAnimationInterpolatedFrames = None
			self.FirstAnimationLoopBool = None
			self.FirstAnimationWeight = None
			self.FirstAnimationPlaybackSpeed = None

			self.SecondAnimationID = None
			self.SecondAnimationStartingFrame = None
			self.SecondAnimationEndFrame = None
			self.SecondAnimationInterpolatedFrames = None
			self.SecondAnimationLoopBool = None
			self.SecondAnimationWeight = None
			self.SecondAnimationPlaybackSpeed = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			# always 174?
			self.Unk = rw.rw_uint32(self.Unk)
			# limited set of ints, usually 31, but absolutely inscrutable. doesn't look like a bitfield
			self.ObjectIndex = rw.rw_uint32(self.ObjectIndex)

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# fully guesswork lol
			self.SecondAnimationDisabled = self.Bitfield & 0x1
			self.FirstAnimationFrameBlendEnabled = (self.Bitfield >> 1) & 0x1
			self.SecondAnimationFrameBlendEnabled = (self.Bitfield >> 2) & 0x1
			self.DebugFrameForward = (self.Bitfield >> 31) & 0x1

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			self.FirstAnimationID = rw.rw_uint32(self.FirstAnimationID)
			self.FirstAnimationStartingFrame = rw.rw_uint32(self.FirstAnimationStartingFrame)
			# fully guessing lol... always 0
			self.FirstAnimationEndFrame = rw.rw_uint32(self.FirstAnimationEndFrame)
			# fully guessing lol... always 0
			self.FirstAnimationInterpolatedFrames = rw.rw_uint32(self.FirstAnimationInterpolatedFrames)
			self.FirstAnimationLoopBool = rw.rw_uint32(self.FirstAnimationLoopBool)
			self.FirstAnimationWeight = rw.rw_float32(self.FirstAnimationWeight)
			self.FirstAnimationPlaybackSpeed = rw.rw_float32(self.FirstAnimationPlaybackSpeed)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])

			self.SecondAnimationID = rw.rw_uint32(self.SecondAnimationID)
			self.SecondAnimationStartingFrame = rw.rw_uint32(self.SecondAnimationStartingFrame)
			# fully guessing lol... only nonzero once in beta
			self.SecondAnimationEndFrame = rw.rw_uint32(self.SecondAnimationEndFrame)
			# fully guessing lol... only nonzero once in beta
			self.SecondAnimationInterpolatedFrames = rw.rw_uint32(self.SecondAnimationInterpolatedFrames)
			self.SecondAnimationLoopBool = rw.rw_uint32(self.SecondAnimationLoopBool)
			self.SecondAnimationWeight = rw.rw_float32(self.SecondAnimationWeight)
			self.SecondAnimationPlaybackSpeed = rw.rw_float32(self.SecondAnimationPlaybackSpeed)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			for unused in self.UNUSED:
				assert unused == 0


	# Field: Base Animation
	class FAB_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.SecondAnimationDisabled = None
			self.FirstAnimationFrameBlendEnabled = None
			self.SecondAnimationFrameBlendEnabled = None
			self.DebugFrameForward = None

			self.ObjectIndex = None

			self.FirstAnimationID = None
			self.FirstAnimationStartingFrame = None
			self.FirstAnimationEndFrame = None
			self.FirstAnimationInterpolatedFrames = None
			self.FirstAnimationLoopBool = None
			self.FirstAnimationPlaybackSpeed = None

			self.SecondAnimationID = None
			self.SecondAnimationStartingFrame = None
			self.SecondAnimationEndFrame = None
			self.SecondAnimationInterpolatedFrames = None
			self.SecondAnimationLoopBool = None
			self.SecondAnimationPlaybackSpeed = None

			self.UNUSED = [None]*6

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# fully guesswork lol
			self.SecondAnimationDisabled = self.Bitfield & 0x1
			self.FirstAnimationFrameBlendEnabled = (self.Bitfield >> 1) & 0x1
			self.SecondAnimationFrameBlendEnabled = (self.Bitfield >> 2) & 0x1
			self.DebugFrameForward = (self.Bitfield >> 31) & 0x1

			# :shrug:
			self.ObjectIndex = rw.rw_uint32(self.ObjectIndex)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])

			self.FirstAnimationID = rw.rw_uint32(self.FirstAnimationID)
			self.FirstAnimationStartingFrame = rw.rw_uint32(self.FirstAnimationStartingFrame)
			self.FirstAnimationEndFrame = rw.rw_uint32(self.FirstAnimationEndFrame)
			self.FirstAnimationInterpolatedFrames = rw.rw_uint32(self.FirstAnimationInterpolatedFrames)
			self.FirstAnimationLoopBool = rw.rw_uint32(self.FirstAnimationLoopBool)
			self.FirstAnimationPlaybackSpeed = rw.rw_float32(self.FirstAnimationPlaybackSpeed)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])

			self.SecondAnimationID = rw.rw_uint32(self.SecondAnimationID)
			self.SecondAnimationStartingFrame = rw.rw_uint32(self.SecondAnimationStartingFrame)
			self.SecondAnimationEndFrame = rw.rw_uint32(self.SecondAnimationEndFrame)
			self.SecondAnimationInterpolatedFrames = rw.rw_uint32(self.SecondAnimationInterpolatedFrames)
			self.SecondAnimationLoopBool = rw.rw_uint32(self.SecondAnimationLoopBool)
			self.SecondAnimationPlaybackSpeed = rw.rw_float32(self.SecondAnimationPlaybackSpeed)

			self.UNUSED[4] = rw.rw_uint32(self.UNUSED[4])
			self.UNUSED[5] = rw.rw_uint32(self.UNUSED[5])

			for unused in self.UNUSED:
				assert unused == 0


	# Flashback: End
	# Or... field background?
	# ...but they often seem to have ended already, so idfk
	class FbEn(Serializable):

		def __init__(self):
			self.UNUSED = None

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED = rw.rw_uint32s(self.UNUSED, 4)
			for unused in self.UNUSED:
				assert unused == 0


	# Fade
	class Fd__(Serializable):

		def __init__(self):
			self.FadeMode = None
			self.FadeType = None
			self.UnkBool = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UnkBool = rw.rw_int32(self.UnkBool)
			# 0 = None, 1 = FadeIn, 2 = FadeOut
			self.FadeMode = rw.rw_int8(self.FadeType)
			# 0 = BasicFade, 5 = BrushStrokes, ... etc.
			self.FadeType = rw.rw_int8(self.FadeType)
			self.UNUSED[0] = rw.rw_int16(self.UNUSED[0])
			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_int32(self.UNUSED[2])
			for unused in self.UNUSED:
				assert unused == 0


	# Field: ???
	class FDFl(Serializable):

		def __init__(self):
			self.Unk1 = None
			self.Unk2 = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			with EndiannessManager(rw, ">"):
				# 0, 100
				self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0


	# Fade (Simple)
	class FdS_(Serializable):

		def __init__(self):
			self.FadeType = None
			self.UnkBool = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UnkBool = rw.rw_uint32(self.UnkBool)
			# 0 = None, 1 = FadeInBlack, 2 = FadeOutBlack, 3 = FadeInWhite, 4 = FadeOutWhite
			self.FadeType = rw.rw_uint32(self.FadeType)
			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Field: ???
	class FGFl(Serializable):

		def __init__(self):
			self.UnkEnum = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			with EndiannessManager(rw, "<"):
				# 0-2
				self.UnkEnum = rw.rw_uint32(self.UnkEnum)
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			for unused in self.UNUSED:
				assert unused == 0


	# Flashback: Start
	# Or... field background?
	# (actually more for like, flashes of metaverse background in reality)
	class Flbk(Serializable):

		def __init__(self):
			self.ImageMajorID = None
			self.ImageMinorID = None
			self.ImageOpacity = None
			self.UnkBool = None

			self.UnkFloats = None
			self.OverlayObjectIDs = None

			self.UNUSED = [None]*7

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			self.ImageMajorID = rw.rw_uint16(self.ImageMajorID)
			self.ImageMinorID = rw.rw_uint16(self.ImageMinorID)
			# 0-255
			self.ImageOpacity = rw.rw_uint32(self.ImageOpacity)
			# always 1
			self.UnkBool = rw.rw_uint32(self.UnkBool)

			# positioning? duration? idk
			# all used Flbk commands have [80.0, 250.0, 1.0, 2.6666667461395264, 3.3333332538604736, 3.3333332538604736, 15.0]
			self.UnkFloats = rw.rw_float32s(self.UnkFloats, 7)
			# could be more allowed, but this is the most that get used
			self.OverlayObjectIDs = rw.rw_uint32s(self.OverlayObjectIDs, 3)

			# might some of these be positioning or rotation?
			for i in range(1, 7):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Frame: Free Motion!
	# never appears ever! but you can add it in the editor
	class FMtn(Serializable):

		def __init__(self):
			self.AssetID = None

			self.Bitfield = None
			self.UpAnimationFromExt = None
			self.DownAnimationFromExt = None
			self.LeftAnimationFromExt = None
			self.RightAnimationFromExt = None

			self.UpAnimationID = None
			self.DownAnimationID = None
			self.LeftAnimationID = None
			self.RightAnimationID = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			# 0-999
			self.AssetID = rw.rw_uint32(self.AssetID)

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.UpAnimationFromExt = self.Bitfield & 0x1
			self.DownAnimationFromExt = (self.Bitfield >> 1) & 0x1
			self.LeftAnimationFromExt = (self.Bitfield >> 2) & 0x1
			self.RightAnimationFromExt = (self.Bitfield >> 3) & 0x1

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# -1 to 59; default = -1
			self.UpAnimationID = rw.rw_int32(self.UpAnimationID)
			self.DownAnimationID = rw.rw_int32(self.DownAnimationID)
			self.LeftAnimationID = rw.rw_int32(self.LeftAnimationID)
			self.RightAnimationID = rw.rw_int32(self.RightAnimationID)


	# Field Object Data...?
	class FOD_(Serializable):

		def __init__(self):
			# that's my guess, anyway...
			self.EnableFieldObject = None
			self.ObjectIndex = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.EnableFieldObject = rw.rw_uint32(self.EnableFieldObject)
			# -1 to like 65535... actually 64235 but you get it
			self.ObjectIndex = rw.rw_int32(self.ObjectIndex)
			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	class FrJ_(Serializable):

		def __init__(self):
			self.DestinationFrame = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			# 0-99999
			self.DestinationFrame = rw.rw_uint32(self.DestinationFrame)

			for i in range(3):
				self.UNUSED[i] = rw.rw_int32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Field: Placement
	class FS__(Serializable):

		def __init__(self):
			self.UnkBool = None
			self.Coordinates = None
			self.Rotation = None
			self.UnkFloat = None
			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			self.UnkBool = rw.rw_uint32(self.UnkBool)
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			self.Coordinates = rw.rw_float32s(self.Coordinates, 3)
			self.Rotation = rw.rw_float32s(self.Rotation, 3)
			self.UnkFloat = rw.rw_float32(self.UnkFloat)

			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])

			for unused in self.UNUSED:
				assert unused == 0


	# GUI: ???
	class GCAP(Serializable):

		def __init__(self):
			self.Unk1 = None
			self.Unk2 = None
			self.Unk3 = None
			self.Unk4 = None

		def __rw_hook__(self, rw, dataSize):
			# 0, 2, 4, 6, 10
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# 0-20 or so
			self.Unk2 = rw.rw_uint32(self.Unk2)
			# 0-3
			self.Unk3 = rw.rw_uint32(self.Unk3)
			# 0, 4-10
			self.Unk4 = rw.rw_uint32(self.Unk4)


	# GUI: Good Gauge
	class GGGg(Serializable):

		def __init__(self):
			self.Unk1 = None
			self.Unk2 = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 1-3
			self.Unk1 = rw.rw_uint32(self.Unk1)

			self.UNUSED[1] = rw.rw_uint16(self.UNUSED[1])
			assert self.UNUSED[1] == 0

			# 0-2
			self.Unk2 = rw.rw_uint16(self.Unk2)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			assert self.UNUSED[2] == 0


	# GUI: Poem
	class GPoe(Serializable):

		def __init__(self):
			self.PoemType = None
			self.PoemID = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0 = ConfidantStart, 1 = ConfidantMax, 2 = GameOver
			# only GameOver is actually used, interestingly
			self.PoemType = rw.rw_uint32(self.PoemType)
			self.PoemID = rw.rw_uint32(self.PoemID)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0


	# Image: Display
	class ImDp(Serializable):

		def __init__(self):
			self.Mode = None
			self.PlayAnimation = None
			self.ImageID = None
			self.FrameID = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 1 = Show, 2 = Hide
			self.Mode = rw.rw_uint8(self.Mode)
			# bool
			self.PlayAnimation = rw.rw_uint8(self.PlayAnimation)
			# from IMAGE/PICT{}.DDS
			self.ImageID = rw.rw_uint16(self.ImageID)
			# from IMAGE/FRAME{}.GMD
			self.FrameID = rw.rw_uint16(self.FrameID)

			self.UNUSED[1] = rw.rw_uint16(self.UNUSED[1])
			assert self.UNUSED[1] == 0

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			assert self.UNUSED[2] == 0


	# Frame: Intervention...?
	# never appears ever! but you can add it in the editor
	class InVn(Serializable):

		def __init__(self):

			self.LabelNumber = None
			self.LocalDataNumber = None

			self.DestinationFrame1 = None
			self.DestinationFrame2 = None
			self.DestinationFrame3 = None
			self.DestinationFrame4 = None
			self.DestinationFrame5 = None
			self.DestinationFrame6 = None
			self.DestinationFrame7 = None
			self.DestinationFrame8 = None

			self.UNUSED = [None]*6

		def __rw_hook__(self, rw, dataSize):

			self.LabelNumber = rw.rw_uint32(self.LabelNumber)
			self.LocalDataNumber = rw.rw_uint32(self.LocalDataNumber)

			self.DestinationFrame1 = rw.rw_uint32(self.DestinationFrame1)
			self.DestinationFrame2 = rw.rw_uint32(self.DestinationFrame2)
			self.DestinationFrame3 = rw.rw_uint32(self.DestinationFrame3)
			self.DestinationFrame4 = rw.rw_uint32(self.DestinationFrame4)
			self.DestinationFrame5 = rw.rw_uint32(self.DestinationFrame5)
			self.DestinationFrame6 = rw.rw_uint32(self.DestinationFrame6)
			self.DestinationFrame7 = rw.rw_uint32(self.DestinationFrame7)
			self.DestinationFrame8 = rw.rw_uint32(self.DestinationFrame8)

			for i in range(6):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Letterbox
	class LBX_(Serializable):

		def __init__(self):
			self.UnkEnum1 = None
			self.UnkEnum2 = None
			self.UnkBool = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			# 0, 2 ... presumably can also be 1...?
			self.UnkEnum1 = rw.rw_uint32(self.UnkEnum1)
			# 1, 2
			self.UnkEnum2 = rw.rw_uint8(self.UnkEnum2)
			self.UnkBool = rw.rw_uint8(self.UnkBool)
			self.UNUSED[0] = rw.rw_uint16(self.UNUSED[0])
			for i in range(1, 3):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	class MAA_(Serializable):

		def __init__(self):
			self.TrackNumber = None
			self.AnimationID = None
			self.InterpolatedFrames = None
			self.Weight = None
			self.LoopBool = None
			self.PlaybackSpeed = None
			self.StartingFrame = None

			self.Bitfield = None
			self.FromExt = None
			self.DebugFrameForward = None

		def __rw_hook__(self, rw, dataSize):
			# 0-7 ...  I guess there are 7-or-8 slots for additive animations? inchresting...
			# only 1-7 ever appear, though... so... is zero not actually an option?
			self.TrackNumber = rw.rw_int32(self.TrackNumber)
			# 0-49
			self.AnimationID = rw.rw_int32(self.AnimationID)
			# 0-100
			self.InterpolatedFrames = rw.rw_int32(self.InterpolatedFrames)
			# 0-1; default = 1
			self.Weight = rw.rw_float32(self.Weight)
			self.LoopBool = rw.rw_int32(self.LoopBool)
			# 0-10; default = 1
			self.PlaybackSpeed = rw.rw_float32(self.PlaybackSpeed)
			# 0-99999
			self.StartingFrame = rw.rw_uint32(self.StartingFrame)

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.FromExt = self.Bitfield & 0x1
			self.DebugFrameForward = (self.Bitfield >> 31) & 0x1


	# Attachment Animation (base animation for attached object)
	class MAAB(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.SecondAnimationDisabled = None
			self.SecondAnimationFrameBlendEnabled = None
			self.FirstAnimationFromExt = None
			self.SecondAnimationFromExt = None

			self.ChildObjectId = None

			self.FirstAnimationID = None
			self.FirstAnimationInterpolatedFrames = None
			self.FirstAnimationLoopBool = None
			self.FirstAnimationPlaybackSpeed = None
			self.FirstAnimationStartingFrame = None
			self.FirstAnimationEndFrame = None

			self.SecondAnimationID = None
			self.SecondAnimationInterpolatedFrames = None
			self.SecondAnimationLoopBool = None
			self.SecondAnimationPlaybackSpeed = None
			self.SecondAnimationStartingFrame = None
			self.SecondAnimationEndFrame = None

			self.UNUSED = [None]*6

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_int32(self.Bitfield)
			self.SecondAnimationDisabled = self.Bitfield & 0x1
			self.SecondAnimationFrameBlendEnabled = (self.Bitfield >> 1) & 0x1
			self.FirstAnimationFromExt = (self.Bitfield >> 4) & 0x1
			self.SecondAnimationFromExt = (self.Bitfield >> 5) & 0x1

			# 0-999
			self.ChildObjectId = rw.rw_int32(self.ChildObjectId)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])

			self.FirstAnimationID = rw.rw_int32(self.FirstAnimationID)
			self.FirstAnimationInterpolatedFrames = rw.rw_int32(self.FirstAnimationInterpolatedFrames)
			# default = 0
			self.FirstAnimationLoopBool = rw.rw_int32(self.FirstAnimationLoopBool)
			self.FirstAnimationPlaybackSpeed = rw.rw_float32(self.FirstAnimationPlaybackSpeed)
			self.FirstAnimationStartingFrame = rw.rw_int32(self.FirstAnimationStartingFrame)
			self.FirstAnimationEndFrame = rw.rw_int32(self.FirstAnimationEndFrame)

			for i in range(2, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])

			self.SecondAnimationID = rw.rw_int32(self.SecondAnimationID)
			self.SecondAnimationInterpolatedFrames = rw.rw_int32(self.SecondAnimationInterpolatedFrames)
			# default = 1
			self.SecondAnimationLoopBool = rw.rw_int32(self.SecondAnimationLoopBool)
			self.SecondAnimationPlaybackSpeed = rw.rw_float32(self.SecondAnimationPlaybackSpeed)
			self.SecondAnimationStartingFrame = rw.rw_int32(self.SecondAnimationStartingFrame)
			self.SecondAnimationEndFrame = rw.rw_int32(self.SecondAnimationEndFrame)

			for i in range(4, 6):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])

			for unused in self.UNUSED:
				assert unused == 0


	class MAB_(Serializable):

		def __init__(self):
			self.FirstAnimationIndex = None
			self.FirstAnimationUnkFrames = None
			self.FirstAnimationInterpolatedFrames = None
			self.FirstAnimationLoopBool = None
			self.FirstAnimationPlaybackSpeed = None

			self.SecondAnimationIndex = None
			self.SecondAnimationUnkFrames = None
			self.SecondAnimationInterpolatedFrames = None
			self.SecondAnimationLoopBool = None
			self.SecondAnimationPlaybackSpeed = None

			self.Bitfield = None
			self.SecondAnimationDisabled = None
			self.SecondAnimationFrameBlendingEnabled = None
			self.FirstAnimationFromExt = None
			self.SecondAnimationFromExt = None
			self.UnkBool1 = None
			self.UnkBool2 = None
			self.UnkBool3 = None
			self.UnkBool4 = None
			self.UnkBool5 = None
			self.UnkBool6 = None
			self.UnkBool7 = None
			self.DebugUnkBool = None
			self.DebugFrameForward = None

			self.FirstAnimationStartingFrame = None
			self.FirstAnimationEndFrame = None
			self.SecondAnimationStartingFrame = None
			self.SecondAnimationEndFrame = None
			self.StartWaitingFrame = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			# 0-59
			self.FirstAnimationIndex = rw.rw_uint32(self.FirstAnimationIndex)
			self.FirstAnimationUnkFrames = rw.rw_uint16(self.FirstAnimationUnkFrames)
			# 0-100
			self.FirstAnimationInterpolatedFrames = rw.rw_uint16(self.FirstAnimationInterpolatedFrames)
			# default = 0
			self.FirstAnimationLoopBool = rw.rw_uint32(self.FirstAnimationLoopBool)
			# 0-10; default = 1
			self.FirstAnimationPlaybackSpeed = rw.rw_float32(self.FirstAnimationPlaybackSpeed)

			self.SecondAnimationIndex = rw.rw_uint32(self.SecondAnimationIndex)
			self.SecondAnimationUnkFrames = rw.rw_uint16(self.SecondAnimationUnkFrames)
			self.SecondAnimationInterpolatedFrames = rw.rw_uint16(self.SecondAnimationUnkFrames)
			# default = 1
			self.SecondAnimationLoopBool = rw.rw_int32(self.SecondAnimationLoopBool)
			self.SecondAnimationPlaybackSpeed = rw.rw_float32(self.SecondAnimationPlaybackSpeed)

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.SecondAnimationDisabled = self.Bitfield & 0x1
			self.SecondAnimationFrameBlendingEnabled = (self.Bitfield >> 1) & 0x1
			self.FirstAnimationFromExt = (self.Bitfield >> 4) & 0x1
			self.SecondAnimationFromExt = (self.Bitfield >> 5) & 0x1
			# no idea what any of these do... they're in the beta but not in the editor!
			self.UnkBool1 = (self.Bitfield >> 6) & 0x1
			self.UnkBool2 = (self.Bitfield >> 7) & 0x1
			self.UnkBool3 = (self.Bitfield >> 8) & 0x1
			self.UnkBool4 = (self.Bitfield >> 9) & 0x1
			self.UnkBool5 = (self.Bitfield >> 10) & 0x1
			self.UnkBool6 = (self.Bitfield >> 11) & 0x1
			self.UnkBool7 = (self.Bitfield >> 12) & 0x1
			# this persists, but does it affect rendering and not just debug...?
			self.DebugUnkBool = (self.Bitfield >> 30) & 0x1
			self.DebugFrameForward = (self.Bitfield >> 31) & 0x1

			# 0-99999
			self.FirstAnimationStartingFrame = rw.rw_int32(self.FirstAnimationStartingFrame)
			# 0-99999
			self.FirstAnimationEndFrame = rw.rw_int32(self.FirstAnimationEndFrame)
			# 0-99999
			self.SecondAnimationStartingFrame = rw.rw_int32(self.SecondAnimationStartingFrame)
			# 0-99999
			self.SecondAnimationEndFrame = rw.rw_int32(self.SecondAnimationEndFrame)
			# 0-20
			self.StartWaitingFrame = rw.rw_uint32(self.StartWaitingFrame)

			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])
			for unused in self.UNUSED:
				assert unused == 0


	# Model: Idle Animation
	class MAI_(Serializable):

		def __init__(self):
			self.Bitfield = [None]*10
			self.AnimationEnabled = [None]*10
			self.AnimationFromExt = [None]*10
			self.FrameBlendingEnabled = [None]*10

			self.AnimationID = [None]*10
			self.AnimationStartingFrame = [None]*10
			self.AnimationEndingFrame = [None]*10
			self.AnimationInterpolatedFrames = [None]*10
			self.AnimationPlaybackSpeed = [None]*10

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			for i in range(10):
				# 5 by default...?
				self.Bitfield[i] = rw.rw_uint32(self.Bitfield[i])
				# 1 by default for first animation... immutably so i guess
				self.AnimationEnabled[i] = self.Bitfield[i] & 0x1
				self.AnimationFromExt[i] = (self.Bitfield[i] >> 1) & 0x1
				# 1 by default for all (immutably so for first animation???)
				self.FrameBlendingEnabled[i] = (self.Bitfield[i] >> 2) & 0x1

				# 0-59
				self.AnimationID[i] = rw.rw_uint32(self.AnimationID[i])
				# 0-99999
				self.AnimationStartingFrame[i] = rw.rw_uint32(self.AnimationStartingFrame[i])
				# 0-99999
				self.AnimationEndingFrame[i] = rw.rw_uint32(self.AnimationEndingFrame[i])
				# 0-100
				self.AnimationInterpolatedFrames[i] = rw.rw_uint32(self.AnimationInterpolatedFrames[i])
				# 0-10; default = 1
				self.AnimationPlaybackSpeed[i] = rw.rw_float32(self.AnimationPlaybackSpeed[i])

			for i in range(1, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Model: Transparency
	class MAlp(Serializable):

		def __init__(self):
			#self.AlphaLevel = None
			self.RGBA = None

			self.InterpolationParameters = None
			self.InterpolationType = None
			self.InSlopeType = None
			self.OutSlopeType = None

			self.TranslucentMode = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			#with EndiannessManager(rw, ">"):
			#	# 0-255; default = 255
			#	self.AlphaLevel = rw.rw_uint32(self.AlphaLevel)
			# only A is used
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)
			assert not any(self.RGBA[:3])

			# default = 4354
			self.InterpolationParameters = rw.rw_uint32(self.InterpolationParameters)
			# 0 = Linear, 1 = Step, 2 = Hermite; default = 2 (always 2 lol)
			self.InterpolationType = self.InterpolationParameters & 0xFF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.InSlopeType = (self.InterpolationParameters >> 8) & 0xF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.OutSlopeType = (self.InterpolationParameters >> 12) & 0xF

			# 0 = Normal, 1 = Mask, 2 = PostMask
			self.TranslucentMode = rw.rw_uint8(self.TranslucentMode)

			self.UNUSED[1] = rw.rw_uint8(self.UNUSED[1])
			assert self.UNUSED[1] == 0
			self.UNUSED[2] = rw.rw_uint16(self.UNUSED[2])
			assert self.UNUSED[2] == 0


	# Model: Attachment
	class MAt_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.UnkBool = None

			self.BoneId = None
			self.ChildObjectId = None

			self.RelativeXPosition = None
			self.RelativeYPosition = None
			self.RelativeZPosition = None

			self.XRotation = None
			self.YRotation = None
			self.ZRotation = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.UnkBool = (self.Bitfield >> 4) & 0x1

			# 0-9999
			self.BoneId = rw.rw_uint32(self.BoneId)
			# 0-999
			self.ChildObjectId = rw.rw_uint32(self.ChildObjectId)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# -99999 to +99999
			self.RelativeXPosition = rw.rw_float32(self.RelativeXPosition)
			self.RelativeYPosition = rw.rw_float32(self.RelativeYPosition)
			self.RelativeZPosition = rw.rw_float32(self.RelativeZPosition)

			# -180 to +180
			self.XRotation = rw.rw_float32(self.XRotation)
			self.YRotation = rw.rw_float32(self.YRotation)
			self.ZRotation = rw.rw_float32(self.ZRotation)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			for unused in self.UNUSED:
				assert unused == 0


	# Model: Attachment Offset
	class MAtO(Serializable):

		def __init__(self):
			self.ChildObjectId = None

			self.XShift = None
			self.YShift = None
			self.ZShift = None

			self.XRotation = None
			self.YRotation = None
			self.ZRotation = None

			self.InterpolationType = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# 0-999
			self.ChildObjectId = rw.rw_uint32(self.ChildObjectId)

			# -99999 to +99999
			self.XShift = rw.rw_float32(self.XShift)
			self.YShift = rw.rw_float32(self.YShift)
			self.ZShift = rw.rw_float32(self.ZShift)

			# -180 to +180
			self.XRotation = rw.rw_float32(self.XRotation)
			self.YRotation = rw.rw_float32(self.YRotation)
			self.ZRotation = rw.rw_float32(self.ZRotation)

			# 0 = Linear, 1 = Step, 4354 = Hermitian (why not 2????? beats me)
			self.InterpolationType = rw.rw_uint32(self.InterpolationType)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])

			for unused in self.UNUSED:
				assert unused == 0


	# Model: Shadow Color
	class MCSd(Serializable):

		def __init__(self):
			self.UnkEnum = None
			self.RGBA1 = None
			self.RGBA2 = None
			self.UnkInd1 = None
			self.UnkInd2 = None
			self.UNUSED  = [None]*4

		def __rw_hook__(self, rw, dataSize):

			# 0, 3
			self.UnkEnum = rw.rw_uint32(self.UnkEnum)

			#with EndiannessManager(rw, ">"):
			# seems like the mode/default = 0, 0, 0, 128
			self.RGBA1 = rw.rw_uint8s(self.RGBA1, 4)
			#self.RGBA1 = rw.rw_uint32(self.RGBA1)
			# seems like the mode/default = 0, 0, 0, 96
			self.RGBA2 = rw.rw_uint8s(self.RGBA2, 4)
			#self.RGBA2 = rw.rw_uint32(self.RGBA2)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# seems like the mode/default = 20
			self.UnkInd1 = rw.rw_uint16(self.UnkInd1)
			# seems like the mode/default = 40
			self.UnkInd2 = rw.rw_uint16(self.UnkInd2)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])

			for unused in self.UNUSED:
				assert unused == 0


	# Model: Detachment
	class MDt_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.RemainInSceneAfterDetach = None
			self.UnkBool = None

			self.BoneId = None
			self.ChildObjectId = None

			self.XPosition = None
			self.YPosition = None
			self.ZPosition = None

			self.XRotation = None
			self.YRotation = None
			self.ZRotation = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			# 3, 11, 19, 27
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# for some reason these are always both 1... except in aaaancient beta EVTs that don't open properly
			#assert self.Bitfield & 0x1 and (self.Bitfield >> 1) & 0x1
			self.RemainInSceneAfterDetach = (self.Bitfield >> 3) & 0x1
			self.UnkBool = (self.Bitfield >> 4) & 0x1

			# 0-9999
			self.BoneId = rw.rw_uint32(self.BoneId)
			# 0-999
			self.ChildObjectId = rw.rw_uint32(self.ChildObjectId)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# after detach, assuming item remains in scene
			# -99999 to +99999
			self.XPosition = rw.rw_float32(self.XPosition)
			self.YPosition = rw.rw_float32(self.YPosition)
			self.ZPosition = rw.rw_float32(self.ZPosition)

			# -180 to +180
			self.XRotation = rw.rw_float32(self.XRotation)
			self.YRotation = rw.rw_float32(self.YRotation)
			self.ZRotation = rw.rw_float32(self.ZRotation)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			for unused in self.UNUSED:
				assert unused == 0


	# Model: Footsteps
	class MFts(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.Disable = None
			self.AreaDistortion = None
			self.PuddleEffect = None
			#self.UnkBool1 = None
			#self.UnkBool2 = None
			#self.UnkBool3 = None

			self.Strength = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			# 0, 1, 2, 6; beta version has 31 and 63
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.Disable = self.Bitfield & 0x1
			self.AreaDistortion = (self.Bitfield >> 1) & 0x1
			self.PuddleEffect = (self.Bitfield >> 2) & 0x1
			# only in one unused and very old event in the beta, so probably not worth much
			#self.UnkBool1 = (self.Bitfield >> 3) & 0x1
			#self.UnkBool2 = (self.Bitfield >> 4) & 0x1
			#self.UnkBool3 = (self.Bitfield >> 5) & 0x1

			# 0-1; always zero i.e. seemingly unused in beta
			self.Strength = rw.rw_float32(self.Bitfield)
			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# Model: ???
	# truly i have no idea here... only in royal, and barely if ever gets used -- seems like all instances are in unused events
	class MGd_(Serializable):

		def __init__(self):
			self.UNK = None

		def __rw_hook__(self, rw, dataSize):
			self.UNK = rw.rw_uint8s(self.UNK, dataSize)


	# Model: Icon
	class MIc_(Serializable):

		def __init__(self):
			self.IconType = None
			self.IconSize = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])

			# 0 = None, 1-28
			self.IconType = rw.rw_int32(self.IconType)
			# 0 = Normal/x1.0, 1 = Small/x0.7, 2 = Large/x1.5, 3 = XLarge/x2.0
			self.IconSize = rw.rw_int32(self.IconSize)

			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])

			for i in range(len(self.UNUSED)):
				assert self.UNUSED[i] == 0


	# Model: Lighting
	class ML__(Serializable):

		def __init__(self):

			self.Display = None
			self.Unk2 = None

			self.AmbientRGBA = None
			self.DiffuseRGBA = None
			self.SpecularRGBA = None

			self.Direction = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):

			# boolean
			self.Display = rw.rw_uint32(self.Display)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 191, 191, 191, 255
			#self.AmbientRGBA = rw.rw_uint8s(self.AmbientRGBA, 4)
			self.AmbientRGBA = rw.rw_uint32(self.AmbientRGBA)
			# default = 229, 229, 229, 255
			#self.DiffuseRGBA = rw.rw_uint8s(self.DiffuseRGBA, 4)
			self.DiffuseRGBA = rw.rw_uint32(self.DiffuseRGBA)
			# default = 255, 255, 255, 255
			#self.SpecularRGBA = rw.rw_uint8s(self.SpecularRGBA, 4)
			self.SpecularRGBA = rw.rw_uint32(self.SpecularRGBA)

			# -1 to 1
			self.Direction = rw.rw_float32s(self.Direction, 3)

			for i in range(2, 4):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	class MLa_(Serializable):

		def __init__(self):
			self.ResetEyeWhenMoving = None
			self.Bitfield = None
			self.EyeIsMovable = None
			self.HeadIsMovable = None
			self.TorsoIsMovable = None
			self.SlowDownTorso = None
			self.UnkBool = None

			self.MotionType = None
			self.SpeedType = None
			self.TargetType = None
			self.TargetCoordinates = None
			self.TargetModelID = None
			self.TargetBoneID = None

			self.UNUSED = [None]*1

		def __rw_hook__(self, rw, dataSize):
			self.ResetEyeWhenMoving = rw.rw_uint16(self.ResetEyeWhenMoving)
			self.Bitfield = rw.rw_uint16(self.Bitfield)
			self.EyeIsMovable = self.Bitfield & 0x1
			self.HeadIsMovable = (self.Bitfield >> 1) & 0x1
			self.TorsoIsMovable = (self.Bitfield >> 2) & 0x1
			assert (self.Bitfield >> 3) & 0x1 == 0
			assert (self.Bitfield >> 4) & 0x1 == 0
			self.SlowDownTorso = (self.Bitfield >> 5) & 0x1
			#assert (self.Bitfield >> 6) & 0x1 == 0
			# seems like royal-only, or at least not in beta
			self.UnkBool = (self.Bitfield >> 6) & 0x1
			assert (self.Bitfield >> 7) & 0x1 == 0

			# 0 = LookAtControl, 1 = ResetMotion, 2 = NoddingMotion, 3 = ShakeMotion, 4 = ???
			self.MotionType = rw.rw_int16(self.MotionType)   # values: 0-4
			# 0 = Direct, 1 = Slow, 2 = Middle, 3 = Fast; default = 2/Middle
			self.SpeedType = rw.rw_int16(self.SpeedType)   # values: 0-3

			self.UNUSED[0] = rw.rw_int16(self.UNUSED[0]) # values: 0-3
			#assert self.UNUSED[0] == 0

			# 0 = None, 1 = Reset, 2 = Coordinates, 3 = Helper/Bone
			self.TargetType = rw.rw_int16(self.TargetType)
			# -99999 to +99999
			self.TargetCoordinates = rw.rw_float32s(self.TargetCoordinates, 3)
			# 0-999
			self.TargetModelID = rw.rw_int32(self.TargetModelID)
			# 0-9999
			self.TargetBoneID = rw.rw_int32(self.TargetBoneID)


	# Model: Load
	# (not particularly used, tbh)
	class MLd_(Serializable):

		def __init__(self):
			self.UNUSED = None

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED = rw.rw_uint32s(self.UNUSED, 4)
			for unused in self.UNUSED:
				assert unused == 0


	# Model: Look Away (Look Around)
	class MLw_(Serializable):

		def __init__(self):
			self.EnableUpperBodyRotation = None

			self.TopLimitAngle = None
			self.BottomLimitAngle = None
			self.LeftLimitAngle = None
			self.RightLimitAngle = None

			self.UpdateIntervalMinimumFrameValue = None
			self.UpdateIntervalRandomFrame = None

			self.UNUSED = [None]

		def __rw_hook__(self, rw, dataSize):
			# default = true
			self.EnableUpperBodyRotation = rw.rw_uint32(self.EnableUpperBodyRotation)

			# all in degrees, it seems
			# 0-30; default = 5
			self.TopLimitAngle = rw.rw_float32(self.TopLimitAngle)
			# 0-30; default = 5
			self.BottomLimitAngle = rw.rw_float32(self.BottomLimitAngle)
			# 0-50; default = 15
			self.LeftLimitAngle = rw.rw_float32(self.LeftLimitAngle)
			# 0-50; default = 15
			self.RightLimitAngle = rw.rw_float32(self.RightLimitAngle)

			# 1-300; default = 150
			self.UpdateIntervalMinimumFrameValue = rw.rw_uint32(self.UpdateIntervalMinimumFrameValue)
			# 0-300; default = 60
			self.UpdateIntervalRandomFrame = rw.rw_uint32(self.UpdateIntervalRandomFrame)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0


	class MMD_(Serializable):

		def __init__(self):
			self.InterpolationType = None
			self.NumControlGroups = None
			self.TargetPositions = [None]*24

			self.Bitfield = None
			self.MovingAnimationDisabled = None
			self.WaitingAnimationDisabled = None
			self.MovingAnimationFromExt = None
			self.WaitingAnimationFromExt = None
			self.DisableOrientationChange = None
			self.MovementLoopBool = None

			self.MovementSpeed = None
			self.UNK = None

			self.StartSpeedType = None
			self.FinalSpeedType = None

			self.MovingAnimationID = None
			self.MovingAnimationInterpolatedFrames = None
			self.MovingAnimationLoopBool = None
			self.MovingAnimationPlaybackSpeed = None
			self.MovingAnimationStartingFrame = None

			self.WaitingAnimationID = None
			self.WaitingAnimationInterpolatedFrames = None
			self.WaitingAnimationLoopBool = None
			self.WaitingAnimationPlaybackSpeed = None
			self.WaitingAnimationStartingFrame = None

			self.UNUSED = [None]*9

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 96 or dataSize == 384

			# 0 = Linear, 1 = BezierCurve
			self.InterpolationType = rw.rw_uint32(self.InterpolationType)
			# 1-8; default = 1 (actually i think it goes up to 24, no? maybe that came after the editor, idfk)
			self.NumControlGroups = rw.rw_uint32(self.NumControlGroups)

			if dataSize == 384:
				for i in range(24):
					# -99999 to +99999; seem to form a straight line toward whatever direction the model is facing
					self.TargetPositions[i] = rw.rw_float32s(self.TargetPositions[i], 3)

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.MovingAnimationDisabled = self.Bitfield & 0x1
			self.WaitingAnimationDisabled = (self.Bitfield >> 1) & 0x1
			self.MovingAnimationFromExt = (self.Bitfield >> 2) & 0x1
			self.WaitingAnimationFromExt = (self.Bitfield >> 3) & 0x1
			self.DisableOrientationChange = (self.Bitfield >> 4) & 0x1
			self.MovementLoopBool = (self.Bitfield >> 5) & 0x1

			# 1-50; default = 1
			self.MovementSpeed = rw.rw_float32(self.MovementSpeed)
			self.UNK = rw.rw_uint32(self.UNK)

			# 0 = Fixed, 1 = Running, 2 = Walking
			self.StartSpeedType = rw.rw_uint8(self.StartSpeedType)
			self.FinalSpeedType = rw.rw_uint8(self.FinalSpeedType)

			self.UNUSED[8] = rw.rw_uint16(self.UNUSED[8])

			# 0-59
			self.MovingAnimationID = rw.rw_uint32(self.MovingAnimationID)
			# 0-100
			self.MovingAnimationInterpolatedFrames = rw.rw_uint32(self.MovingAnimationInterpolatedFrames)
			# default = true
			self.MovingAnimationLoopBool = rw.rw_uint32(self.MovingAnimationLoopBool)
			# 0-10; default = 1
			self.MovingAnimationPlaybackSpeed = rw.rw_float32(self.MovingAnimationPlaybackSpeed)
			# 0-99999
			self.MovingAnimationStartingFrame = rw.rw_uint32(self.MovingAnimationStartingFrame)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			# 0-59
			self.WaitingAnimationID = rw.rw_uint32(self.WaitingAnimationID)
			# 0-100
			self.WaitingAnimationInterpolatedFrames = rw.rw_uint32(self.WaitingAnimationInterpolatedFrames)
			# default = true
			self.WaitingAnimationLoopBool = rw.rw_uint32(self.WaitingAnimationLoopBool)
			# 0-10; default = 1
			self.WaitingAnimationPlaybackSpeed = rw.rw_float32(self.WaitingAnimationPlaybackSpeed)
			# 0-99999
			self.WaitingAnimationStartingFrame = rw.rw_uint32(self.WaitingAnimationStartingFrame)

			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])
			self.UNUSED[4] = rw.rw_uint32(self.UNUSED[4])
			self.UNUSED[5] = rw.rw_uint32(self.UNUSED[5])
			self.UNUSED[6] = rw.rw_uint32(self.UNUSED[6])
			self.UNUSED[7] = rw.rw_uint32(self.UNUSED[7])

			#for i in range(len(self.UNUSED)):
			#	assert self.UNUSED[i] == 0


	# Model: Register
	class MRgs(Serializable):

		def __init__(self):
			self.DisplayType = None
			self.Scene = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			# 0 = None, 1 = On, 2 = Off
			self.DisplayType = rw.rw_uint32(self.DisplayType)
			# 0 = Scene 0, 1 = Scene 1 (but it's always 0 so idfk what this means)
			self.Scene = rw.rw_uint32(self.Scene)
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			for unused in self.UNUSED:
				assert unused == 0


	# Model: Rotate
	class MRot(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.YawEnabled = None
			self.PitchEnabled = None
			self.RollEnabled = None
			self.RotatingAnimationEnabled = None
			self.WaitingAnimationEnabled = None
			self.RotatingAnimationFromExt = None
			self.WaitingAnimationFromExt = None
			#self.AutomaticRotationParametersEnabled = None
			self.CustomRotationAnimationsEnabled = None

			#self.Rotation = None
			self.Yaw = None
			self.Pitch = None
			self.Roll = None
			self.InterpolationType = None

			self.UNK = None

			self.RotatingAnimationID = None
			self.RotatingAnimationInterpolatedFrames = None
			self.RotatingAnimationLoopBool = None
			self.RotatingAnimationPlaybackSpeed = None
			self.RotatingAnimationStartingFrame = None

			self.WaitingAnimationID = None
			self.WaitingAnimationInterpolatedFrames = None
			self.WaitingAnimationLoopBool = None
			self.WaitingAnimationPlaybackSpeed = None
			self.WaitingAnimationStartingFrame = None

			self.UNUSED = [None]*8

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			# default = 1
			self.YawEnabled = self.Bitfield & 0x1
			self.PitchEnabled = (self.Bitfield >> 1) & 0x1
			self.RollEnabled = (self.Bitfield >> 2) & 0x1
			self.RotatingAnimationEnabled = (self.Bitfield >> 4) & 0x1
			self.WaitingAnimationEnabled = (self.Bitfield >> 5) & 0x1
			self.RotatingAnimationFromExt = (self.Bitfield >> 6) & 0x1
			self.WaitingAnimationFromExt = (self.Bitfield >> 7) & 0x1
			#self.AutomaticRotationParametersEnabled = (self.Bitfield >> 12) & 0x1
			self.CustomRotationAnimationsEnabled = (self.Bitfield >> 12) & 0x1

			#self.Rotation = rw.rw_float32s(self.Rotation, 3)
			# -180 to +180
			self.Yaw = rw.rw_float32(self.Yaw)
			self.Pitch = rw.rw_float32(self.Pitch)
			self.Roll = rw.rw_float32(self.Roll)

			# 0 = Linear, 4354 = Slow-to-Slow Hermite, 4610 = Fast-to-Slow Hermite, 8450 = Slow-to-Fast Hermite
			self.InterpolationType = rw.rw_uint32(self.InterpolationType)

			self.UNK = rw.rw_int32(self.UNK)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])

			# 0-59
			self.RotatingAnimationID = rw.rw_uint32(self.WaitingAnimationID)
			# 0-100
			self.RotatingAnimationInterpolatedFrames = rw.rw_uint32(self.WaitingAnimationInterpolatedFrames)
			self.RotatingAnimationLoopBool = rw.rw_uint32(self.WaitingAnimationLoopBool)
			# 0-10; default = 1
			self.RotatingAnimationPlaybackSpeed = rw.rw_float32(self.WaitingAnimationPlaybackSpeed)
			# 0-99999
			self.RotatingAnimationStartingFrame = rw.rw_uint32(self.WaitingAnimationStartingFrame)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])
			self.UNUSED[4] = rw.rw_uint32(self.UNUSED[4])

			# 0-59
			self.WaitingAnimationID = rw.rw_uint32(self.WaitingAnimationID)
			# 0-100
			self.WaitingAnimationInterpolatedFrames = rw.rw_uint32(self.WaitingAnimationInterpolatedFrames)
			self.WaitingAnimationLoopBool = rw.rw_uint32(self.WaitingAnimationLoopBool)
			# 0-10; default = 1
			self.WaitingAnimationPlaybackSpeed = rw.rw_float32(self.WaitingAnimationPlaybackSpeed)
			# 0-99999
			self.WaitingAnimationStartingFrame = rw.rw_uint32(self.WaitingAnimationStartingFrame)

			self.UNUSED[5] = rw.rw_uint32(self.UNUSED[5])
			self.UNUSED[6] = rw.rw_uint32(self.UNUSED[6])
			self.UNUSED[7] = rw.rw_uint32(self.UNUSED[7])

			for unused in self.UNUSED:
				assert unused == 0


	# Model: Scale
	class MScl(Serializable):

		def __init__(self):
			self.Unk = None
			self.Scale = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			# always 4354
			self.Unk = rw.rw_uint32(self.Unk)
			# 0-3; default = 1
			self.Scale = rw.rw_float32(self.Scale)
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])


	# Model: Placement
	class MSD_(Serializable):

		def __init__(self):
			self.Position = None
			self.Rotation = None

			self.WaitingAnimationID = None
			self.WaitingAnimationInterpolatedFrames = None
			self.WaitingAnimationLoopBool = None
			self.WaitingAnimationPlaybackSpeed = None

			self.Bitfield = None
			self.DisableWaitingAnimation = None
			self.DisableRotation = None
			self.WaitingAnimationFromExt = None

			self.WaitingAnimationStartingFrame = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 48 or dataSize == 64

			# -99999 to +99999
			self.Position = rw.rw_float32s(self.Position, 3)
			# -180 to +180
			self.Rotation = rw.rw_float32s(self.Rotation, 3)

			# 0-59
			self.WaitingAnimationID = rw.rw_uint32(self.WaitingAnimationID)
			# 0-100
			self.WaitingAnimationInterpolatedFrames = rw.rw_uint32(self.WaitingAnimationInterpolatedFrames)
			# default = 1; one time it's 3274084084 ???? i think that's corrupted data bc wtf...
			self.WaitingAnimationLoopBool = rw.rw_uint32(self.WaitingAnimationLoopBool)
			# 0-10; default = 1
			self.WaitingAnimationPlaybackSpeed = rw.rw_float32(self.WaitingAnimationPlaybackSpeed)

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.DisableWaitingAnimation = self.Bitfield & 0x1
			self.DisableRotation = (self.Bitfield >> 1) & 0x1
			self.WaitingAnimationFromExt = (self.Bitfield >> 2) & 0x1

			# 0-99999
			self.WaitingAnimationStartingFrame = rw.rw_uint32(self.WaitingAnimationStartingFrame)

			if dataSize == 64:
				for i in range(4):
					self.UNUSED[i] = rw.rw_int32(self.UNUSED[i])
					#assert self.UNUSED[i] == 0


	# Message: Select
	# never used ever lol
	class MSel(Serializable):

		def __init__(self):
			self.LabelNumber = None
			self.ChoiceCount = None
			self.ModelNumber = None
			self.BackgroundNumber = None
			self.LocalDataNumber = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			# -1 to 999; default = -1
			self.LabelNumber = rw.rw_int32(self.LabelNumber)
			# 1-4; default = 4
			self.ChoiceCount = rw.rw_uint32(self.ChoiceCount)
			# 0-30
			self.ModelNumber = rw.rw_uint32(self.ModelNumber)
			# 0-30
			self.BackgroundNumber = rw.rw_uint32(self.BackgroundNumber)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# 0-15
			self.LocalDataNumber = rw.rw_uint32(self.LocalDataNumber)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

	# Message: IDs
	class Msg_(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.NormalMessageEnabled = None
			self.SelectionEnabled = None
			self.DisplayAsSubtitle = None
			self.UnkBool1 = None
			self.UnkBool2 = None
			self.UnkBool3 = None
			self.SpecifyLabelByIndex = None

			self.MessageMajorId = None
			self.MessageMinorId = None
			self.MessageSubId = None

			# Select/Choice... which is nicer wording...?
			self.SelectMajorId = None
			self.SelectMinorId = None
			self.SelectSubId = None

			self.EvtLocalDataIdSelStorage = None
			self.MessageCoordinateType = None
			self.MessageCoordinates = None
			self.UnkFloat = None

			self.UnkBitfield = None
			self.EntryBools = [None]*14
			self.UnkBool4 = None
			self.UnkBool5 = None
			self.UnkBool6 = None
			self.UnkBool7 = None
			self.UnkBool8 = None

			self.UnkEnum = None
			self.UnkBool9 = None
			self.UnkBool10 = None
			self.UnkBool11 = None

			self.EntryCount = None
			##self.Entries = list()
			#self.Entries = [list(), list(), list()]
			self.Entries1 = [None]*14
			self.Entries2 = [None]*14
			self.Entries3 = [None]*14

			self.RoyalUnkFloats = None

			self.UNUSED = [None]*4

		def __rw_hook__(self, rw, dataSize):
			#assert dataSize == 16 or dataSize == 32 or dataSize == 160 or dataSize == 176
			with rw.relative_origin():
				self.Bitfield = rw.rw_uint32(self.Bitfield)
				self.NormalMessageEnabled = self.Bitfield & 0x1
				self.SelectionEnabled = (self.Bitfield >> 1) & 0x1
				self.DisplayAsSubtitle = (self.Bitfield >> 2) & 0x1
				self.UnkBool1 = (self.Bitfield >> 4) & 0x1
				self.UnkBool2 = (self.Bitfield >> 5) & 0x1
				self.UnkBool3 = (self.Bitfield >> 8) & 0x1
				# unused in royal; used in beta (possible predates MsgR; seems old)
				self.SpecifyLabelByIndex = (self.Bitfield >> 31) & 0x1

				# 0-999
				self.MessageMajorId = rw.rw_uint16(self.MessageMajorId)
				# 0-9
				self.MessageMinorId = rw.rw_uint8(self.MessageMinorId)
				# 0-9
				self.MessageSubId = rw.rw_uint8(self.MessageSubId)

				# 0-999
				self.SelectMajorId = rw.rw_uint16(self.SelectMajorId)
				# 0-9
				self.SelectMinorId = rw.rw_uint8(self.SelectMinorId)
				# 0-9
				self.SelectSubId = rw.rw_uint8(self.SelectSubId)

				# 0-15
				self.EvtLocalDataIdSelStorage = rw.rw_uint32(self.EvtLocalDataIdSelStorage)

				if dataSize > 16:
					# 0 = UpperLeft, 1 = UpperCenter, 2 = UpperRight, 3 = LowerLeft, 4 = LowerCenter, 5 = LowerRight; default = 4/BottomCenter
					self.MessageCoordinateType = rw.rw_uint32(self.MessageCoordinateType)
					# -9999 to +9999; default = 375, 528
					self.MessageCoordinates = rw.rw_float32s(self.MessageCoordinates, 2)
					self.UnkFloat = rw.rw_float32(self.UnkFloat)
					if dataSize > 32:
						self.UnkBitfield = rw.rw_uint32(self.UnkBitfield)
						for i in range(14):
							self.EntryBools[i] = (self.UnkBitfield >> i) & 0x1
						self.UnkBool4 = (self.UnkBitfield >> 20) & 0x1
						self.UnkBool5 = (self.UnkBitfield >> 21) & 0x1
						self.UnkBool6 = (self.UnkBitfield >> 22) & 0x1
						self.UnkBool7 = (self.UnkBitfield >> 23) & 0x1
						self.UnkBool8 = (self.UnkBitfield >> 24) & 0x1
						self.UnkEnum = rw.rw_uint32(self.UnkEnum)
						self.UnkBool9 = self.UnkEnum & 0x1
						self.UnkBool10 = (self.UnkEnum >> 1) & 0x1
						self.UnkBool11 = (self.UnkEnum >> 2) & 0x1
						self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
						self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
						for i in range(14):
							# default = -1
							self.Entries1[i] = rw.rw_int16(self.Entries1[i])
							# default = 10
							self.Entries2[i] = rw.rw_int16(self.Entries2[i])
							# default = 1.0
							self.Entries3[i] = rw.rw_float32(self.Entries3[i])
							"""#self.Entries[i][2] = rw.rw_uint16s(self.Entries[i][2], 2)
							if rw.is_constructlike: # reader
								self.Entries.append(None)
							#self.Entries[i] = rw.rw_int8s(self.Entries[i], 8)
							#self.Entries[i] = rw.rw_int16s(self.Entries[i], 4)
							#self.Entries[i] = rw.rw_int32s(self.Entries[i], 2)
							self.Entries[i] = rw.rw_uint64(self.Entries[i])"""
						if dataSize > 160:
							self.RoyalUnkFloats = rw.rw_float32s(self.RoyalUnkFloats, 2)
							self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
							self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])


	# Message: Reference
	class MsgR(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.NormalMessageEnabled = None
			self.SelectionEnabled = None
			self.UnkBool1 = None
			self.UnkBool2 = None

			self.MessageIndex = None
			self.SelIndex = None
			self.EvtLocalDataIdSelStorage = None

			self.MessageCoordinateType = None
			self.MessageCoordinates = None
			self.UnkFloat = None

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 16 or dataSize == 32

			self.Bitfield = rw.rw_int32(self.Bitfield)
			self.NormalMessageEnabled = self.Bitfield & 0x1
			self.SelectionEnabled = (self.Bitfield >> 1) & 0x1
			self.UnkBool1 = (self.Bitfield >> 5) & 0x1
			self.UnkBool2 = (self.Bitfield >> 8) & 0x1

			# 0-999
			self.MessageIndex = rw.rw_int32(self.MessageIndex)
			# 0-999
			self.SelIndex = rw.rw_int32(self.SelIndex)

			# 0-15
			self.EvtLocalDataIdSelStorage = rw.rw_int32(self.EvtLocalDataIdSelStorage)

			if dataSize > 16:
				# 0 = UpperLeft, 1 = UpperCenter, 2 = UpperRight, 3 = LowerLeft, 4 = LowerCenter, 5 = LowerRight; default = 4/BottomCenter
				self.MessageCoordinateType = rw.rw_uint32(self.MessageCoordinateType)
				# -9999 to +9999; default = 375, 528
				self.MessageCoordinates = rw.rw_float32s(self.MessageCoordinates, 2)
				self.UnkFloat = rw.rw_float32(self.UnkFloat)


	class MSSs(Serializable):

		def __init__(self):
			self.ActiveShoeNode = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# valid values: 1-4; observed values: 1-2
			self.ActiveShoeNode = rw.rw_uint32(self.ActiveShoeNode)
			assert self.ActiveShoeNode >= 1 and self.ActiveShoeNode <= 4

			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_int32(self.UNUSED[2])

			for i in range(len(self.UNUSED)):
				assert self.UNUSED[i] == 0


	"""class MvCt(Serializable):

		def __init__(self):
			self.UnkEnum = None
			self.Frame = None

			#self.UnkBitfield1 = None
			self.Thing1 = None
			self.Thing2 = None
			self.UNUSED = None

			self.UnkBitfield2 = None

		def __rw_hook__(self, rw, dataSize):
			# 0-3
			self.UnkEnum = rw.rw_uint32(self.UnkEnum)

			self.Frame = rw.rw_uint32(self.Frame)

			#with EndiannessManager(rw, "<"):
			#self.UnkBitfield1 = rw.rw_uint8s(self.UnkBitfield1, 4)
			self.Thing1 = rw.rw_uint8(self.Thing1)
			self.Thing2 = rw.rw_uint8(self.Thing2)

			self.UNUSED = rw.rw_uint16(self.UNUSED)
			assert self.UNUSED == 0

			self.UnkBitfield2 = rw.rw_uint8s(self.UnkBitfield2, 4)"""


	class MvCt(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.DisableFrameLock = None
			self.LoopPlayback = None

			self.LinkedAssetID = None

			self.Thing1 = None
			self.Thing2 = None
			self.UNUSED = None

			self.LoopStartFrame = None

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.DisableFrameLock = self.Bitfield & 0x1
			self.LoopPlayback = (self.Bitfield >> 1) & 0x1

			self.LinkedAssetID = rw.rw_uint32(self.LinkedAssetID)

			#self.UNUSED = rw.rw_uint32(self.UNUSED)
			#assert self.UNUSED == 0
			self.Thing1 = rw.rw_uint8(self.Thing1)
			self.Thing2 = rw.rw_uint8(self.Thing2)

			self.UNUSED = rw.rw_uint16(self.UNUSED)
			assert self.UNUSED == 0

			self.LoopStartFrame = rw.rw_uint32(self.LoopStartFrame)


	class MvPl(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.DisableFrameLock = None
			self.LoopPlayback = None

			self.LinkedAssetID = None
			self.LoopStartFrame = None

			self.UNUSED = None

		def __rw_hook__(self, rw, dataSize):
			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.DisableFrameLock = self.Bitfield & 0x1
			self.LoopPlayback = (self.Bitfield >> 1) & 0x1

			self.LinkedAssetID = rw.rw_uint32(self.LinkedAssetID)

			self.UNUSED = rw.rw_uint32(self.UNUSED)
			assert self.UNUSED == 0

			self.LoopStartFrame = rw.rw_uint32(self.LoopStartFrame)


	# distortion blur... texture blur?
	class PBDs(Serializable):

		def __init__(self):

			self.StartFrame = None
			self.EndFrame = None
			self.Unk1 = None
			self.Unk2 = None

			self.Strength1 = None
			self.U1 = None
			self.V1 = None

			self.Strength2 = None
			self.U2 = None
			self.V2 = None

			self.BlendType = None
			self.RGBA = None
			self.TextureAssetID = None
			self.IntervalFrames = None
			self.Unk3 = None

			self.UNUSED = [None]*6

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0-60
			self.StartFrame = rw.rw_uint16(self.StartFrame)
			# 0-60
			self.EndFrame = rw.rw_uint16(self.EndFrame)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			# 0-50; default = 5
			self.Strength1 = rw.rw_float32(self.Strength1)
			# -1 to 1; default = 0.13
			self.U1 = rw.rw_float32(self.U1)
			# -1 to 1; default = 0.2
			self.V1 = rw.rw_float32(self.V1)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0

			# 0-50; default = 5
			self.Strength2 = rw.rw_float32(self.Strength2)
			# -1 to 1; default = -0.28
			self.U2 = rw.rw_float32(self.U2)
			# -1 to 1; default = 0.26
			self.V2 = rw.rw_float32(self.V2)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			assert self.UNUSED[2] == 0

			# 0 = Opaque, 1 = Translucent, 2 = AdditiveTranslucent, 3 = SubtractiveTranslucent, 4 = MultiplicativeTranslucent, 5 = 2xMultiplicativeTranslucent
			self.BlendType = rw.rw_uint32(self.BlendType)
			# shown in editor as HSL + alpha but stored as RGBA
			# default = 255, 255, 255, 128
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)
			# 0-999
			self.TextureAssetID = rw.rw_uint32(self.TextureAssetID)
			# 0-60
			self.IntervalFrames = rw.rw_uint32(self.IntervalFrames)
			# always 4354
			self.Unk3 = rw.rw_uint32(self.Unk3)

			for i in range(3, 6):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# noise blur
	class PBNs(Serializable):

		def __init__(self):

			self.StartFrame = None
			self.EndFrame = None
			self.Unk1 = None
			self.Unk2 = None

			self.Scale = None
			self.Strength = None

			self.BlendType = None
			self.RGBA = None

			self.ScaleFrames = None
			self.Unk3 = None
			self.StrengthFrames = None
			self.Unk4 = None

			self.UNUSED = [None]*1

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0-60
			self.StartFrame = rw.rw_uint16(self.StartFrame)
			# 0-60
			self.EndFrame = rw.rw_uint16(self.EndFrame)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			# 0-10
			self.Scale = rw.rw_float32(self.Scale)
			# 0-50; default = 5
			self.Strength = rw.rw_float32(self.Strength)

			# 0 = Opaque, 1 = Translucent, 2 = AdditiveTranslucent, 3 = SubtractiveTranslucent, 4 = MultiplicativeTranslucent, 5 = 2xMultiplicativeTranslucent
			self.BlendType = rw.rw_uint32(self.BlendType)

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 255, 255, 255, 128
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)

			# 0-60
			self.ScaleFrames = rw.rw_uint32(self.ScaleFrames)
			# always 4354
			self.Unk3 = rw.rw_uint32(self.Unk3)
			# 0-60
			self.StrengthFrames = rw.rw_uint32(self.StrengthFrames)
			# always 4354
			self.Unk4 = rw.rw_uint32(self.Unk4)


	# radial blur
	class PBRd(Serializable):

		def __init__(self):

			self.StartFrame = None
			self.EndFrame = None
			self.Unk1 = None
			self.Unk2 = None

			self.Coordinates = None
			self.Strength = None
			self.Attenuation = None

			self.BlendType = None
			self.RGBA = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# 0-60
			self.StartFrame = rw.rw_uint16(self.StartFrame)
			# 0-60
			self.EndFrame = rw.rw_uint16(self.EndFrame)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			# X, Y; both -1 through +1
			self.Coordinates = rw.rw_float32s(self.Coordinates, 2)
			# 0-50; default = 5
			self.Strength = rw.rw_float32(self.Strength)
			# 0-2000
			self.Attenuation = rw.rw_float32(self.Attenuation)

			# 0 = Opaque, 1 = Translucent, 2 = AdditiveTranslucent, 3 = SubtractiveTranslucent, 4 = MultiplicativeTranslucent, 5 = 2xMultiplicativeTranslucent; default = 1/Translucent
			self.BlendType = rw.rw_uint32(self.BlendType)

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 255, 255, 255, 128
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			for unused in self.UNUSED:
				assert unused == 0


	# linear blur (motion blur?)
	class PBSt(Serializable):

		def __init__(self):

			self.StartFrame = None
			self.EndFrame = None
			self.Unk1 = None
			self.Unk2 = None

			self.Direction = None
			self.Strength = None

			self.BlendType = None
			self.RGBA = None

			self.UNUSED = [None]*1

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0-60
			self.StartFrame = rw.rw_uint16(self.StartFrame)
			# 0-60
			self.EndFrame = rw.rw_uint16(self.EndFrame)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			# 0-360... in the UI... but stored here as radians (/ 57.29578 relative to what's shown in UI, so 0-2*pi)
			self.Direction = rw.rw_float32(self.Direction)
			# 0-50; default = 5
			self.Strength = rw.rw_float32(self.Strength)

			# 0 = Opaque, 1 = Translucent, 2 = AdditiveTranslucent, 3 = SubtractiveTranslucent, 4 = MultiplicativeTranslucent, 5 = 2xMultiplicativeTranslucent
			self.BlendType = rw.rw_uint32(self.BlendType)

			# shown in editor as HSL + alpha but stored as RGBA
			# default = 255, 255, 255, 128
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)


	# color correction
	class PCc_(Serializable):

		def __init__(self):

			self.StartFrame = None
			self.EndFrame = None
			self.Unk1 = None
			self.Unk2 = None

			self.Coordinates = None
			self.Dimensions = None

			self.CMY = None
			self.Dodge = None
			self.Burn = None
			self.Alpha = None

			self.TextureAssetID = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0-60
			self.StartFrame = rw.rw_uint16(self.StartFrame)
			# 0-60
			self.EndFrame = rw.rw_uint16(self.EndFrame)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			# X, Y; 0-1
			self.Coordinates = rw.rw_float32s(self.Coordinates, 2)
			# W, H; 0-1; default = 1
			self.Dimensions = rw.rw_float32s(self.Dimensions, 2)

			# -1 to 1
			self.CMY = rw.rw_float32s(self.CMY, 3)
			# 0-0.99
			self.Dodge = rw.rw_float32(self.Dodge)
			# 0-0.99
			self.Burn = rw.rw_float32(self.Burn)
			# 0-1
			self.Alpha = rw.rw_float32(self.Alpha)

			# 0-999
			self.TextureAssetID = rw.rw_uint32(self.TextureAssetID)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0


	class PCr_(Serializable):

		def __init__(self):

			self.Bitfield = None

			self.StartFrame = None
			self.EndFrame = None
			self.Unk1 = None
			self.Unk2 = None

			self.Coordinates = None
			self.LargeUnk = None
			self.SmallUnk = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):

			self.Bitfield = rw.rw_uint32(self.Bitfield)

			# 0-60
			self.StartFrame = rw.rw_uint16(self.StartFrame)
			# 0-60
			self.EndFrame = rw.rw_uint16(self.EndFrame)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			self.Coordinates = rw.rw_float32s(self.Coordinates, 2)
			self.LargeUnk = rw.rw_float32s(self.LargeUnk, 6)
			self.SmallUnk = rw.rw_float32s(self.SmallUnk, 6)

			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# lens flare
	class PLf_(Serializable):

		def __init__(self):

			self.LensFlareType = None
			self.LightSourceCoordinates = None
			self.RGBA = None
			self.LightSourceStrength = None
			self.FilterType = None

			#self.Bitfield = None
			self.ShowFilter = None
			self.DisplayGlowAtLightSourcePosition = None
			self.DisplayGlowNearCenterOfScreen = None
			self.UnkBool = None

			self.StartInterpolationFrame = None
			self.EndInterpolationFrame = None
			self.StartInterpolationType = None
			self.EndInterpolationType = None

			self.UnkInd = None
			self.UnkThing1 = None
			self.UnkThing2 = None

			self.UNUSED = [None]*1

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 48 or dataSize == 64

			# 0 = Normal, 1 = Night, 2 = ElectricEtc
			self.LensFlareType = rw.rw_uint32(self.LensFlareType)
			# -99999.9 to +99999.9; default X=0 Y=455.28 Z=910.56
			self.LightSourceCoordinates = rw.rw_float32s(self.LightSourceCoordinates, 3)
			# shown in editor as HSL + alpha but stored as RGBA
			# default = 255, 255, 255, 255
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)
			# 0-2; default = 1
			self.LightSourceStrength = rw.rw_float32(self.LightSourceStrength)
			# 0 = ScaryAtmosphere, 1 = LensDust
			self.FilterType = rw.rw_uint32(self.FilterType)

			self.ShowFilter = rw.rw_uint8(self.ShowFilter)
			self.DisplayGlowAtLightSourcePosition = rw.rw_uint8(self.DisplayGlowAtLightSourcePosition)
			self.DisplayGlowNearCenterOfScreen = rw.rw_uint8(self.DisplayGlowNearCenterOfScreen)
			self.UnkBool = rw.rw_uint8(self.UnkBool)

			# 0-60
			self.StartInterpolationFrame = rw.rw_uint32(self.StartInterpolationType)
			# 0-60
			self.EndInterpolationFrame = rw.rw_uint32(self.EndInterpolationType)
			# 0 = Linear, 4354 = HermiteSlowToSlow, 4610 = HermiteFastToSlow, 8450 = HermiteSlowToFast; default = 4354/HermiteSlowToSlow
			self.StartInterpolationType = rw.rw_uint32(self.StartInterpolationType)
			# 0 = Linear, 4354 = HermiteSlowToSlow, 4610 = HermiteFastToSlow, 8450 = HermiteSlowToFast; default = 4354/HermiteSlowToSlow
			self.EndInterpolationType = rw.rw_uint32(self.EndInterpolationType)

			if dataSize > 48:
				self.UnkInd = rw.rw_uint32(self.UnkInd)
				self.UnkThing1 = rw.rw_int16s(self.UnkThing1, 2)
				self.UnkThing2 = rw.rw_int16s(self.UnkThing2, 2)
				self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])


	class PMc_(Serializable):

		def __init__(self):

			self.StartFrame = None
			self.EndFrame = None
			self.Unk1 = None
			self.Unk2 = None

			self.UnkFloats = None

			self.UNUSED = [None]*5

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0-60
			self.StartFrame = rw.rw_uint16(self.StartFrame)
			# 0-60
			self.EndFrame = rw.rw_uint16(self.EndFrame)
			# always 4354
			self.Unk1 = rw.rw_uint32(self.Unk1)
			# always 4354
			self.Unk2 = rw.rw_uint32(self.Unk2)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0

			# 0-1
			self.UnkFloats = rw.rw_float32s(self.UnkFloats, 4)

			for i in range(2, 5):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	class PRum(Serializable):

		def __init__(self):
			self.RumblePreset = None
			self.FrameDuration = None
			self.RumbleStrength = None
			self.SmallMotorBool = None
			self.OnFrame = None
			self.OffFrame = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			# 0 = None, 1 = IM, 2 = Call
			# for IM preset: Duration=30, Strength=0, SmallMotor=1, OnFrame=6, OffFrame=12
			# for Call preset: Duration=30, Strength=0, SmallMotor=1, OnFrame=30, OffFrame=0
			self.RumblePreset = rw.rw_uint32(self.RumblePreset)
			# 0-500
			self.FrameDuration = rw.rw_uint32(self.FrameDuration)
			# 0-255; recommended > 64
			self.RumbleStrength = rw.rw_uint32(self.RumbleStrength)
			# 0, 1
			self.SmallMotorBool = rw.rw_uint32(self.SmallMotorBool)
			# 0-500
			self.OnFrame = rw.rw_uint32(self.OnFrame)
			# 0-500
			self.OffFrame = rw.rw_uint32(self.OffFrame)
			for i in range(2):
				self.UNUSED[i] = rw.rw_uint32(self.UNUSED[i])
				assert self.UNUSED[i] == 0


	# still not totally sure what this is...
	# value of 1 more common than value of 2
	# few events have these... but the ones that do have a lot of them!
	# tends to give bool == 1 for all indices first, then bool == 2 for all the same indices
	# so... it's enabling/disabling something for different objects?
	# ...hm, nope, the indices don't seem to be objectIds...
	# are they... field noise cues...? i think they must be
	# some of the indices baffle me and idk what the enum is but. maybe???
	# SoundBackgroundEffect...?
	# SoundBackgroundEnable?
	# Sound: Field Environment
	class SBE_(Serializable):

		def __init__(self):
			self.UnkBool = None
			self.Action = None
			self.CueId = None
			self.UNUSED = [None]

		def __rw_hook__(self, rw, dataSize):
			self.UnkBool = rw.rw_uint32(self.UnkBool)
			assert self.UnkBool == 0 or self.UnkBool == 1

			# 1 = Play, 2 = Stop
			self.Action = rw.rw_uint32(self.Action)
			assert self.Action == 1 or self.Action == 2

			self.CueId = rw.rw_uint32(self.CueId)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0


	# ...nor this. but presumably their enums are one and the same
	# value of 2 more common than value of 1
	# almost every event has one of these -- usually just one instance, but sometimes more
	# if this appears alone, it's basically guaranteed to have enum == 2
	# can occur throughout, but seem most common at frame 1 and last frame
	# SoundBoardEndAll??? BackgroundEndAll???
	# SoundBackgroundEffect...All? as in, it ends all effects at once...? but what's the enum...
	# SoundBackgroundEnableAll?
	# Sound: Field Environment (All)
	class SBEA(Serializable):

		def __init__(self):
			self.Action = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 1 = Play, 2 = Stop
			self.Action = rw.rw_uint32(self.Action)
			assert self.Action == 1 or self.Action == 2

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			assert self.UNUSED[2] == 0


	class Scr_(Serializable):

		def __init__(self):
			self.ProcedureIndex = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			self.ProcedureIndex = rw.rw_int32(self.ProcedureIndex)
			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_int32(self.UNUSED[2])
			for unused in self.UNUSED:
				assert unused == 0


	class SFlt(Serializable):

		def __init__(self):
			self.EnableFilter = None
			self.BlendType = None
			self.AlphaValue = None
			self.FilterID = None

		def __rw_hook__(self, rw, dataSize):
			self.EnableFilter = rw.rw_uint32(self.EnableFilter)
			# 0 = Opaque, 1 = SemiTransparent, 2 = AdditiveTransparency, 3 = SubtractiveTransparency, 4 = ModulateTransparency, 5 = Modulate2Transparency
			self.BlendType = rw.rw_uint32(self.BlendType)
			# 0-1; default = 1
			self.AlphaValue = rw.rw_float32(self.AlphaValue)
			# -1 through 255; basically color-to-transparent gradients at various angles. editor shows them but i don't feel like listing them all lmao. no sensible order here
			self.FilterID = rw.rw_uint32(self.FilterID)


	class SFts(Serializable):

		def __init__(self):
			self.Enable = None
			self.ObjectId = None

			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			self.Enable = rw.rw_uint32(self.Enable)
			assert self.Enable == 0 or self.Enable == 1

			self.ObjectId = rw.rw_uint32(self.ObjectId)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0


	class Snd_(Serializable):

		def __init__(self):
			self.Source = None
			self.Action = None
			self.Channel = None
			self.CueId = None
			self.FadeDuration = None

			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0 = None, 1 = BGM, 2 = System, 3 = Event(_SE)
			self.Source = rw.rw_uint32(self.Source)
			assert self.Source >= 0 and self.Source <= 3

			# 0 = None, 1 = Play, 2 = Stop
			self.Action = rw.rw_uint32(self.Action)
			assert self.Action >= 0 and self.Action <= 2

			# collation:
			# Channel
			#   VAL: 0  FREQ: 8949
			#   VAL: 1  FREQ: 1460
			#   VAL: 2  FREQ: 157
			#   VAL: 3  FREQ: 138
			# ...so... is 0 mono, 1 stereo, and 2 and 3... left and right single-channel?
			# ...or is 0 "just play whatever the file has" while 1, 2, and 3 change it?
			self.Channel = rw.rw_uint32(self.Channel)
			assert self.Channel >= 0 and self.Channel <= 3

			# 0-99999
			self.CueId = rw.rw_uint32(self.CueId)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			assert self.UNUSED[1] == 0

			# fade time in ms...? 0-120
			self.FadeDuration = rw.rw_uint32(self.FadeDuration)

			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])
			assert self.UNUSED[2] == 0


	class SsCp(Serializable):

		def __init__(self):
			self.FadeOutStartFrame = None
			self.UNUSED = [None]*3

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			# 0-(specified duration of command)
			self.FadeOutStartFrame = rw.rw_uint32(self.FadeOutStartFrame)

			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])
			self.UNUSED[2] = rw.rw_uint32(self.UNUSED[2])

			for unused in self.UNUSED:
				assert unused == 0


	# Texture: Color
	class TCol(Serializable):

		def __init__(self):
			self.RGBA = None
			self.InterpolationType = None
			self.UNUSED = [None]*2

		def __rw_hook__(self, rw, dataSize):
			
			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# default = 255, 255, 255, 255
			self.RGBA = rw.rw_uint8s(self.RGBA, 4)
			# 0 = Linear, 1 = Step, 4354 = Hermitian (why not 2????? beats me); default = 4354/Hermitian
			self.InterpolationType = rw.rw_uint32(self.InterpolationType)

			self.UNUSED[1] = rw.rw_int32(self.UNUSED[1])
			assert self.UNUSED[1] == 0


	# Texture: Move
	class TMov(Serializable):

		def __init__(self):

			self.BitwiseNonsense = None
			self.InterpolationType = None
			self.HermitianInGradientType = None
			self.HermitianOutGradientType = None
			self.StepCount = None

			self.Coordinates = None

			self.UNUSED = [None]

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# uses nibbles, and also if i try to split it into shorts it does dumb stuff
			# ...in royal, which can be big or little endian. rifp
			self.BitwiseNonsense = rw.rw_int32(self.BitwiseNonsense)
			# 0 = Linear, 1 = Step, 2 = Hermitian; default = 2/Hermitian
			self.InterpolationType = self.BitwiseNonsense & 0xFF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1/Slow
			self.HermitianInGradientType = (self.BitwiseNonsense >> 8) & 0xF
			self.HermitianOutGradientType = (self.BitwiseNonsense >> 12) & 0xF
			# 0-10
			self.StepCount = (self.BitwiseNonsense >> 16) & 0xFFFF

			# X, Y; -99999 to +99999
			self.Coordinates = rw.rw_float32s(self.Coordinates, 2)


	# in the beta (once) but not in the editor lol
	class TMSE(Serializable):

		def __init__(self):
			self.UNK = [None]*4

		def __rw_hook__(self, rw, dataSize):
			for i in range(4):
				self.UNK[i] = rw.rw_int32(self.UNK[i])


	# Texture: Register
	class TRgs(Serializable):

		def __init__(self):
			self.DisplayType = None
			self.DrawingPriority = None
			self.BlendType = None
			self.UNUSED = [None]

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# 0 = None, 1 = On, 2 = Off
			self.DisplayType = rw.rw_uint32(self.DisplayType)
			# 0 = 2dLower, 1 = 2dBasis, 2 = 2dUpper; default = 1/2dBasis
			self.DrawingPriority = rw.rw_uint32(self.DrawingPriority)
			# 0 = Opaque, 1 = Translucent, 2 = AdditiveTranslucent, 3 = SubtractiveTranslucent, 4 = MultiplicativeTranslucent, 5 = 2xMultiplicativeTranslucent
			self.BlendType = rw.rw_uint32(self.BlendType)


	# Frame: Trigger Motion
	class TrMt(Serializable):

		def __init__(self):
			self.Bitfield = None
			self.UseSumOfInputConditionValues = None
			self.UpAnimationFromExt = None
			self.DownAnimationFromExt = None
			self.LeftAnimationFromExt = None
			self.RightAnimationFromExt = None

			self.AssetID = None
			self.TimeLimit = None

			self.UpAnimationID = None
			self.DownAnimationID = None
			self.LeftAnimationID = None
			self.RightAnimationID = None

			self.UpInputConditionValue = None
			self.DownInputConditionValue = None
			self.LeftInputConditionValue = None
			self.RightInputConditionValue = None

			self.UNK = [None]*16
			self.UNUSED = None

		def __rw_hook__(self, rw, dataSize):
			assert dataSize == 48 or dataSize == 112

			self.Bitfield = rw.rw_uint32(self.Bitfield)
			self.UseSumOfInputConditionValues = self.Bitfield & 0x1
			assert (self.Bitfield >> 1) & 0x1 == 0
			assert (self.Bitfield >> 2) & 0x1 == 0
			self.UpAnimationFromExt = (self.Bitfield >> 4) & 0x1
			self.DownAnimationFromExt = (self.Bitfield >> 5) & 0x1
			self.LeftAnimationFromExt = (self.Bitfield >> 6) & 0x1
			self.RightAnimationFromExt = (self.Bitfield >> 7) & 0x1

			# 0-999
			self.AssetID = rw.rw_uint32(self.AssetID)
			# 0-99999
			self.TimeLimit = rw.rw_uint32(self.TimeLimit)

			self.UNUSED = rw.rw_uint32(self.UNUSED)
			assert self.UNUSED == 0

			# -1 to 59; default = -1
			self.UpAnimationID = rw.rw_int32(self.UpAnimationID)
			self.DownAnimationID = rw.rw_int32(self.DownAnimationID)
			self.LeftAnimationID = rw.rw_int32(self.LeftAnimationID)
			self.RightAnimationID = rw.rw_int32(self.RightAnimationID)

			# 0-10
			self.UpInputConditionValue = rw.rw_uint32(self.UpInputConditionValue)
			self.DownInputConditionValue = rw.rw_uint32(self.DownInputConditionValue)
			self.LeftInputConditionValue = rw.rw_uint32(self.LeftInputConditionValue)
			self.RightInputConditionValue = rw.rw_uint32(self.RightInputConditionValue)

			if dataSize > 48:
				for i in range(16):
					self.UNK[i] = rw.rw_uint32(self.UNK[i])


	# Texture: Scale
	class TScl(Serializable):

		def __init__(self):
			self.BitwiseNonsense = None
			self.InterpolationType = None
			self.HermitianInGradientType = None
			self.HermitianOutGradientType = None
			self.StepCount = None

			self.HorizontalScale = None
			self.VerticalScale = None

			self.UNUSED = [None]

		def __rw_hook__(self, rw, dataSize):

			self.UNUSED[0] = rw.rw_int32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# uses nibbles, and also if i try to split it into shorts it does dumb stuff
			# ...in royal, which can be big or little endian. rifp
			self.BitwiseNonsense = rw.rw_int32(self.BitwiseNonsense)
			# 0 = Linear, 1 = Step, 2 = Hermitian; default = 2
			self.InterpolationType = self.BitwiseNonsense & 0xFF
			# 0 = Normal, 1 = Slow, 2 = Fast; default = 1
			self.HermitianInGradientType = (self.BitwiseNonsense >> 8) & 0xF
			self.HermitianOutGradientType = (self.BitwiseNonsense >> 12) & 0xF
			# 0-10
			self.StepCount = (self.BitwiseNonsense >> 16) & 0xFFFF

			# 0-3; default = 1
			self.HorizontalScale = rw.rw_float32(self.HorizontalScale)
			self.VerticalScale = rw.rw_float32(self.VerticalScale)


	# Wipe: Circle
	# editor only?
	class WpCi(Serializable):
		
		def __init__(self):
			self.LockedToStartCoordinates = None
			self.TextureType = None

			self.StartingCoordinates = None
			self.EndingCoordinates = None

			self.DisplayMagnification = None

			self.UNUSED = [None]

		def __rw_hook__(self, rw, dataSize):
			# bool; if true, EndingCoordinates inherently equal to StartingCoordinates
			self.LockedToStartCoordinates = rw.rw_uint32(self.LockedToStartCoordinates)
			# always 0...
			self.TextureType = rw.rw_uint32(self.TextureType)

			# X is 0-1280; Y is 0-720; default: 640, 360
			self.StartingCoordinates = rw.rw_uint32s(self.StartingCoordinates, 2)
			# X is 0-1280; Y is 0-720; default: 640, 360
			self.EndingCoordinates = rw.rw_uint32s(self.EndingCoordinates, 2)

			# 0-50; default = 1
			self.DisplayMagnification = rw.rw_float32(self.DisplayMagnification)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0


	# Wipe: Horizontal
	# editor only?
	class WpHo(Serializable):

		def __init__(self):
			self.TextureType = None
			self.Mode = None
			self.Direction = None
			self.UNUSED = [None]

		def __rw_hook__(self, rw, dataSize):

			# this coult be TextureType, but that's also always zero, so :shrug:
			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])
			assert self.UNUSED[0] == 0

			# always 0...
			self.TextureType = rw.rw_uint32(self.TextureType)
			# 0 = Open, 1 = Close
			self.Mode = rw.rw_uint32(self.Mode)
			# 0 = LeftToRight, 1 = RightToLeft
			self.Direction = rw.rw_uint32(self.Direction)


	class Unk_(Serializable):

		def __init__(self):
			self.UNK = None

		def __rw_hook__(self, rw, dataSize):
			self.UNK = rw.rw_bytestring(self.UNK, dataSize)


if __name__ == "__main__":
	main()
