from Formats import ChatInviteTable


def main():

	tablePath = "Scripts/Assets/VANILLA_PMCHATINVITE365TBL.DAT"
	table = ChatInviteTable()
	table.read(tablePath)
	table.pretty_print()


if __name__ == "__main__":
	main()
