from Formats import BustupParam


def main():
	"""
	Modifies P5R's BUSTUP/DATA/BUSTUP_PARAM.DAT to change one
	of Sumi's sprite offsets to fit a new characters' sprite.
	"""

	bpPath = "Scripts/Assets/VANILLA_BUSTUP_PARAM.DAT"
	bp = BustupParam()
	bp.read(bpPath)

	# change the offsets for the modded sprite
	for entry in bp.Entries:
		if entry.MajorId == 10 and entry.MinorId == 963 and entry.SubId == 0:
			assert entry.BasePos[0] == -2
			assert entry.BasePos[1] == 22
			assert entry.EyePos[0] == 200
			assert entry.EyePos[1] == 367
			assert entry.MouthPos[0] == 254
			assert entry.MouthPos[1] == 509
			entry.EyePos[0] = 210
			entry.EyePos[1] = 293
			entry.MouthPos[0] = 252
			entry.MouthPos[1] = 399

	modPath = "Scripts/Assets/MODDED_BUSTUP_PARAM.DAT"
	bp.write_right(modPath)

	bp2 = BustupParam()
	bp2.read(modPath)

	# check that the old and new params are identical
	assert len(bp.Entries) == len(bp2.Entries)
	for i in range(len(bp2.Entries)):
		if bp2.Entries[i].MajorId == 10 and bp2.Entries[i].MinorId == 963 and bp2.Entries[i].SubId == 0:
			assert bp2.Entries[i].BasePos[0] == -2
			assert bp2.Entries[i].BasePos[1] == 22
			assert bp2.Entries[i].EyePos[0] == 210
			assert bp2.Entries[i].EyePos[1] == 293
			assert bp2.Entries[i].MouthPos[0] == 252
			assert bp2.Entries[i].MouthPos[1] == 399
		assert bp.Entries[i].BasePos == bp2.Entries[i].BasePos
		assert bp.Entries[i].EyePos == bp2.Entries[i].EyePos
		assert bp.Entries[i].MouthPos == bp2.Entries[i].MouthPos


if __name__ == "__main__":
	main()
