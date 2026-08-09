
import argparse
import os

from pathlib import Path

from Formats import EVT, ECS


def main():

	parser = argparse.ArgumentParser(prog="ElementsInEvent", description="Print all commands used in a provided event.")
	parser.add_argument("--extracted-dir", required=True, help="Path to directory including EVT and ECS files.")
	parser.add_argument("--major-id", type=int, required=True, help="Major ID of the event.")
	parser.add_argument("--minor-id", type=int, required=True, help="Minor ID of the event.")
	#parser.add_argument("--command-name", help="Name of the command type to optionally print specifically.")
	parser.add_argument("--type-name", help="Name of the command type to optionally print specifically.")
	parser.add_argument("--element-type", required=False, choices=["header", "objects", "commands"], default="commands", help="Type of element to collate")
	args = parser.parse_args()

	for ext, cls in [("EVT", EVT), ("ECS", ECS)]:
		path = os.path.join(args.extracted_dir, "E{:03d}".format((args.major_id // 100) * 100), "E{:03d}".format((args.major_id // 10) * 10), "E{:03d}_{:03d}.{}".format(args.major_id, args.minor_id, ext))
		if not os.path.isfile(path):
			path = os.path.join(args.extracted_dir, "e{:03d}".format((args.major_id // 100) * 100), "e{:03d}".format((args.major_id // 10) * 10), "e{:03d}_{:03d}.{}".format(args.major_id, args.minor_id, ext))

		if os.path.isfile(path):
			event = cls()
			#try:
			event.read(path)
			#except Exception:
			#	print(f"WARNING: EVT is ill-formed for file at: {path}")
			if ext == "EVT":
				print(f"E{event.MajorId:03d}_{event.MinorId:03d} ({event.FrameCount})")
			if args.element_type == "commands":
				for command in event.Commands:
					if command.Data is not None and (args.type_name is None or command.Type == args.type_name):
						print()
						#print(command.Frame, command.Type, list(command.Data.UNK))
						print(command.StartingFrame, command.FrameCount, command.ObjectId, command.Type, command.ForceSkipCommand, command.__dict__, command.Data.__dict__)
			elif args.element_type == "objects" and ext == "EVT":
				for obj in event.Objects:
					if args.type_name is None or str(obj.Type) == args.type_name:
						print()
						print(obj.__dict__)
			elif args.element_type == "header":
				print()
				print(event.__dict__)
		else:
			print(f"Event does not exist at file path: {path}")


if __name__ == "__main__":
	main()

