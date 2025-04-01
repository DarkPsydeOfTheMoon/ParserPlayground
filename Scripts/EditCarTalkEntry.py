import copy
from Formats import Table, FtdEntryTypes


def main():
	"""
	Load up a FLDPTYTALKCAR table and edit an entry (to remove it).
	"""

	tablePath1 = "Scripts/Assets/VANILLA_FLDPTYTALKCAR.PTD"
	tableName = "FLDPTYTALKCAR"

	table1 = Table()
	table1.read(tablePath1, filename=tableName)

	# remove mona asking ann on an evening stroll
	print(table1.Entries[3].Entries[29].stringify())
	table1.Entries[3].Entries[29].SupportMsgIndex = 65535

	# remove talk about ann's t&a lmao
	print(table1.Entries[3].Entries[68].stringify())
	print(table1.Entries[4].Entries[0].stringify())
	print(table1.Entries[18].Entries[15].stringify())
	table1.Entries[3].Entries[68].SupportMsgIndex = 65535
	table1.Entries[4].Entries[0].SupportMsgIndex = 65535
	table1.Entries[18].Entries[15].SupportMsgIndex = 65535

	# remove more talk about ann's t&a...
	print(table1.Entries[3].Entries[75].stringify())
	print(table1.Entries[4].Entries[18].stringify())
	print(table1.Entries[19].Entries[10].stringify())
	table1.Entries[3].Entries[75].SupportMsgIndex = 65535
	table1.Entries[4].Entries[18].SupportMsgIndex = 65535
	table1.Entries[19].Entries[10].SupportMsgIndex = 65535

	# save the results
	tablePath2 = "Scripts/Assets/MODDED_FLDPTYTALKCAR.PTD"
	table1.write_right(tablePath2, filename=tableName)

	# check the results
	table2 = Table()
	table2.read(tablePath2, filename=tableName)
	assert table1.DataCount == table2.DataCount
	for i in range(table2.DataCount):
		assert table1.Entries[i].EntryCount == table2.Entries[i].EntryCount

	# show the results!
	print("##########")
	print(table1.Entries[3].Entries[29].stringify())
	print(table1.Entries[3].Entries[68].stringify())
	print(table1.Entries[4].Entries[0].stringify())
	print(table1.Entries[18].Entries[15].stringify())
	print(table1.Entries[3].Entries[75].stringify())
	print(table1.Entries[4].Entries[18].stringify())
	print(table1.Entries[19].Entries[10].stringify())


if __name__ == "__main__":
	main()
