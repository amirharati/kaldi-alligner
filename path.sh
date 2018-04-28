export KALDI_ROOT=/home/amir/Projects/kaldi
export PATH=$PWD/utils/:$KALDI_ROOT/src/bin:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/src/fstbin/:$KALDI_ROOT/src/gmmbin/:$KALDI_ROOT/src/featbin/:$KALDI_ROOT/src/lm/:$KALDI_ROOT/src/sgmmbin/:$KALDI_ROOT/src/sgmm2bin/:$KALDI_ROOT/src/fgmmbin/:$KALDI_ROOT/src/latbin/:$KALDI_ROOT/src/nnet2bin/:$KALDI_ROOT/src/nnetbin:$KALDI_ROOT/src/online2bin/:$KALDI_ROOT/src/ivectorbin/:$PWD:$PATH
#export LC_ALL=C
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$KALDI_ROOT/tools/srilm/lm/bin/i686-m64/:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
export PATH=$KALDI_ROOT/tools/sctk/bin:$PATH
export LC_ALL=C
