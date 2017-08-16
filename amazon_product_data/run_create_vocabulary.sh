python create_vocabulary.py train_normal.src > normal_vocab.sources.txt
python create_vocabulary.py train_lowercase.src > lowercase_vocab.sources.txt
python create_vocabulary.py train_title.src > title_vocab.sources.txt

python create_vocabulary.py train_normal.tgt > normal_vocab.targets.txt
python create_vocabulary.py train_lowercase.tgt > lowercase_vocab.targets.txt
python create_vocabulary.py train_title.tgt > title_vocab.targets.txt

