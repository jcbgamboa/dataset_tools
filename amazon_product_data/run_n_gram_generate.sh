
function usage {
	echo "Usage: ./generate_folds.sh [OPTS]"
	echo ""
	echo "    OPTS:"
	echo "    -v: verbose"
	echo "    -h: show this help"
}

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

if [ ${verbose} -eq 1 ]; then
	set -x
fi

#python n_gram_generate.py train.json train_lowercase en --capitalize=lowercase
#python n_gram_generate.py train.json train_title en --capitalize=title
#python n_gram_generate.py train.json train_normal en

#python n_gram_generate.py validate.json validate_normal en
#python n_gram_generate.py validate.json validate_lowercase en --capitalize=lowercase
#python n_gram_generate.py validate.json validate_title en --capitalize=title

#python n_gram_generate.py test.json test_normal en
#python n_gram_generate.py test.json test_lowercase en --capitalize=lowercase
#python n_gram_generate.py test.json test_title en --capitalize=title

python n_gram_generate.py train.json train_lowercase_tcs en --capitalize=lowercase --target_char_seq=True
python n_gram_generate.py train.json train_title_tcs en --capitalize=title --target_char_seq=True
python n_gram_generate.py train.json train_normal_tcs en --target_char_seq=True

python n_gram_generate.py validate.json validate_normal_tcs en --target_char_seq=True
python n_gram_generate.py validate.json validate_lowercase_tcs en --capitalize=lowercase --target_char_seq=True
python n_gram_generate.py validate.json validate_title_tcs en --capitalize=title --target_char_seq=True

python n_gram_generate.py test.json test_normal_tcs en --target_char_seq=True
python n_gram_generate.py test.json test_lowercase_tcs en --capitalize=lowercase --target_char_seq=True
python n_gram_generate.py test.json test_title_tcs en --capitalize=title --target_char_seq=True


