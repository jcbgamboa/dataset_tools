# Command line arguments parsing strongly inspired from
# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash

function usage {
	echo "Usage: ./generate_folds.sh [OPTS]"
	echo ""
	echo "    OPTS:"
	echo "    -v: verbose"
	echo "    -h: show this help"
}

#if [ "$#" -eq 0 ]; then
#	usage
#	exit 0
#fi

# Reset in case getopts has been used previously in the shell.
OPTIND=1
verbose=0

while getopts "h?v" opt; do
    case "$opt" in
    h|\?)
        usage
        exit 0
        ;;
    v)  verbose=1
        ;;
    esac
done

shift $((OPTIND-1))

# After this, we expect exactly two input options: the `in_folder` and the
# `out_folder` options. If there is anything else, we show usage and quit.
#if [ $# -ne 1 ]; then
#	echo "ERROR: OPTS must precede positional arguments"
#	usage
#	exit 0
#fi

CMD_OPTS=''

if [ ${verbose} -eq 1 ]; then
	set -x
	CMD_OPTS+=' -v'
fi

declare -A folder_names=(
	["non_lemmatized_text"]=""
	["lemmatized_text"]="-l"
	["non_lemmatized_trees"]="-t"
	["lemmatized_trees"]="-l -t"
)

fold_files=(dvd canon mp3 nikon cellphone)

for i in "${!folder_names[@]}"; do
	./parse_dataset.sh ${CMD_OPTS} ${folder_names[$i]} dataset output/$i

	# Now we want to put the right files inside each fold's folder
	for ((j = 0; j < ${#fold_files[@]}; j++)); do
		# Create the folder for the current cross-validation fold
		mkdir output/$i/${i}_cross${j}

		# Create the three data folders (i.e., train, dev and test)
		mkdir output/$i/${i}_cross${j}/train
		mkdir output/$i/${i}_cross${j}/dev
		mkdir output/$i/${i}_cross${j}/test

		# Copy the files
		# This puts all the generated files except "one of them" into the train folder
		find output/$i -type f -maxdepth 1 ! -name ${fold_files[$j]}* -exec cp -t output/$i/${i}_cross${j}/train {} +

		# Yes, we are using the test set as validation. This is
		# "sinful", but will be fixed when we actually do some true
		# experiment
		cp output/$i/${fold_files[$j]}* output/$i/${i}_cross${j}/dev
		cp output/$i/${fold_files[$j]}* output/$i/${i}_cross${j}/test

		# Finally, generate the sources.txt and targets.txt
		cat output/$i/${i}_cross${j}/train/*.in > output/$i/${i}_cross${j}/train/sources.txt
		cat output/$i/${i}_cross${j}/dev/*.in > output/$i/${i}_cross${j}/dev/sources.txt
		cat output/$i/${i}_cross${j}/test/*.in > output/$i/${i}_cross${j}/test/sources.txt

		cat output/$i/${i}_cross${j}/train/*.gt > output/$i/${i}_cross${j}/train/targets.txt
		cat output/$i/${i}_cross${j}/dev/*.gt > output/$i/${i}_cross${j}/dev/targets.txt
		cat output/$i/${i}_cross${j}/test/*.gt > output/$i/${i}_cross${j}/test/targets.txt
	done
done

