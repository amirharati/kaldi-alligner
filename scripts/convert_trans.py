"""
  A script to generate refined transcriptions as input to Kaldi.
  The goal is to replace oovs with proper symbols and also add alternatives.
  This script is written with Aspire model in mind (having laughter, noise) markers.
  Amir Harati April 2018
"""
import argparse
import string 
# reptation of actual transcription
# We might want to make it sensetive to score.
R = 6

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_trans",
                       default=None, help="input transcription.")
    parser.add_argument("-o", "--output_trans",
                       default=None, help="output transcription.")
    parser.add_argument("-l", "--add_laughter", default=None,
                       help="add laughter")
    parser.add_argument("-n", "--add_noise", default=None,
                        help="add noise")
    parser.add_argument("-w", "--input_words",
                         default=None,
                        help="words for recognizer lexicon (in Kaldi format).")
    parser.add_argument("-u", "--unknown", default="<unk>", help="OOV symbol")
    #parser.add_argument("-g", "--use_g2p", default=False)
    args = parser.parse_args()

    if args.input_trans is None:
      print("You need to specify the input transcript.")
      exit(0)
    if args.output_trans is None:
      print("You need to specify the output transcript.")
      exit(0)
    if args.input_words is None:
      print("You need to specify the input wor list.")
      exit(0)

    ##exclude = set(string.punctuation)
    exclude = {'#', '+', '`', '^', '!', '\\', ';', '?', '{', '/', '|', '}', '~', '"', '(', "'", ']', '-', '>', '%', ')', '&', '=', '[', '@', '_', '.', '<', '*'}

    # read input transcript. One per line (in case multiple version existed)
    input_trans = [line.strip().lower() for line in open(args.input_trans)]

    # read input words
    input_words = [line.strip().split()[0] for line in open(args.input_words)]

    output_trans = []
    #loop over all trans
    # repeat the none expanded transcript
    # basiaclly bias the LM toward this.
    for r in range(R):
      for trans in input_trans:
        trans = trans.lower()
        trans = trans.replace(",", " ")
        trans = ''.join([ch for ch in trans if ch not in exclude])
        out_trans = ""
        for w in trans.split():
          if w in input_words:
            out_trans += w
          else:
            out_trans += args.unknown
          out_trans += " "
        out_trans = out_trans.strip()
        output_trans.append(out_trans)

    if args.add_laughter:
      out_trans = ""
      for w in trans.split():
        if w in input_words:
          out_trans += args.add_laughter + " " + w
        else:
          out_trans += args.add_laughter + " " + args.unknown
        out_trans += " "
      out_trans = out_trans.strip()
      output_trans.append(out_trans)

    if args.add_noise:
      out_trans = ""
      for w in trans.split():
        if w in input_words:
          out_trans += args.add_noise + " " + w
        else:
          out_trans += args.add_noise + " " + args.unknown
        out_trans += " "
      out_trans = out_trans.strip()
      output_trans.append(out_trans)


    fo = open(args.output_trans, "w")
    for tr in output_trans:
      fo.write(tr + "\n")
    fo.close()
if __name__ == "__main__":
    main()
