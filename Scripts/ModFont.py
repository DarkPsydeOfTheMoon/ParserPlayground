from Formats import Font


def main():
	"""
	Adds Polish and Turkish characters to the main P5R font
	from a directory of indexed PNGs.

	This is mega-unoptimized and takes literally 13 minutes to run...
	Fair warning....
	"""

	basePath = "Scripts/Assets"
	fntName = "FONT0"

	# read vanilla font and save it as a single large image
	fntPath = f"{basePath}/VANILLA_{fntName}.FNT"
	fnt = Font()
	fnt.read(fntPath)
	fnt.decompress()
	fnt.to_single_image(f"{basePath}/VANILLA_{fntName}.png", 60)

	# update font with Polish and Turkish characters as individual images
	fnt.update_from_dir(f"{basePath}/{fntName}_REPLACE")
	fnt.compress()
	fnt.write_right(f"{basePath}/MODDED_{fntName}.FNT")

	# save the updated font as a single large image
	fnt2 = Font()
	fnt2.read(f"{basePath}/MODDED_{fntName}.FNT")
	fnt2.decompress()
	fnt2.to_single_image(f"{basePath}/MODDED_{fntName}.png", 60)


if __name__ == "__main__":
	main()
