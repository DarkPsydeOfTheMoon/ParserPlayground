import copy
from Formats import Table, FtdEntryTypes


def main():
	"""
	Load up a FLDBGMCND table and add an entry.
	"""

	tablePath1 = "Scripts/Assets/VANILLA_FLDBGMCND.FTD"
	tableName = "FLDBGMCND"

	table1 = Table()
	table1.read(tablePath1, filename=tableName)

	# add an entry (at the BEGINNING of the table)
	newEntry1 = FtdEntryTypes.FLDBGMCND()
	newEntry1.FieldMajorId = 15
	newEntry1.FieldMinorId = 1
	newEntry1.FieldType = 0
	newEntry1.BgmCueId = 41
	table1.Entries[0].Entries.insert(0, newEntry1)

	# ...and another one just for coverage lol
	newEntry2 = FtdEntryTypes.FLDBGMCND()
	newEntry2.FieldMajorId = 1
	newEntry2.FieldMinorId = 6
	newEntry2.FieldType = 0
	newEntry2.BgmCueId = 41
	table1.Entries[0].Entries.insert(0, newEntry2)

	# save the results
	tablePath2 = "Scripts/Assets/MODDED_FLDBGMCND.FTD"
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
