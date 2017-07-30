
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

# I'm not sure if this is the best way to do this
PYTHON=python3

RESULTS=./results
mkdir $RESULTS

#####
# 1 Calculate the intersections of the datasets
#####

#####
# 1.1
# Generate the counts for the SentiWS
cd senti_wortschatz
cat SentiWS_v1.8c_Negative.txt SentiWS_v1.8c_Positive.txt > in_file.txt
$PYTHON sentiws_count_words.py in_file.txt sentiws_words.txt
$PYTHON sentiws_count_words.py in_file.txt sentiws_words_pos.txt --include_pos
cd ..

#####
# 1.2
# Generate the counts for the German Polarity Clues
cd german_polarity_clues

# This is to compare with sentiws_words.txt
$PYTHON gpc_count_words.py GermanPolarityClues-Prob-220311.tsv gpc_words.txt

# This is to compare with sentiws_words_pos.txt
$PYTHON gpc_count_words.py GermanPolarityClues-Prob-220311.tsv gpc_words_pos.txt --include_pos
$PYTHON gpc_count_words.py GermanPolarityClues-Prob-220311.tsv gpc_words_pos_remove_missing_polarity.txt --include_pos --exclude_hifens

# This is to compare with sentiws_words_pos.txt
$PYTHON gpc_count_words.py GermanPolarityClues-Prob-220311.tsv gpc_words_pos_remove_missing_binary_polarity.txt --include_pos --use_binary_polarity --exclude_hifens

#####
# 1.3
# Generate the counts for the German Senti Spin

# This is to compare with sentiws_words.txt
$PYTHON gpc_count_words.py GermanSentiSpin-Prob-220311.tsv gss_words.txt

# This is to compare with sentiws_words_pos.txt
$PYTHON gpc_count_words.py GermanSentiSpin-Prob-220311.tsv gss_words_pos.txt --include_pos
$PYTHON gpc_count_words.py GermanSentiSpin-Prob-220311.tsv gss_words_pos_remove_missing_polarity.txt --include_pos --exclude_hifens

# This is to compare with sentiws_words_pos.txt
$PYTHON gpc_count_words.py GermanSentiSpin-Prob-220311.tsv gss_words_pos_remove_missing_binary_polarity.txt --include_pos --use_binary_polarity --exclude_hifens

cd ..

#####
# 1.4
# Calculate intersections between files

# 1.4.1 Intersections of only words
ALL_WORDS=$RESULTS/all_words
mkdir $ALL_WORDS

# All words in SWS vs. All words in GPC
$PYTHON intersect.py senti_wortschatz/sentiws_words.txt german_polarity_clues/gpc_words.txt $ALL_WORDS/sws_gpc_all_words.txt

# All words in SWS vs. All words in GSS
$PYTHON intersect.py senti_wortschatz/sentiws_words.txt german_polarity_clues/gss_words.txt $ALL_WORDS/sws_gss_all_words.txt

# All words in GPC vs. All words in GSS
$PYTHON intersect.py german_polarity_clues/gpc_words.txt german_polarity_clues/gss_words.txt $ALL_WORDS/gpc_gss_all_words.txt

# Intersection of all words in all datasets
$PYTHON intersect.py $ALL_WORDS/sws_gpc_all_words.txt german_polarity_clues/gss_words.txt $ALL_WORDS/all_datasets_all_words.txt


# 1.4.2 Intersection of words+POS (the SWS has cases of one word with multiple POS's)
ALL_WORDS_POS=$RESULTS/all_words_pos
mkdir $ALL_WORDS_POS

# All words+pos in SWS vs. All words+pos in GPC
$PYTHON intersect.py senti_wortschatz/sentiws_words_pos.txt german_polarity_clues/gpc_words_pos.txt $ALL_WORDS_POS/sws_gpc_all_words_pos.txt

# All words+pos in SWS vs. All words+pos in GSS
$PYTHON intersect.py senti_wortschatz/sentiws_words_pos.txt german_polarity_clues/gss_words_pos.txt $ALL_WORDS_POS/sws_gss_all_words_pos.txt

# I don't need to compare all words+pos in GPC/GSS because the count would be same as just words

# Intersection of all words+pos in all datasets
$PYTHON intersect.py $ALL_WORDS_POS/sws_gpc_all_words_pos.txt german_polarity_clues/gss_words_pos.txt $ALL_WORDS_POS/all_datasets_all_words_pos.txt


# 1.4.3 Intersection of SWS with GPC/GSS, while eliminating words with "-"
ALL_WORDS_NO_HIFEN=$RESULTS/all_words_no_hifen
mkdir $ALL_WORDS_NO_HIFEN


# 1.4.4 Intersection of SWS with binary GPC/GSS polarities, while eliminating
# words without polarity information (where all values are 0)
ALL_WORDS_NO_HIFEN_BINARY=$RESULTS/all_words_no_hifen_binary
mkdir $ALL_WORDS_NO_HIFEN_BINARY



#####
# 2 Calculate Means, Std. Deviations, and generate Histograms
#####

#####
# 2.1
# Generate files to be read by the program that will calculate the values

POLARITIES=$RESULTS/polarities
mkdir $POLARITIES

# Senti WS
$PYTHON senti_wortschatz/sentiws_count_words.py senti_wortschatz/in_file.txt $POLARITIES/sentiws_words_polarity.txt --include_pos --include_polarity

# GPC with continuous values
$PYTHON german_polarity_clues/gpc_count_words.py german_polarity_clues/GermanPolarityClues-Prob-220311.tsv $POLARITIES/gpc_words_pos_remove_missing_polarity.txt --include_pos --include_polarity --exclude_hifens

# GPC with binary values
$PYTHON german_polarity_clues/gpc_count_words.py german_polarity_clues/GermanPolarityClues-Prob-220311.tsv $POLARITIES/gpc_words_pos_remove_missing_binary_polarity.txt --include_pos --include_polarity --use_binary_polarity --exclude_hifens

# GSS with continuous values
$PYTHON german_polarity_clues/gpc_count_words.py german_polarity_clues/GermanSentiSpin-Prob-220311.tsv $POLARITIES/gss_words_pos_remove_missing_polarity.txt --include_pos --exclude_hifens --include_polarity

# GSS with binary values
$PYTHON german_polarity_clues/gpc_count_words.py german_polarity_clues/GermanSentiSpin-Prob-220311.tsv $POLARITIES/gss_words_pos_remove_missing_binary_polarity.txt --include_pos --use_binary_polarity --exclude_hifens --include_polarity

#####
# 2.2
# Call the program to generate the histograms and everything

STATISTICS=$RESULTS/statistics
mkdir $STATISTICS

$PYTHON calculate_statistics.py $POLARITIES/sentiws_words_polarity.txt $STATISTICS/sws_polarities

$PYTHON calculate_statistics.py $POLARITIES/gpc_words_pos_remove_missing_polarity.txt $STATISTICS/gpc_polarities

$PYTHON calculate_statistics.py $POLARITIES/gpc_words_pos_remove_missing_binary_polarity.txt $STATISTICS/gpc_polarities_binary

$PYTHON calculate_statistics.py $POLARITIES/gss_words_pos_remove_missing_polarity.txt $STATISTICS/gss_polarities

$PYTHON calculate_statistics.py $POLARITIES/gss_words_pos_remove_missing_binary_polarity.txt $STATISTICS/gss_polarities_binary

