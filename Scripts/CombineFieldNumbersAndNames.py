import copy
from Formats import Table


def main():
	"""
	Load up FLDPLACENO and FLDPLACENAME to get a more readable sense
	of how field ids map to names.
	"""

	# load up the field name table
	fldNameTablePath = "Scripts/Assets/VANILLA_FLDPLACENAME.FTD"
	fldNameTableName = "FLDPLACENAME"
	fldNameTable = Table()
	fldNameTable.read(fldNameTablePath, filename=fldNameTableName)

	# add a new entry to the field name table
	newEntry = copy.deepcopy(fldNameTable.Entries[-1])
	newEntry.Data = b"Suminomiya\x00"
	fldNameTable.Entries.append(newEntry)
	fldNameTable.update_offsets(filename=fldNameTableName)

	# write updated field name table to a new file and load that up (mostly to check validity)
	fldNameTablePath2 = "Scripts/Assets/MODDED_FLDPLACENAME.FTD"
	fldNameTable.write(fldNameTablePath2, filename=fldNameTableName)
	fldNameTable2 = Table()
	fldNameTable2.read(fldNameTablePath2, filename=fldNameTableName)

	# load up the field number table
	fldNoTablePath = "Scripts/Assets/VANILLA_FLDPLACENO.FTD"
	fldNoTableName = "FLDPLACENO"
	fldNoTable = Table()
	fldNoTable.read(fldNoTablePath, filename=fldNoTableName)

	# add a new entry to the field number table
	# (which references the new entry in the field name table)
	newEntry = copy.deepcopy(fldNoTable.Entries[15].Entries[0])
	newEntry.FieldNameIndex = fldNameTable.DataCount - 1
	newEntry.Room1NameIndex = 45
	newEntry.Room2NameIndex = 0
	newEntry.Room3NameIndex = 0
	fldNoTable.Entries[15].Entries.append(newEntry)
	fldNoTable.update_offsets(filename=fldNoTableName)

	# write updated field number table to a new file and load that up (mostly to check validity)
	fldNoTablePath2 = "Scripts/Assets/MODDED_FLDPLACENO.FTD"
	fldNoTable.write(fldNoTablePath2, filename=fldNoTableName)
	fldNoTable2 = Table()
	fldNoTable2.read(fldNoTablePath2, filename=fldNoTableName)

	# check it out! should be F015_001 :)
	for i in range(fldNoTable2.DataCount):
		for j in range(fldNoTable2.Entries[i].EntryCount):
			fieldName = fldNameTable2.Entries[fldNoTable2.Entries[i].Entries[j].FieldNameIndex].Data
			room1Name = fldNameTable2.Entries[fldNoTable2.Entries[i].Entries[j].Room1NameIndex].Data
			room2Name = fldNameTable2.Entries[fldNoTable2.Entries[i].Entries[j].Room2NameIndex].Data
			room3Name = fldNameTable2.Entries[fldNoTable2.Entries[i].Entries[j].Room3NameIndex].Data
			print(f"F{i:03d}_{j:03d}: {fieldName}")
			print(f"  F{i:03d}_{j:03d}_0: {room1Name}")
			print(f"  F{i:03d}_{j:03d}_1: {room2Name}")
			print(f"  F{i:03d}_{j:03d}_2: {room3Name}")
			print()


if __name__ == "__main__":
	main()
