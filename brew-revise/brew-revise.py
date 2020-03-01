import subprocess

print('\nYou started the interactive brew-revise process.\nThis script will go through your brew formulae and allows you to delete formulae which are independent i.e. don\'t have other formulae depending on them.')

# Print command usage
print('\nCommands you can use:\n' + '-----------\n' 
	+ '- "stop" to stop further checking\n'
	+ '- "info" to get the manpage of the formula\n' 
	+ '- "yes" or "y" to confirm deletion\n' 
	+ '- "no" or "n" to keep this formula\n')

# Returns byte array of stdout output of command
formulae = subprocess.run(['brew', 'list'], stdout=subprocess.PIPE)
# Convert to string
formulae = formulae.stdout.decode('utf-8')
# Convert into list of words
formulae = formulae.split()

for formula in formulae:
	# Get brew formula dependencies
	dependencies = subprocess.run(['brew', 'uses', '--installed', '--recursive', formula], stdout=subprocess.PIPE)
	dependencies = dependencies.stdout.decode('utf-8')

	# No dependencies
	if not dependencies:
		print('\n')
		# Decide wheter to delete formula
		print('Independent formula: ' + formula + '. Do you want to delete it?')
		subprocess.run(['brew', 'desc', formula])
		action = input().lower()

		# Intermediary actions 
		while (action != 'yes' and action != 'y' and action != 'no' and action != 'n'):
			if action == 'info':
				subprocess.run(['man', formula])
			if action == 'stop':
				print('\nDo you still want to clean up?')
				action = input().lower()
				if action == 'yes' or action == 'y':
					print('Quickly cleaning up...')
					subprocess.run(['brew', 'cleanup'])
				exit()
			else:
				print('The input was unrecognized. Please check your command and enter again.')
			action = input().lower()
		if action == 'yes' or action == 'y':
			# Deleting formula in brew
			subprocess.run(['brew', 'uninstall', formula])
			print('Deleted!')
		elif action == 'no' or action == 'n':
			print('Checking next formula...')
	else:
		print('\nThere are formulae depending on: ' + formula)
		#subprocess.run(['brew', 'desc', formula])

print('\nCleaning up...')
subprocess.run(['brew', 'cleanup'])
