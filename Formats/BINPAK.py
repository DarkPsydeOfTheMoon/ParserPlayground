from .exbip.Serializable import Serializable
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


class AtlusArchive(Serializable):

	def __init__(self):
		self.IsOldVersion = None
		self.NamesLength = None
		self.Endianness = None

		self.EntryCount = None
		self.Entries = None
		self.Padding = None

	def __rw_hook__(self, rw):

		if rw.is_constructlike:
			versionPeek = None
			versionPeek = rw.peek_bytestream(5)
			if versionPeek[0] == 0:
				self.IsOldVersion = False
				self.NamesLength = 32
				self.Endianness = ">"
			elif versionPeek[3] == 0 and versionPeek[4] != 0:
				self.IsOldVersion = False
				self.NamesLength = 32
				self.Endianness = "<"
			else:
				self.IsOldVersion = True
				self.NamesLength = 252
				self.Endianness = "<"

		with EndiannessManager(rw, self.Endianness):
			if self.IsOldVersion:
				if rw.is_constructlike:
					self.Entries = list()
					self.Padding = list()
				i = 0
				while (rw.is_constructlike and rw.peek_bytestream(1) != b"") or (rw.is_parselike and i < self.EntryCount):
					if rw.is_constructlike:
						self.Entries.append(None)
						self.Padding.append(None)
					self.Entries[i] = rw.rw_obj(self.Entries[i], FileEntry, self.NamesLength)
					paddingSize = (64 - (rw.tell() % 64)) if (rw.tell() % 64) else 0
					self.Padding[i] = rw.rw_bytestring(self.Padding[i], paddingSize)
					assert all(not b for b in self.Padding[i])
					i += 1
				self.EntryCount = len(self.Entries)
			else:
				self.EntryCount = rw.rw_uint32(self.EntryCount)
				self.Entries = rw.rw_objs(self.Entries, FileEntry, self.EntryCount, self.NamesLength)

		failed = False 
		try: 
			rw.assert_eof()																																											 
		except Exception:
			print("Failed to read file!")
			remainder = rw._bytestream.peek()
			print(len(remainder), remainder)


class FileEntry(Serializable):

	def __init__(self):
		self.Name = None
		self.Size = None
		self.Data = None

	def __rw_hook__(self, rw, namelength, cstring=False):
		#self.Name = rw.rw_bytestring(self.Name, namelength)
		self.Name = rw.rw_string(self.Name, namelength, encoding="ascii")
		#self.Name = rw.rw_cstring(self.Name, namelength, encoding="ascii")
		self.Size = rw.rw_uint32(self.Size)
		self.Data = rw.rw_bytestring(self.Data, self.Size)
		assert len(self.Data) == self.Size
