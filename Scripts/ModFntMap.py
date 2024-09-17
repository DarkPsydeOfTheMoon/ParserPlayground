from Formats import FNTMAP


def main():
	"""
	Modifies PersonaEditor's P5 fontmap to match the P5R fontmap --
	plus some extra characters for Polish and Turkish coverage.
	"""

	# read PersonaEditor's original fontmap
	fntPath = "Scripts/Assets/VANILLA_P5_ENG.FNTMAP"
	fntMap = FNTMAP()
	fntMap.read(fntPath)

	# read the modded EFIGS font table (original from AtlusScriptTools)
	charTbl = "Scripts/Assets/MODDED_P5R_EFIGS.tsv"
	charSet = list()
	with open(charTbl, "r") as f:
		for line in f:
			charSet += [elem.encode("utf-8").decode("unicode_escape") if elem.startswith("\\") and elem != "\\" else elem for elem in line.strip().split("\t")]

	# update fontmap with modded table and write to new fontmap
	newFntPath = "Scripts/Assets/MODDED_P5R_ENG.FNTMAP"
	newFntMap = FNTMAP()
	newFntMap.Inds = [ord(char) for char in charSet]
	newFntMap.write(newFntPath)

	# read the modded fontmap back in just to check
	doubleCheckFntMap = FNTMAP()
	doubleCheckFntMap.read(newFntPath)

	# check that the re-read fontmap comes out the same
	assert len(newFntMap.Inds) == len(doubleCheckFntMap.Inds)
	for i in range(len(doubleCheckFntMap.Inds)):
		assert newFntMap.Inds[i] == doubleCheckFntMap.Inds[i]

	# check that the modded characters are all as expected
	moddedIndStart = 3467
	addedChars = [
		# polish characters
		"Ą", "Ć", "Ę", "Ł", "Ń", "Ś", "Ź", "Ż",
		"ą", "ć", "ę", "ł", "ń", "ś", "ź", "ż",
		# turkish characters
		"Ğ", "İ", "Ş", "ğ", "ı", "ş"
	]
	for i in range(len(addedChars)):
		assert chr(doubleCheckFntMap.Inds[moddedIndStart + i]) == addedChars[i]


if __name__ == "__main__":
	main()
