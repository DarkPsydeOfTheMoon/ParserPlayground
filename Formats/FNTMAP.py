from .exbip.Serializable import Serializable


class FntMap(Serializable):

	def __init__(self):
		self.Inds = list()

	def __rw_hook__(self, rw):
		if rw.is_constructlike:
			while rw.peek_bytestream(1):
				self.Inds.append(None)
				self.Inds[-1] = rw.rw_uint16(self.Inds[-1])
		elif rw.is_parselike:
			oov_base = 9312
			oov_count = 0
			for i in range(len(self.Inds)):
				if self.Inds[i] > 0xFFFF:
					self.Inds[i] = oov_base + oov_count
					oov_count += 1
				self.Inds[i] = rw.rw_uint16(self.Inds[i])
