import copy
from Formats import Table


def main():
	"""
	Load up a FLDPLACENAME table, modify an entry, and add an entry.
	"""


	tablePath1 = "Scripts/Assets/VANILLA_FLDPLACENAME.FTD"
	tableName = "FLDPLACENAME"

	table1 = Table()
	table1.read(tablePath1, filename=tableName)

	# change the final entry
	table1.Entries[-1].Data = b"The Coolest Place\x00"

	# add an entry
	newEntry = copy.deepcopy(table1.Entries[-1])
	newEntry.Data = b"An Even Cooler Place!?\x00"
	table1.Entries.append(newEntry)

	# save the results
	tablePath2 = "Scripts/Assets/MODDED_FLDPLACENAME.FTD"
	table1.write_right(tablePath2, filename=tableName)

	# check the results
	table2 = Table()
	table2.read(tablePath2, filename=tableName)
	assert table1.DataCount == table2.DataCount
	for i in range(table2.DataCount):
		assert table1.Entries[i].Data == table2.Entries[i].Data

	# show the results!
	table2.pretty_print()


if __name__ == "__main__":
	main()
