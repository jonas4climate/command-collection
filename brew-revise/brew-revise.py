import subprocess
import os 
from pathlib import Path

# Print purpose of script
print('\nYou started the brew-revise process.\n'
	+ 'This script runs in an interactive environment and scans your brew formulae for leftover former dependencies and isolate formula you may not need anymore.')

# Print command usage
print('\nCommands you can use:\n' + '-----------\n' 
	+ '- "end" to stop further checking\n'
	+ '- "man" to get the manpage of the formula\n' 
	+ '- "desc" to get the concise brew description\n'
	+ '- "info" to get homepage and more information\n'
	+ '- "rm" to delete formula\n' 
	+ '- "skip" to keep formula and continue searching\n'
	+ '- "fav" to skip and stop asking for this formula in the future')

# Gets all brew formulae of user
formulae = subprocess.run(['brew', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()

# Useful paths
home = str(Path.home())
revise_dir = home + '/.brew-revise'
fav_path = revise_dir + '/favourites.csv'
hist_path = revise_dir + '/history.csv'

# Ensure brew-revise directory and files exists, otherwise create them
if not os.path.exists(revise_dir):
	os.mkdir(revise_dir)
Path(fav_path).touch()
Path(hist_path).touch()

print('\nStarted scanning...')

# Get stored favourites 
with open(fav_path, 'r') as file:
    favs = file.read().replace('\n', '')

# New line for every new session 
with open(hist_path, 'a') as file:
	file.write('\n') 

for formula in formulae:
	# Get brew formula dependencies
	dependencies = subprocess.run(['brew', 'uses', '--installed', '--recursive', formula], stdout=subprocess.PIPE).stdout.decode('utf-8').split()

	# No dependencies and not in favourites
	if not dependencies and not favs.__contains__(formula):
		print('\n')
		# Decide wheter to delete formula
		print('Independent formula: ' + formula)
		action = input().lower()

		# Intermediary actions 
		while (action != 'rm' and action != 'skip' and action != 'fav'):
			# Man page
			if action == 'man':
				subprocess.run(['man', formula])

			# Brew description
			elif action == 'desc':
				subprocess.run(['brew', 'desc', formula])

			# Brew information
			elif action == 'info':
				subprocess.run(['brew', 'info', formula])

			# End script
			elif action == 'stop' or action == 'end':
				print('\nDo you still want to clean up?')
				action = input().lower()
				if action == 'yes' or action == 'y':
					print('Quickly cleaning up...')
					subprocess.run(['brew', 'cleanup'])
				exit()

			# Other (unrecognized) input
			else:
				print('The input was unrecognized.')

			action = input().lower()

		# Remove formula
		if action == 'rm':
			subprocess.run(['brew', 'uninstall', formula])
			with open(hist_path, 'a') as file:
				file.write(action + ': ' + formula + ', ')
			print('Deleted!')

		# Add to favourites to skip asking in the future
		elif action == 'fav':
			with open(fav_path, 'a') as file:
				file.write(formula + ', ')

		#elif action == 'skip':
			# Do nothing
	#else:
	#	print('\nThere are formulae depending on ' + formula)

print('\nCleaning up...')
subprocess.run(['brew', 'cleanup'])
