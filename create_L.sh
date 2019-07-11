# create_L.sh
# Amir Harati, July 2019


input_segment_file=$1
lang_src=$2
mkdir -p $lang_src
cp data/local/dict/lexicon4_extra.txt  $lang_src
cp data/local/dict/extra_questions.txt  $lang_src
cp data/local/dict/silence_phones.txt  $lang_src
cp data/local/dict/optional_silence.txt $lang_src
cp data/local/dict/nonsilence_phones.txt  $lang_src
cp data/local/dict/word_list  $lang_src

python create_new_lexicon.py  --input_lexicon data/local/dict/lexicon4_extra.txt  --input_segment_file $input_segment_file  --output_lexicon $lang_src/lexicon.txt
utils/prepare_lang.sh $lang_src/ "<unk>"  $lang_src/lang_temp $lang_src
