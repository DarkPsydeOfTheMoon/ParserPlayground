import argparse, re
from pathlib import Path
from Formats import Table


def main():
	"""
	Recursively check that FTD reader can read/write all tables in a directory.
	"""

	parser = argparse.ArgumentParser(prog="VerifyTables", description="Check whether the parser can read/write all FTD/CTD/ETD files in a directory.")
	parser.add_argument("--table-directory", required=True, help="Path to the directory containing FTD/CTD/ETD/TTDs.")
	args = parser.parse_args()

	readFail = 0
	writeFail = 0
	totalTables = 0
	patt = re.compile(r"\.[CcEeFfTt][Tt][Dd]$", re.IGNORECASE)
	for tablePath in sorted(path for path in Path(args.table_directory).rglob("*") if patt.search(str(path))):
		tableName = tablePath.stem
		table = Table()
		try:
			table.read(tablePath, filename=tableName)
		except Exception:
			print(f"READ FAIL: {tableName}")
			readFail += 1
		try:
			table.update_offsets(filename=tableName)
		except Exception:
			print(f"WRITE FAIL: {tableName}")
			writeFail += 1
		totalTables += 1

	print()
	print("TOTAL READ FAILS: {:.2%} ({} / {})".format(readFail/totalTables, readFail, totalTables))
	print("TOTAL WRITE FAILS: {:.2%} ({} / {})".format(writeFail/totalTables, writeFail, totalTables))


if __name__ == "__main__":
	main()
