from .exbip.Serializable import Serializable
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


class ChatInviteTable(Serializable):

	def __init__(self):
		self.Entries = None

	def __rw_hook__(self, rw):
		with EndiannessManager(rw, ">"):
			self.Entries = rw.rw_objs(self.Entries, ChatInviteEntry, 365)

	def pretty_print(self):
		for i in range(365):
			print("({}) {}".format(i, self.Entries[i].stringify()))


class ChatInviteEntry(Serializable):

	def __init__(self):
		self.UNK = None

	def __rw_hook__(self, rw):
		with rw.relative_origin():
			self.UNK = rw.rw_uint8s(self.UNK, 40)
			#self.UNK = rw.rw_uint16s(self.UNK, 20)
			#self.UNK = rw.rw_uint32s(self.UNK, 10)
			assert rw.tell() == 40

	def stringify(self):
		return str(self.UNK)
