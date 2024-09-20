import argparse, os
from pathlib import Path
from Formats import AtlusArchive


def main():
	"""
	Unpack a BIN, PAC, or PAK.
	"""

	parser = argparse.ArgumentParser(prog="UnPak", description="Unpack the entries in an Atlus BIN/PAC/PAK file.")
	parser.add_argument("--archive-path", required=True, help="Path to the BIN/PAC/PAK.")
	args = parser.parse_args()

	acv = AtlusArchive()
	acv.read(args.archive_path)

	outputDir = os.path.join(Path(args.archive_path).parent, Path(args.archive_path).stem)
	os.makedirs(outputDir, exist_ok=True)
	for fileEntry in acv.Entries:
		fileName = fileEntry.Name.strip("\0")
		filePath = os.path.join(outputDir, fileName)
		with open(filePath, "wb") as f:
			f.write(fileEntry.Data)


if __name__ == "__main__":
	main()
