# Command line arguments parsing strongly inspired from
# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash

function usage {
	echo "Usage: ./create_folds.sh [OPTS] in_folder out_folder"
	echo ""
	echo "    in_folder: the folder containing the 5 products."
	echo "    out_folder: the folder to be created with all the folds."
	echo ""
	echo "    OPTS:"
	echo "    -v: verbose"
	echo "    -h: show this help"
}

if [ "$#" -eq 0 ]; then
	usage
	exit 0
fi

# Reset in case getopts has been used previously in the shell.
OPTIND=1
verbose=0

while getopts "h?vf:" opt; do
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
if [ $# -ne 2 ]; then
	usage
	exit 0
fi

in_folder=$1
out_folder=$2

if [ ${verbose} -eq 1 ]; then
	set -x
fi

# Create the output folder
mkdir -p ${out_folder}

# These are the 5 product files (you can download these files in
# https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html )
declare -A dataset_files=(
	["Apex AD2600 Progressive-scan DVD player.txt"]="dvd"
	["Canon G3.txt"]="canon"
	["Creative Labs Nomad Jukebox Zen Xtra 40GB.txt"]="mp3"
	["Nikon coolpix 4300.txt"]="nikon"
	["Nokia 6610.txt"]="cellphone"
)

for i in "${!dataset_files[@]}"; do
	# As explained in:
	# https://stackoverflow.com/questions/11226322/how-to-concatenate-two-strings-to-build-a-complete-path
	# "The POSIX standard mandates that multiple / are treated as a
	# single / in a file name. Thus //dir///subdir////file is the same
	# as /dir/subdir/file."
	python generate_sequences.py "${in_folder}/${i}" "${out_folder}/${dataset_files[$i]}"
done


