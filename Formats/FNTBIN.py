from .exbip.Serializable import Serializable
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


def main():

	path = "/home/ajda/Desktop/unpackery/FIELD/NPC/FNT003_002_00.BIN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/NPC/FNT003_002_01.BIN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/NPC/FNT190_001_00.BIN"
	fnt = FNTBIN()
	fnt.read(path)


class FNTBINEntry(Serializable):

	def __init__(self):
		self.Unk = None

	def __rw_hook__(self, rw):

		self.Unk = rw.rw_bytestring(self.Unk, 116)
		print(list(self.Unk))
		print()

		"""self.Type = rw.rw_uint32(self.Type)
		self.Version = rw.rw_uint32(self.Version)
		self.Size = rw.rw_uint32(self.Size)
		self.ListOffset = rw.rw_uint32(self.ListOffset)
		print(self.Type, self.Version, self.Size, self.ListOffset)

		if self.ListOffset:
			self.ListSize = rw.rw_uint32(self.ListSize)
			self.Reserve = rw.rw_uint32s(self.Reserve, 3)
			print("##########")
			print(self.TYPES[self.Type])
			print("##########")
			assert self.Type in self.TYPES
			self.List = rw.rw_objs(self.List, self.TYPES[self.Type], self.ListSize)

		print(self.ListSize, self.Reserve)"""


class FNTBIN(Serializable):

	def __init__(self):
		self.Entries = list()

	def __rw_hook__(self, rw):

		with EndiannessManager(rw, ">"):
			while rw.peek_bytestream(1):
				with rw.relative_origin():
					if rw.is_constructlike:
						self.Entries.append(None)
					self.Entries[-1] = rw.rw_obj(self.Entries[-1], FNTBINEntry)
					#assert rw.tell() == self.Entries[-1].Size
					#print(rw.tell(), self.Entries[-1].Size)
					#rw.seek(self.Entries[-1].Size, 0)
		return


if __name__ == "__main__":
	main() 
