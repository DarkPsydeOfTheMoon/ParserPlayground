from .exbip.Serializable import Serializable
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


class MAP(Serializable):

	def __init__(self):
		#self.Endianness = "<"
		self.EntryCount = 0

		self.Endianness = 0
		self.Spacing = 0
		self.Flags = 0
		self.Version = 0

		self.Unk1 = 0
		self.Unk2 = 0
		self.Unk3 = 0
		self.Unk4 = 0
		self.UnkEnum = 0

		self.Entries = None

		self.UNUSED = [0]*5

	def __rw_hook__(self, rw):

		if rw.is_constructlike:
			#self.Endianness = "<"
			#with EndiannessManager(rw, self.Endianness):
			with EndiannessManager(rw, "<"):
				self.EntryCount = rw.rw_uint32(self.EntryCount)
				#if self.EntryCount > 999:
				#	self.Endianness = ">"
				self.Endianness = rw.rw_uint8(self.Endianness)
				rw.seek(0, 0)

		#with EndiannessManager(rw, self.Endianness):
		with EndiannessManager(rw, "<" if self.Endianness == 1 else ">"):

			self.EntryCount = rw.rw_uint32(self.EntryCount)

			self.Endianness = rw.rw_uint8(self.Endianness)
			self.Spacing = rw.rw_uint8(self.Spacing)
			self.Flags = rw.rw_uint16(self.Flags)

			# observed: 0x1000000, 0x10000001, 0x1000100
			self.Version = rw.rw_int32(self.Version)

			self.UNUSED[0] = rw.rw_uint32(self.UNUSED[0])

			print("#####")
			print(self.EntryCount, self.Endianness, self.Spacing, self.Flags, self.Version)
			print("#####")

			self.Entries = rw.rw_objs(self.Entries, MAPEntry, self.EntryCount, self.Version)

			#if self.Flags == 512:
			if (self.Flags >> 9) & 1:
				self.Unk1 = rw.rw_uint8(self.Unk1)
				self.Unk2 = rw.rw_uint8(self.Unk2)
				self.UNUSED[1] = rw.rw_uint8(self.UNUSED[1])

				self.Unk3 = rw.rw_uint8(self.Unk3)
				self.Unk4 = rw.rw_uint8(self.Unk4)
				self.UNUSED[2] = rw.rw_uint8(self.UNUSED[2])

				self.UnkEnum = rw.rw_uint16(self.UnkEnum)

				self.UNUSED[3] = rw.rw_uint32(self.UNUSED[3])
				self.UNUSED[4] = rw.rw_uint32(self.UNUSED[4])
				print("!!!!!!!!", self.Unk1, self.Unk2, self.Unk3, self.Unk4, self.UnkEnum)

			assert all(unused == 0 for unused in self.UNUSED)

		#print(rw._bytestream.peek())
		rw.assert_eof()


class MAPEntry(Serializable):

	def __init__(self):
		self.MajorID = 0
		self.MinorID = 0

		self.X = 0
		self.Y = 0
		self.Z = 0
		self.Direction = 0

		self.UnkEnum = 0
		self.UnkBool = 0
		self.Priority = 0

		self.UNUSED = [0]*2

	def __rw_hook__(self, rw, version):

		self.MajorID = rw.rw_uint16(self.MajorID)
		self.MinorID = rw.rw_uint16(self.MinorID)

		self.X = rw.rw_uint8(self.X)
		self.Y = rw.rw_uint8(self.Y)
		self.Z = rw.rw_uint8(self.Z)
		self.Direction = rw.rw_uint8(self.Direction)

		print(self.MajorID, self.MinorID)
		print(self.X, self.Y, self.Z, self.Direction)

		self.UNUSED[0] = rw.rw_uint8(self.UNUSED[0])

		# royal only
		self.UnkEnum = rw.rw_uint8(self.UnkEnum)
		if version < 0x1000100:
			assert self.UnkEnum == 0

		# royal only
		self.UnkBool = rw.rw_uint8(self.UnkBool)
		if version < 0x1000100:
			assert self.UnkBool == 0

		# not royal only, but not used in oldest version
		self.Priority = rw.rw_uint8(self.Priority)
		if version < 0x1000001:
			assert self.Priority == 0

		# royal only
		if version >= 0x1000100:
			self.UNUSED[1] = rw.rw_uint32(self.UNUSED[1])

		assert all(unused == 0 for unused in self.UNUSED)

		print(self.UnkEnum, self.UnkBool, self.Priority)

		print("#####")
