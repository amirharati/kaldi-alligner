#!/bin/bash
# Program: align.sh
# Amir Harati April 2018
#
# script to align (and enrich) the transcript to given audio.
# This script uses Kaldi and Aspire model.
# It generate a simple LM and create a new HCLG network and then
# run the recognizer to align the input speech to input transcript.
# transcripts expands by adding laughter and noise markers.
# In the output alignment, OOV words will be replaced by <unk> marker.
#
# Example Use case:
#

source path.sh

# input transcript (can be nbest)
input_trans=$1
# input wave file
input_wav=$2

input_lang_dir=$3

# ctm file contains the aligned trancript
out_ctm=$4

out_phone_ctm=$5

out_transid_seq=$6

#rm -rf temp
mkdir -p temp
# create scp files
python scripts/create_scp.py -i $input_wav -o temp




# copy the lm data
mkdir -p temp/lang

mkdir -p temp/graph_pp


cp $input_lang_dir/* temp/lang


# expand and update the transcriptions
python scripts/convert_trans.py -i $input_trans -o temp/trans.txt \
        -l [laughter] -n [noise] -u "<unk>" -w temp/lang/words.txt 

# make sure srilm is installed in is in the path (path.sh should do it but in case it does not)
ngram-count   -text temp/trans.txt -order 2 -addsmooth 0.1   -unk  -lm temp/custom.lm



#sh test.sh
# create a FST for custom lm (G.fst)
cat temp/custom.lm  | arpa2fst --disambig-symbol=#0  --read-symbol-table=temp/lang/words.txt - temp/lang/G.fst

# create HCLG graph
utils/mkgraph.sh --self-loop-scale 1.0 temp/lang exp/tdnn_7b_chain_online temp/graph_pp


# run the recognizer
# subsample the frames by factor 3
# --frame-subsampling-factor=1
mkdir -p temp/out
online2-wav-nnet3-latgen-faster --online=true --do-endpointing=false   --config=exp/tdnn_7b_chain_online/conf/online.conf --max-active=7000 --beam=15.0 \
--lattice-beam=6.0 --acoustic-scale=1.0 --word-symbol-table=temp/graph_pp/words.txt exp/tdnn_7b_chain_online/final.mdl \
temp/graph_pp/HCLG.fst "ark:temp/spk2utt.scp"  "scp:temp/wav.scp" "ark:|lattice-scale --acoustic-scale=0.5 ark:- ark:- | gzip -c >temp/out/lat.1.gz"

# create time alignment
# also acount for frame sub-sampling
# --frame-shift=0.01
lattice-align-words-lexicon  temp/lang/phones/align_lexicon.int  exp/tdnn_7b_chain_online/final.mdl "ark:gunzip -c temp/out/lat.1.gz|" ark:- | lattice-1best ark:- ark:- |  nbest-to-ctm  ark:- temp/out/align.ctm

zcat temp/out/lat.1.gz  > temp/out/lat.1
lattice-1best --acoustic-scale=1 ark:temp/out/lat.1 ark:temp/out/1best.lats
nbest-to-linear ark:temp/out/1best.lats ark,t:temp/out/1.ali 
ali-to-phones --ctm-output exp/tdnn_7b_chain_online/final.mdl ark:temp/out/1.ali temp/out/phone_alined.ctm

python scripts/convert_ctm.py -i temp/out/align.ctm  -w temp/lang/words.txt -o $out_ctm

python scripts/convert_ctm.py -i temp/out/phone_alined.ctm  -w temp/lang/phones.txt -o $out_phone_ctm

copy-int-vector ark:temp/out/1.ali ark,t:$out_transid_seq