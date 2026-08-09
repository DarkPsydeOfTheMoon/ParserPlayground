from .exbip.Serializable import Serializable
from .exbip.BinaryTargets.Interface.Base import EndiannessManager


def main():

	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F003_002_00.FBN"
	path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F003_002_01.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F003_102_00.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F012_041_00.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F190_001_00.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F001_003_00.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F151_004_00.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F151_005_00.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F154_008_00.FBN"
	#path = "/home/ajda/Desktop/unpackery/FIELD/DATA/F191_050_00.FBN"
	#path = "/home/ajda/.config/rpcs3/dev_hdd0/game/JUNE2014/USRDIR/PS3_GAME/USRDIR/field/data/f003_002_00.FBN"
	#path = "/home/ajda/.config/rpcs3/dev_hdd0/game/JUNE2014/USRDIR/PS3_GAME/USRDIR/field/data/f003_002_01.FBN"
	fbn = FBN()
	fbn.read(path)


class FBNTrigger(Serializable):

	def __init__(self):
		self.TypeValue = None
		#self.TypeIdentifier = None

		self.Center = None

		self.Scale = None

		self.BottomRight = None
		self.TopRight = None
		self.BottomLeft = None
		self.TopLeft = None

		self.UNK = [None]*8

	def __rw_hook__(self, rw):
		self.UNK[0] = rw.rw_uint32(self.UNK[0])

		self.TypeValue = rw.rw_uint16s(self.TypeValue, 2)
		##self.TypeIdentifier = rw.rw_uint32(self.TypeIdentifier)

		self.Center = rw.rw_float32s(self.Center, 3)

		self.UNK[1] = rw.rw_float32(self.UNK[1])
		self.UNK[2] = rw.rw_float32(self.UNK[2])
		self.UNK[3] = rw.rw_uint8s(self.UNK[3], 4)

		self.Scale = rw.rw_float32(self.Scale)

		self.UNK[4] = rw.rw_float32(self.UNK[4])
		self.UNK[5] = rw.rw_float32(self.UNK[5])

		self.BottomRight = rw.rw_float32s(self.BottomRight, 3)
		self.TopRight = rw.rw_float32s(self.TopRight, 3)
		self.BottomLeft = rw.rw_float32s(self.BottomLeft, 3)
		self.TopLeft = rw.rw_float32s(self.TopLeft, 3)

		self.UNK[6] = rw.rw_float32(self.UNK[6])
		self.UNK[7] = rw.rw_float32(self.UNK[7])


class FBNEntrance(Serializable):

	def __init__(self):
		self.Unk1 = None
		self.Unk2 = None

		self.Position = None
		self.Rotation = None

		self.EntranceID = None
		self.RoomID = None

	def __rw_hook__(self, rw):
		self.Unk1 = rw.rw_uint32(self.Unk1)
		self.Unk2 = rw.rw_uint32(self.Unk2)

		self.Position = rw.rw_float32s(self.Position, 3)
		self.Rotation = rw.rw_float32s(self.Rotation, 3)

		self.EntranceID = rw.rw_uint16(self.EntranceID)
		self.RoomID = rw.rw_uint16(self.RoomID)


class FBNWanderShadow(Serializable):

	def __init__(self):
		self.Unk1 = None
		self.Unk2 = None
		self.Unk3 = None

		self.Position = None
		self.Rotation = None

		self.WanderRadius = None

		self.Unk4 = None

	def __rw_hook__(self, rw):
		self.Unk1 = rw.rw_uint32(self.Unk1)
		self.Unk2 = rw.rw_uint16(self.Unk2)
		self.Unk3 = rw.rw_uint16(self.Unk3)

		self.Position = rw.rw_float32s(self.Position, 3)
		self.Rotation = rw.rw_float32s(self.Rotation, 3)

		self.WanderRadius = rw.rw_float32(self.WanderRadius)

		self.Unk4 = rw.rw_uint32(self.Unk4)


class FBNChest(Serializable):

	def __init__(self):
		self.Unk1 = None

		self.Position = None
		self.Rotation = None

		self.MajorID = None
		self.MinorID = None

		self.ResourceHandle = None

		self.Unk2 = None

	def __rw_hook__(self, rw):
		self.Unk1 = rw.rw_uint32(self.Unk1)

		self.Position = rw.rw_float32s(self.Position, 3)
		self.Rotation = rw.rw_float32s(self.Rotation, 4)

		self.MajorID = rw.rw_uint16(self.MajorID)
		self.MinorID = rw.rw_uint16(self.MinorID)

		self.ResourceHandle = rw.rw_uint16(self.ResourceHandle)
		print("##### RESHND:", self.MajorID, self.MinorID, self.ResourceHandle)

		self.Unk2 = rw.rw_uint16(self.Unk2)


# idc enough to implement this one yet lol
class FBNCover(Serializable):

	def __init__(self):
		self.UNK = None

	def __rw_hook__(self, rw):
		self.UNK = rw.rw_bytestring(self.UNK, 148)


class FBNPatrolShadow(Serializable):

	def __init__(self):
		self.Unk1 = None

		self.ShadowSpeed = None

		self.Unk2 = None
		self.Unk3 = None
		self.Unk4 = None
		self.Unk5 = None

		self.PathNodeCount = None

		self.Unk6 = None

		self.PathNodes = list()
		self.WaitTimePerNode = None

	def __rw_hook__(self, rw):
		self.Unk1 = rw.rw_uint32(self.Unk1)

		self.ShadowSpeed = rw.rw_float32(self.ShadowSpeed)

		self.Unk2 = rw.rw_uint32(self.Unk2)
		self.Unk3 = rw.rw_uint32(self.Unk3)
		self.Unk4 = rw.rw_uint32(self.Unk4)
		self.Unk5 = rw.rw_uint32(self.Unk5)

		self.PathNodeCount = rw.rw_uint16(self.PathNodeCount)

		self.Unk6 = rw.rw_uint16(self.Unk6)

		for i in range(self.PathNodeCount):
			if rw.is_constructlike:
				self.PathNodes.append(None)
			self.PathNodes[-1] = rw.rw_float32s(self.PathNodes[-1], 3)

		self.WaitTimePerNode = rw.rw_uint32s(self.WaitTimePerNode, self.PathNodeCount)


class FBNNPC(Serializable):

	def __init__(self):
		self.Rotation = None
		self.FntID = None

		self.PathNodeCount = None
		self.PathNodes = list()

		self.UNK = [None]*9

	def __rw_hook__(self, rw):
		self.UNK[0] = rw.rw_uint32(self.UNK[0])
		self.UNK[1] = rw.rw_float32(self.UNK[1])

		self.Rotation = rw.rw_float32s(self.Rotation, 3)

		self.UNK[2] = rw.rw_float32(self.UNK[2])
		self.UNK[3] = rw.rw_float32(self.UNK[3])

		self.FntID = rw.rw_uint16(self.FntID)
		print("##### FNTID:", self.FntID)

		self.UNK[4] = rw.rw_uint16(self.UNK[4])
		self.UNK[5] = rw.rw_uint32(self.UNK[5])
		self.UNK[6] = rw.rw_uint32(self.UNK[6])
		self.UNK[7] = rw.rw_int32(self.UNK[7])

		self.PathNodeCount = rw.rw_uint16(self.PathNodeCount)

		self.UNK[8] = rw.rw_uint16(self.UNK[4])

		for i in range(self.PathNodeCount):
			if rw.is_constructlike:
				self.PathNodes.append(None)
			self.PathNodes[-1] = rw.rw_float32s(self.PathNodes[-1], 3)


class FBNSearchObj(Serializable):

	def __init__(self):
		self.Unk1 = None
		self.Unk2 = None
		self.Unk3 = None

		self.Position = None
		self.Rotation = None

		self.MajorID = None
		self.MinorID = None

		self.ResourceHandle = None

		self.Unk4 = None

		#self.UNK = [None]*9

	def __rw_hook__(self, rw):
		self.Unk1 = rw.rw_uint32(self.Unk1)
		self.Unk2 = rw.rw_uint16(self.Unk2)
		self.Unk3 = rw.rw_uint16(self.Unk3)

		self.Position = rw.rw_float32s(self.Position, 3)
		self.Rotation = rw.rw_float32s(self.Position, 4)

		self.MajorID = rw.rw_uint16(self.MajorID)
		self.MinorID = rw.rw_uint16(self.MinorID)

		self.ResourceHandle = rw.rw_uint16(self.ResourceHandle)
		print("##### RESHND:", self.MajorID, self.MinorID, self.ResourceHandle)

		self.Unk4 = rw.rw_uint16(self.Unk4)
		

class FBNWarningObj(Serializable):

	def __init__(self):
		self.Unk1 = None

		self.Position = None
		self.Rotation = None

		self.Unk2 = None
		self.Unk3 = None

		self.MajorID = None
		self.MinorID = None

		self.ResourceHandle = None

		self.Unk4 = None
		self.Unk5 = None

		self.ActiveTimer = None
		self.InactiveTime = None

	def __rw_hook__(self, rw):
		self.Unk1 = rw.rw_uint32(self.Unk1)

		self.Position = rw.rw_float32s(self.Position, 3)
		self.Rotation = rw.rw_float32s(self.Position, 4)

		self.Unk2 = rw.rw_uint16(self.Unk2)
		self.Unk3 = rw.rw_uint16(self.Unk3)

		self.MajorID = rw.rw_uint16(self.MajorID)
		self.MinorID = rw.rw_uint16(self.MinorID)

		self.ResourceHandle = rw.rw_uint16(self.ResourceHandle)
		print("##### RESHND:", self.MajorID, self.MinorID, self.ResourceHandle)

		self.Unk4 = rw.rw_uint16(self.Unk4)
		self.Unk5 = rw.rw_uint32(self.Unk5)

		self.ActiveTimer = rw.rw_float32(self.ActiveTimer)
		self.InactiveTime = rw.rw_float32(self.InactiveTime)


class FBNGrappleObj(Serializable):

	def __init__(self):
		self.Unk1 = None

		self.JumpAfterGrapple1 = None
		self.JumpAfterGrapple2 = None

		self.WireSequenceID = None

		self.Position = None
		self.Rotation = None

		self.MajorID = None
		self.MinorID = None

		self.ResourceHandle = None

		self.Unk2 = None

		self.JumpLength = None
		self.JumpHeight = None

	def __rw_hook__(self, rw):
		self.Unk1 = rw.rw_uint32(self.Unk1)

		self.JumpAfterGrapple1 = rw.rw_uint8(self.JumpAfterGrapple1)
		self.JumpAfterGrapple2 = rw.rw_uint8(self.JumpAfterGrapple2)
		self.WireSequenceID = rw.rw_uint16(self.WireSequenceID)

		self.Position = rw.rw_float32s(self.Position, 3)
		self.Rotation = rw.rw_float32s(self.Position, 4)

		self.MajorID = rw.rw_uint16(self.MajorID)
		self.MinorID = rw.rw_uint16(self.MinorID)

		self.ResourceHandle = rw.rw_uint16(self.ResourceHandle)
		print("##### RESHND:", self.MajorID, self.MinorID, self.ResourceHandle)

		self.Unk2 = rw.rw_uint16(self.Unk2)

		self.JumpLength = rw.rw_uint16(self.JumpLength)
		self.JumpHeight = rw.rw_uint16(self.JumpHeight)


class FBNGrappleTrigger(Serializable):

	def __init__(self):
		self.TypeValue = None
		#self.TypeIdentifier = None

		self.ResourceHandle = None

		self.Center = None

		self.Scale = None

		self.BottomRight = None
		self.TopRight = None
		self.BottomLeft = None
		self.TopLeft = None

		self.UNK = [None]*9

	def __rw_hook__(self, rw):
		self.UNK[0] = rw.rw_uint32(self.UNK[0])

		self.TypeValue = rw.rw_uint16s(self.TypeValue, 2)
		##self.TypeIdentifier = rw.rw_uint32(self.TypeIdentifier)

		self.ResourceHandle = rw.rw_uint16(self.ResourceHandle)
		print("##### RESHND:", self.ResourceHandle)

		self.UNK[1] = rw.rw_uint16(self.UNK[1])

		self.Center = rw.rw_float32s(self.Center, 3)

		self.UNK[2] = rw.rw_float32(self.UNK[2])
		self.UNK[3] = rw.rw_float32(self.UNK[3])
		self.UNK[4] = rw.rw_float32(self.UNK[4])

		self.Scale = rw.rw_float32(self.Scale)

		self.UNK[5] = rw.rw_float32(self.UNK[5])
		self.UNK[6] = rw.rw_float32(self.UNK[6])

		self.BottomRight = rw.rw_float32s(self.BottomRight, 3)
		self.TopRight = rw.rw_float32s(self.TopRight, 3)
		self.BottomLeft = rw.rw_float32s(self.BottomLeft, 3)
		self.TopLeft = rw.rw_float32s(self.TopLeft, 3)

		self.UNK[7] = rw.rw_uint16(self.UNK[7])
		self.UNK[8] = rw.rw_uint16(self.UNK[8])


class FBNEntry(Serializable):

	TYPES = {
		1: FBNTrigger,
		#2: FBNCrowdSpawn,
		#3: FBNNavi,
		4: FBNEntrance,
		#5: FBNHit,
		#6: FBNMask,
		#7: FBNCrowdPath,
		8: FBNWanderShadow,
		9: FBNChest,
		10: FBNCover,
		11: FBNPatrolShadow,
		#12: FBNMementosHit,
		#13: FBNMementosEntrance,
		14: FBNNPC,
		#15: FBNStealObj,
		#16: FBNSteal,
		#17: FBNLightPath,
		18: FBNSearchObj,
		19: FBNTrigger, #FBNSearchObjHit,
		21: FBNWarningObj,
		22: FBNTrigger, #FBNVoiceHit,
		#24: FBNMementosEntrance2,
		25: FBNGrappleObj,
		26: FBNGrappleTrigger,
		#1178750512: FBNHeader
	}

	def __init__(self):
		self.Type = 1178750512
		self.Version = 0
		self.Size = 16
		self.ListOffset = 0

		self.ListSize = 0
		self.List = list()

		self.Reserve = None

	def __rw_hook__(self, rw):

		self.Type = rw.rw_uint32(self.Type)
		self.Version = rw.rw_uint32(self.Version)
		self.Size = rw.rw_uint32(self.Size)
		self.ListOffset = rw.rw_uint32(self.ListOffset)
		#print(self.Type, self.Version, self.Size, self.ListOffset)

		if self.ListOffset:
			self.ListSize = rw.rw_uint32(self.ListSize)
			self.Reserve = rw.rw_uint32s(self.Reserve, 3)
			print("##########")
			print(self.TYPES[self.Type], self.ListSize)
			print("##########")
			assert self.Type in self.TYPES
			self.List = rw.rw_objs(self.List, self.TYPES[self.Type], self.ListSize)


class FBN(Serializable):

	def __init__(self):
		self.Entries = list()

	def __rw_hook__(self, rw):

		with EndiannessManager(rw, ">"):
			while rw.peek_bytestream(1):
				with rw.relative_origin():
					if rw.is_constructlike:
						self.Entries.append(None)
					self.Entries[-1] = rw.rw_obj(self.Entries[-1], FBNEntry)
					#print("?????", rw.tell(), self.Entries[-1].Size)
					assert rw.tell() == self.Entries[-1].Size
					rw.seek(self.Entries[-1].Size, 0)
		return


if __name__ == "__main__":
	main() 
