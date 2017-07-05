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

set -x
for i in "${!folder_names[@]}"; do
	./parse_dataset.sh ${CMD_OPTS} ${folder_names[$i]} dataset output/$i
done

