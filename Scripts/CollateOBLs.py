
import argparse
import array

from pathlib import Path

from Formats import Table


def main():

	parser = argparse.ArgumentParser(prog="CollateOBLs", description="Get value distributions across all OBLs.")
	parser.add_argument("--extracted-dir", required=True, help="Path to directory including OBL files.")
	args = parser.parse_args()

	paths = list(sorted(Path(args.extracted_dir).rglob("*.OBL")))
	for path in paths:
		table = Table()
		table.read(path, filename="OBL")
		print(path)
		if table.Entries and table.Entries[1].Entries:
			for entry in table.Entries[1].Entries:
				print("\t"+entry.stringify())
		print()
	return

	types = set()
	collation = dict()
	for patt, cls in [("EVT", EVT), ("ECS", ECS)]:
		for path in paths:
			event = cls()
			#try:
			event.read(path)
			#except Exception:
			#	print(f"WARNING: EVT is ill-formed for file at: {path}")
			#	continue
			if args.element_type == "commanddata":
				for command in event.Commands:
					types.add(command.Type)
					if args.type_name is None or (command.Type == args.type_name and command.Data is not None):
						data = command.Data.__dict__
						if args.data_field_name is not None and args.data_field_value is not None and str(data.get(args.data_field_name)) != args.data_field_value:
							continue
						for key in data:
							if key not in collation:
								collation[key] = dict()
							if isinstance(data[key], list) or isinstance(data[key], array.array):
								data[key] = str(data[key])
							collation[key][data[key]] = collation[key].get(data[key], 0) + 1
							#print(key, data[key], event.Version, command.CommandVersion)
						#print(event.MajorId, event.MinorId, path)
			elif args.element_type == "commandbases" and patt == "EVT":
				for command in event.Commands:
					types.add(command.Type)
					if args.type_name is None or command.Type == args.type_name:
						data = command.__dict__
						if args.data_field_name is not None and args.data_field_value is not None and str(data.get(args.data_field_name)) != args.data_field_value:
							continue
						#print(event.MajorId, event.MinorId, path)
						for key in data:
							if key == "Data":
								continue
							if key not in collation:
								collation[key] = dict()
							if isinstance(data[key], list) or isinstance(data[key], array.array):
								data[key] = str(data[key])
							collation[key][data[key]] = collation[key].get(data[key], 0) + 1
			elif args.element_type == "objects" and patt == "EVT":
				for obj in event.Objects:
					types.add(obj.Type)
					if args.type_name is None or str(obj.Type) == args.type_name:
						data = obj.__dict__
						if args.data_field_name is not None and args.data_field_value is not None and str(data.get(args.data_field_name)) != args.data_field_value:
							continue
						for key in data:
							if key not in collation:
								collation[key] = dict()
							if isinstance(data[key], list) or isinstance(data[key], array.array):
								data[key] = str(data[key])
							collation[key][data[key]] = collation[key].get(data[key], 0) + 1
						#print(event.MajorId, event.MinorId)
			elif args.element_type == "headers": # and patt == "EVT":
				data = event.__dict__
				if args.data_field_name is not None and args.data_field_value is not None and str(data.get(args.data_field_name)) != args.data_field_value:
					continue
				for key in data:
					if key == "Commands" or key == "Objects":
						continue
					if key not in collation:
						collation[key] = dict()
					if isinstance(data[key], list) or isinstance(data[key], array.array):
						data[key] = str(data[key])
					collation[key][data[key]] = collation[key].get(data[key], 0) + 1

	print(len(types), sorted(types))
	for key in collation:
		print("{} ({} / {}) (min: {}, max: {})".format(key, len(collation[key]), sum(collation[key].values()), min([k for k in collation[key] if k is not None]), max([k for k in collation[key] if k is not None])))
		for val in sorted(collation[key], key=lambda k: -collation[key][k])[:20]:
			print(f"\tVAL: {val}\tFREQ: {collation[key][val]}")


if __name__ == "__main__":
	main()

