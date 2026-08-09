
import argparse

from pathlib import Path

from Formats import MAP


def main():

	parser = argparse.ArgumentParser(prog="PrintMaps", description="Print the contents of all MAP files.")
	parser.add_argument("--extracted-dir", required=True, help="Path to directory including MAP files.")
	args = parser.parse_args()

	failures = list()
	paths = list(sorted(Path(args.extracted_dir).rglob(f"*.MAP")))
	for path in paths:
		mappy = MAP()
		try:
			print()
			print(path)
			mappy.read(path)
		except:
			print("FAIL")
			failures.append(str(path))

	print("Failed to read {}/{} MAPs: {}".format(len(failures), len(paths), ", ".join(failures)))

if __name__ == "__main__":
	main()

