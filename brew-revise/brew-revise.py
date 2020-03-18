import subprocess
import os 
from pathlib import Path

# Print purpose of script
print('\nYou started the interactive brew-revise process.\n'
	+ 'This script runs in an interactive environment and scans your brew formulae for leftover former dependencies you don\t need anymore.')

# Print command usage
print('\nCommands you can use:\n' + '-----------\n' 
	+ '- "end" to stop further checking\n'
	+ '- "man" to get the manpage of the formula\n' 
	+ '- "desc" to get the brew description\n'
	+ '- "info" to get links and more info than "desc"\n'
	+ '- "rm" to delete formula\n' 
	+ '- "skip" to keep formula and continue searching\n')

# Gets all brew formulae of user
formulae = subprocess.run(['brew', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()

home = str(Path.home())

# Ensure fav path + file exists, otherwise create it
if not os.path.exists(home + '/.brew-revise'):
	os.mkdir(home + '/.brew-revise')
Path(home + '/.brew-revise/favourites.csv').touch()

# Get stored favourites 
with open(home + '/.brew-revise/favourites.csv', 'r') as file:
    favs = file.read().replace('\n', '')

for formula in formulae:
	# Get brew formula dependencies
	dependencies = subprocess.run(['brew', 'uses', '--installed', '--recursive', formula], stdout=subprocess.PIPE).stdout.decode('utf-8').split()

	# No dependencies
	if not dependencies:
		print('\n')
		# Decide wheter to delete formula
		print('Independent formula: ' + formula)
		action = input().lower()

		# Intermediary actions 
		while (action != 'rm' and action != 'skip'):
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
			elif action == 'end':
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
			print('Deleted!')
	#else:
	#	print('\nThere are formulae depending on ' + formula)

print('\nCleaning up...')
subprocess.run(['brew', 'cleanup'])
