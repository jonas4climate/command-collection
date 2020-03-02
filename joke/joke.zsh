#!/bin/zsh

# Read jokes from joke-library.txt file
jokes=("${(@f)$(cat ~/CS/Additional/Projects/command-collection/joke/joke-library.txt)}")

# Set defaults for flags
a_flag="false"
# h_flag not needed
n_flag="false"
n_arg=""

echo ""

# Read flags
while getopts 'ahn:' flag; do
   case "${flag}" in
      a) a_flag="true" ;;
      h) man joke ;;
      n) n_flag="true"
         n_arg="${OPTARG}" ;;
      *) echo "Please refer to the man page for valid flags."
         exit 1 ;;
   esac
done

# Output according to arguments
if [ "$#" -ne 0 ]; then
   if [ "$a_flag" = "true" ]; then
      for joke in $jokes; do
         echo $joke
         echo ""
      done
   elif [ "$n_flag" = "true" ]; then
      if [ $n_arg -gt 0 ] && [ $n_arg -le $#jokes ]; then
         echo $jokes[$n_arg]
      else
         echo "Out of bounds. Jokes only available between 1 and $#jokes "
         echo "Read manpage for usage of the -n flag"
      fi
   else
      echo "invalid arguments"
      exit 1
   fi
else
   # Random joke
   min=1
   max=$#jokes
   random=$[${RANDOM}%max+min]
   echo $jokes[random]
fi
