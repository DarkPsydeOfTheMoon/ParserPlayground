from Formats import Table


def main():
	"""
	Load up FLDDNGPLACENO and FLDPLACENAME to get a more readable sense
	of how field ids map to names.
	"""

	# load up the field name table
	fldNameTablePath = "Scripts/Assets/VANILLA_FLDPLACENAME.FTD"
	fldNameTableName = "FLDPLACENAME"
	fldNameTable = Table()
	fldNameTable.read(fldNameTablePath, filename=fldNameTableName)

	# load up the field number table
	fldDngNoTablePath = "Scripts/Assets/VANILLA_FLDDNGPLACENO.FTD"
	fldDngNoTableName = "FLDDNGPLACENO"
	fldDngNoTable = Table()
	fldDngNoTable.read(fldDngNoTablePath, filename=fldDngNoTableName)

	# ...also FLDATDNGPLACENO, i guess
	fldAtDngNoTablePath = "Scripts/Assets/VANILLA_FLDATDNGPLACENO.FTD"
	fldAtDngNoTableName = "FLDATDNGPLACENO"
	fldAtDngNoTable = Table()
	fldAtDngNoTable.read(fldAtDngNoTablePath, filename=fldAtDngNoTableName)

	# ...also FLDTESTDNGPLACENO, i guess
	fldTestDngNoTablePath = "Scripts/Assets/VANILLA_FLDTESTDNGPLACENO.FTD"
	fldTestDngNoTableName = "FLDTESTDNGPLACENO"
	fldTestDngNoTable = Table()
	fldTestDngNoTable.read(fldTestDngNoTablePath, filename=fldTestDngNoTableName)

	# combine!
	for noTable in [fldAtDngNoTable, fldDngNoTable, fldTestDngNoTable]:
		for i in range(noTable.DataCount):
			print("Dungeon {}:".format(i))
			for j in range(noTable.Entries[i].EntryCount):
				fieldNameLine1 = fldNameTable.Entries[noTable.Entries[i].Entries[j].MajorNameIndex].Data
				fieldNameLine2 = fldNameTable.Entries[noTable.Entries[i].Entries[j].MinorNameIndex].Data
				print("  Area {}:".format(j))
				print("    {}".format(fieldNameLine1))
				print("    {}".format(fieldNameLine2))
			print()


if __name__ == "__main__":
	main()
