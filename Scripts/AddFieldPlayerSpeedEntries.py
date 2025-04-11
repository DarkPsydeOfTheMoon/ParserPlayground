import copy
from Formats import Table, FtdEntryTypes


def main():
	"""
	Load up a FLDPLAYERSPEED table and add an entry.
	"""

	tablePath1 = "Scripts/Assets/VANILLA_FLDPLAYERSPEED.FTD"
	tableName = "FLDPLAYERSPEED"

	table1 = Table()
	table1.read(tablePath1, filename=tableName)

	# add an entry (at the end of the table)
	newEntry1 = FtdEntryTypes.FLDPLAYERSPEED()
	newEntry1.FieldMajorId = 9
	newEntry1.FieldMinorId = 2
	newEntry1.WalkSpeed = 50
	newEntry1.RunSpeed = 100
	newEntry1.AccelFrames = 4
	newEntry1.DecelFrames = 4
	newEntry1.StaticTurnFrames = 4
	table1.Entries[0].Entries.append(newEntry1)

	# save the results
	tablePath2 = "Scripts/Assets/MODDED_FLDPLAYERSPEED.FTD"
	table1.write_right(tablePath2, filename=tableName)

	# check the results
	table2 = Table()
	table2.read(tablePath2, filename=tableName)
	assert table1.DataCount == table2.DataCount
	for i in range(table2.DataCount):
		assert table1.Entries[i].EntryCount == table2.Entries[i].EntryCount

	# show the results!
	table2.pretty_print()


if __name__ == "__main__":
	main()
