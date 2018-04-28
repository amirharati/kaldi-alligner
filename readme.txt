Kaldi Aligner: A simple script to create time alignment for given speech/transcription pairs.
This script also enrich the transcription using [laughter] and [noise] markers.
It does not use the forced-alignment instead it creates a bigram LM using the input transcription (after enriching the transcription with markers).
After creating a language model it create an HCLG graph and use Kaldi decoder to generate a lattice and finally use the lattice to obtain alignment information.

requirements:
1- Kaldi tool.
2- SRILM (also existed under Kaldi/tools)
3- Python 3
4- bash (only tested under Linux)

After installing Kaldi and SRILM:
open path.sh and update export KALDI_ROOT=/home/amir/Projects/kaldi to your kaldi path.
Also make sure SRILM binaries (specifically ngram-count) is in the PATH.

Before running the aligner:
Download the pretrained Aspire chain model by running:
sh sownload_extract.sh
This  script downloads the model and also run some commands for preparation.
Alternatively, you can train your own model. However, you might need to update the scripts accordingly.

Example:
bash align.sh example/trans.txt example/test.wav  out.ctm

cat out.ctm
test.wav 1 0.070 0.840 [noise]
test.wav 1 0.910 0.320 my
test.wav 1 1.240 0.300 name
test.wav 1 1.540 0.340 is
test.wav 1 1.880 0.300 [noise]
test.wav 1 2.180 0.780 [laughter]
test.wav 1 2.960 0.600 [noise]
test.wav 1 3.630 0.360 amir
test.wav 1 4.000 0.480 <unk>
test.wav 1 4.510 1.610 [noise]

Notice OOVs are replaced with <unk>. The scripts adds [noise]/[laughter] markers when needed.
