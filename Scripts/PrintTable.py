import argparse
from pathlib import Path
from Formats import Table


def main():

	parser = argparse.ArgumentParser(prog="PrintTable", description="Print the entries in a FTD/CTD/ETD file.")
	parser.add_argument("--table-path", required=True, help="Path to the FTD/CTD/ETD.")
	parser.add_argument("--table-name", required=False, help="Optionally provide the canonical name of the table. If omitted, will derive name from path.")
	args = parser.parse_args()

	table = Table()
	table.read(args.table_path, filename=(args.table_name if args.table_name else Path(args.table_path).stem))
	table.pretty_print()


if __name__ == "__main__":
	main()
