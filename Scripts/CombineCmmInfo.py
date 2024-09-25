from Formats import Table


def main():
	"""
	Load up cmmFormat and cmmMemberName to cross-reference them.
	"""

	# load up the cmm name tables
	cmmNameTablePath1 = "Scripts/Assets/VANILLA_cmmMemberName.ctd"
	cmmNameTableName1 = "cmmMemberName"
	cmmNameTable1 = Table()
	cmmNameTable1.read(cmmNameTablePath1, filename=cmmNameTableName1)

	cmmNameTablePath2 = "Scripts/Assets/VANILLA_cmmName.ctd"
	cmmNameTableName2 = "cmmName"
	cmmNameTable2 = Table()
	cmmNameTable2.read(cmmNameTablePath2, filename=cmmNameTableName2)

	# load up the cmm format table
	cmmFormatTablePath = "Scripts/Assets/VANILLA_cmmFormat.ctd"
	cmmFormatTableName = "cmmFormat"
	cmmFormatTable = Table()
	cmmFormatTable.read(cmmFormatTablePath, filename=cmmFormatTableName)

	for i in range(cmmFormatTable.DataCount):
		for j in range(cmmFormatTable.Entries[i].EntryCount):
			nameTableInd = cmmFormatTable.Entries[i].Entries[j].ConfidantTableIndex
			personName = cmmNameTable1.Entries[0].Entries[nameTableInd].stringify().decode("utf-8")
			menuName =  cmmNameTable2.Entries[0].Entries[nameTableInd].stringify().decode("utf-8")
			print("{}: {} ({})".format(j, menuName, personName))
			print("  {}".format(cmmFormatTable.Entries[i].Entries[j].stringify()))
			print()


if __name__ == "__main__":
	main()
