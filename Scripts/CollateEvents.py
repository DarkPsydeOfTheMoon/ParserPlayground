
import argparse
import array

from pathlib import Path

from Formats import EVT, ECS


def main():

	parser = argparse.ArgumentParser(prog="CollateEvents", description="Get value distributions across all events where a provided command is used.")
	parser.add_argument("--extracted-dir", required=True, help="Path to directory including EVT and ECS files.")
	#parser.add_argument("--command-name", required=True, help="Name of the command type to analyze.")
	parser.add_argument("--type-name", required=False, help="Name of the command type to analyze.")
	parser.add_argument("--element-type", required=False, choices=["headers", "objects", "commandbases", "commanddata"], default="commanddata", help="Type of element to collate")
	parser.add_argument("--data-field-name", help="Name of a data field to optionally check the value of.")
	parser.add_argument("--data-field-value", help="Value of a data field to optinally check for.")
	args = parser.parse_args()

	types = set()
	collation = dict()
	for patt, cls in [("EVT", EVT), ("ECS", ECS)]:
		paths = list(sorted(Path(args.extracted_dir).rglob(f"*.{patt}")))
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
					"""if command.Type in {"FOD_", "FAB_", "FAA_"} and command.Data.__dict__["ObjectIndex"] >= 64000:
						for obj in event.Objects:
							if obj.Id == command.ObjectId:
								print("##### E{:03d}_{:03d}: F{:03d}_{:03d}_{} ({}{})".format(event.MajorId, event.MinorId, obj.ResourceMajorId, obj.ResourceMinorId, obj.ResourceSubId, command.Type, command.Data.__dict__["ObjectIndex"]))"""
					if args.type_name is None or (command.Type == args.type_name and command.Data is not None):
						data = command.Data.__dict__
						#print("#####", event.MajorId, event.MinorId, event.Version, event.Endianness, command.CommandVersion, command.DataSize, data["UnkBool1"], data["EntryCount"])
						#if data["Entries"] == [[-1, 10, 1.0], [-1, 10, 1.0], [3, 8, 1.0], [0, 8, 1.0], [41, 8, 1.0], [0, 8, 1.0], [-1, 10, 1.0], [-1, 10, 1.0], [-1, 10, 1.0], [-1, 10, 1.0], [-1, 10, 1.0], [-1, 10, 1.0], [-1, 10, 1.0], [-1, 10, 1.0]]:
						#if data["Entries1"] and data["Entries1"] != [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]:
						#if data["Entries2"] and data["Entries2"] == [15, 15, 15, 15, 15, 15, 15, 15, 10, 10, 10, 10, 10, 10]:
						#	print("##############", event.MajorId, event.MinorId, data["Entries1"])
						#if command.Type == "MAA_" and data["AnimationID"] == 30:
						#	for obj in event.Objects:
						#		if obj.Id == command.ObjectId:
						#			if obj.ResourceMajorId == 4:
						#				print("#####", event.MajorId, event.MinorId)
						#			break
						#if command.Type == "FOD_" and data["ObjectIndex"] >= 64000:
						##if command.Type == "FOD_" and data["ObjectIndex"] >= 200 and data["ObjectIndex"] < 1600:
						##	print("#####", event.MajorId, event.MinorId)
						#	for obj in event.Objects:
						#		if obj.Id == command.ObjectId:
						#			print("##### E{:03d}_{:03d}: F{:03d}_{:03d}_{} ({})".format(event.MajorId, event.MinorId, obj.ResourceMajorId, obj.ResourceMinorId, obj.ResourceSubId, data["ObjectIndex"]))
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
						#print("#####", event.Version, command.CommandVersion, command.DataSize)
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
						if obj.Type == 0x0000003 and obj.ResourceMajorId == 195 and obj.ResourceMinorId == 1:
							print("#####", event.MajorId, event.MinorId)
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
		non_none_keys = [k for k in collation[key] if k is not None]
		min_val = min(non_none_keys) if non_none_keys else None
		print("{} ({} / {}) (min: {}, max: {})".format(key, len(collation[key]), sum(collation[key].values()), min(non_none_keys) if non_none_keys else None, max(non_none_keys) if non_none_keys else None))
		for val in sorted(collation[key], key=lambda k: -collation[key][k]): #[:20]:
			print(f"\tVAL: {val}\tFREQ: {collation[key][val]}")


if __name__ == "__main__":
	main()

