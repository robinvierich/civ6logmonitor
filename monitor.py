import os, time
import shutil
import argparse
import sys

is_windows = sys.platform.startswith('win')

if is_windows:
	default_civ_dump_path = os.path.join(os.path.expanduser('~'), "Documents", "My Games", "Sid Meier's Civilization VI", "Dumps")
else:
	print('WARNING: This script has only been tested on Windows.')
	default_civ_dump_path = ''

argparser = argparse.ArgumentParser(
	description='Watch for Civ VI crash logs and copy them before they are automatically deleted.',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argparser.add_argument('watch_path', nargs='?', help='The path where Civ VI will dump its crash logs.', default=default_civ_dump_path)
argparser.add_argument('save_path', nargs='?', help='The path where this script will copy the crash logs.', default=os.path.abspath('.'))

args = argparser.parse_args()

path_to_watch = args.watch_path
path_to_copy_to_on_change = args.save_path

before_abspaths = [os.path.join(path_to_watch, f) for f in os.listdir(path_to_watch)]
before = dict([(os.path.basename(f), os.stat(f)) for f in before_abspaths])


print("Watching \"{}\" for changes...".format(path_to_watch))
while True:
  time.sleep(0.03)

  after_abspaths = [os.path.join(path_to_watch, f) for f in os.listdir(path_to_watch)]
  after = dict([(os.path.basename(f), os.stat(f)) for f in after_abspaths])

  added_or_changed_files = [f for f, after_stat in after.items() if (not f in before or before[f].st_mtime != after_stat.st_mtime)]
  #removed_files = [f for f in before if not f in after]
  if added_or_changed_files:
  	print("Added or Changed: {}".format(", ".join (added_or_changed_files)))
  	for file in added_or_changed_files:
  		file_abspath = os.path.join(path_to_watch, file)
  		copied = False
  		
	  	dest_path = os.path.join(path_to_copy_to_on_change, file)

	  	while not copied:
	  		try:
			  	if os.path.isdir(file_abspath):
				  	if os.path.exists(dest_path):
						shutil.rmtree(dest_path)

					shutil.copytree(file_abspath, dest_path)
				else:
					shutil.copy2(file_abspath, dest_path)

				copied = True
			except Exception as e:
				print(e)
				continue

  		print "Copied: {} to {}".format(file_abspath, dest_path)

  before = after


