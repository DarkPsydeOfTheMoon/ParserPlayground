
import argparse

from pathlib import Path

from Formats import EVT, ECS


def main():

	parser = argparse.ArgumentParser(prog="EventsWithCommand", description="Search for all events (and times) where a provided command is used.")
	parser.add_argument("--extracted-dir", required=True, help="Path to directory including EVT and ECS files.")
	#parser.add_argument("--command-name", required=True, help="Name of the command type to search for.")
	parser.add_argument("--command-name", required=False, help="Name of the command type to search for. If omitted, will search in the header.")
	parser.add_argument("--data-field-name", help="Name of a data field to optionally check the value of.")
	parser.add_argument("--data-field-value", help="Value of a data field to optinally check for.")
	args = parser.parse_args()

	frames = dict()
	durations = dict()
	for patt, cls in [("EVT", EVT), ("ECS", ECS)]:
		paths = list(sorted(Path(args.extracted_dir).rglob(f"*.{patt}")))
		for path in paths:
			event = cls()
			#try:
			event.read(path)
			#except Exception:
			#	#print(f"WARNING: EVT is ill-formed for file at: {path}")
			#	continue
			if args.command_name is None:
				if args.data_field_name is not None and args.data_field_value is not None and str(event.__dict__.get(args.data_field_name)) != args.data_field_value:
					continue
				if not path in frames:
					frames[path] = list()
				if patt == "EVT" and path not in durations:
					durations[path] = event.FrameCount
			for command in event.Commands:
				if command.Data is not None and command.Type == args.command_name:
					if args.data_field_name is not None and args.data_field_value is not None and str(command.Data.__dict__.get(args.data_field_name)) != args.data_field_value:
						continue
					#if not (event.MajorId, event.MinorId) in frames:
					#	frames[(event.MajorId, event.MinorId)] = list()
					#	durations[(event.MajorId, event.MinorId)] = event.FrameCount
					#frames[(event.MajorId, event.MinorId)].append(str(command.StartingFrame))
					if not path in frames:
						frames[path] = list()
					if patt == "EVT" and path not in durations:
						durations[path] = event.FrameCount
					frames[path].append(str(command.StartingFrame))

	#for majorId, minorId in sorted(frames):
	#	print("E{:03d}_{:03d} ({}): {}".format(majorId, minorId, durations[(majorId, minorId)], ", ".join(frames[(majorId, minorId)])))
	for path in sorted(frames):
		print("{} ({}): {}".format(path, durations.get(path), ", ".join(frames[path])))


if __name__ == "__main__":
	main()

