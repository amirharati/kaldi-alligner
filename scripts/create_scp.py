"""
  A script to generate scp and spk2utt for Kaldi.
  Amir Harati April 2018
"""
import argparse
from shutil import copyfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_wav",
                       default=None, help="input wav file")
    parser.add_argument("-o", "--out_dir",
                       default=None, help="out directory")
    args = parser.parse_args()

    if args.input_wav is None:
      print("You need to specify the input wave file.")
      exit(0)

    if args.out_dir is None:
      print("You need to specify the out directory.")
      exit(0)

    parts = args.input_wav.split(".")
    base = parts[0]
    kaldi_base = "xxx_" + base  # xxx is the speaker
    new_file = kaldi_base + ".wav"

    copyfile(args.input_wav, args.out_dir + "/" + new_file)
    spk2utr = "xxx " + kaldi_base
    wav_scp = kaldi_base + " sox -c 1 -e signed -b 16 " + args.out_dir + "/" + new_file + " -t wav -r 8000 -|"

    fo = open(args.out_dir + "/spk2utt.scp", "w")
    fo.write(spk2utr + "\n")
    fo.close()

    fp = open(args.out_dir + "/wav.scp", "w")
    fp.write( wav_scp + "\n")
    fp.close()

if __name__ == "__main__":
    main()
