from enum import Enum
from .exbip.Serializable import Serializable


class BustupParam(Serializable):

	def __init__(self):
		self.Entries = list()

	def update_offsets(self):
		self.tobytes()

	def write_right(self, path):
		self.update_offsets()
		self.write(path)

	def __rw_hook__(self, rw):

		rw.endianness = ">"

		entriesSoFar = 0
		while (rw.is_constructlike and rw.peek_bytestream(1)) or (rw.is_parselike and entriesSoFar < len(self.Entries)):
			if rw.is_constructlike:
				self.Entries.append(None)
			self.Entries[entriesSoFar] = rw.rw_obj(self.Entries[entriesSoFar], Entry)
			entriesSoFar += 1


class Entry(Serializable):

	def __init__(self):
		self.MajorId = None
		self.MinorId = None
		self.SubId = None
		self.Reserve1 = None

		self.BasePos = None
		self.EyePos = None
		self.MouthPos = None
		self.Type = None
		self.AnimType = None
		self.Reserve2 = None

	def __rw_hook__(self, rw):

		self.MajorId = rw.rw_uint16(self.MajorId)
		self.MinorId = rw.rw_uint16(self.MinorId)
		self.SubId = rw.rw_uint16(self.SubId)
		self.Reserve1 = rw.rw_uint16(self.Reserve1)
		assert self.Reserve1 == 0

		self.BasePos = rw.rw_float32s(self.BasePos, 2)
		self.EyePos = rw.rw_float32s(self.EyePos, 2)
		self.MouthPos = rw.rw_float32s(self.MouthPos, 2)

		self.Type = rw.rw_uint16(self.Type)
		assert self.Type == 0
		self.AnimType = rw.rw_uint16(self.AnimType)
		self.Reserve2 = rw.rw_uint32(self.Reserve2)
		assert self.Reserve2 == 0


class AnimationType(Enum):
	Null                    = 0
	Eyes                    = 1
	Mouth                   = 2
	Eyes_Mouth              = 3
	Eyes_Mouth_ExcludeAlpha = 11
	Unknown                 = 15
