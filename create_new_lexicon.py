# create_new_lexicon.py
# Amir Harati, july 2019
"""
    create a new leixcon by adding g2p outputs to input leixcon.
"""
import argparse

import pandas as pd
import string
from g2p.g2p_en import G2p

def main():
    g2p = G2p()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_lexicon",
                       default=None, help="input lexicon")
    parser.add_argument("--input_segment_file",
                       default=None, help="input segment file")
    parser.add_argument("--output_lexicon", default=None,
                       help="output lexicon")
   
    args = parser.parse_args()

    if args.input_lexicon is None:
      print("You need to specify the input lexicon.")
      exit(0)
    if args.output_lexicon is None:
      print("You need to specify the output lexicon.")
      exit(0)
    if args.input_segment_file is None:
      print("You need to specify the input segment file.")
      exit(0)

    exclude = {'#', '+', '`', '^', '!', '\\', ';', '?', '{', '/', '|', '}', '~', '"', '(', "'", ']', '-', '>', '%', ')', '&', '=', '[', '@', '_', '.', '<', '*'}
    
    #printable = set(string.printable)

    lexicon = {}
    lines = [line.strip() for line in open(args.input_lexicon)]
    for line in lines:
        p = line.split()
        key = p[0]
        val = " ".join(p[1:])
        lexicon[key] = val
    
    segments = pd.read_csv(args.input_segment_file, sep="|")

    #trans = []
    words = set()
    for txt in segments["transcription"]:
        txt = txt.lower()
        txt = txt.replace(",", " ")
        txt = ''.join(ch for ch in txt if ch not in exclude)
        ws = txt.split()
        for w in ws:
            words.add(w.strip())
    words = list(words)

    for w in words:
        w = w.encode('ascii',errors='ignore').decode()
        if w not in lexicon:
            #print(w)
            trans = g2p(w)
            trans = [ch for ch in trans if ch not in list(exclude) + [","]]
            trans_converted = ' '.join([i.lower() for i in trans if i != " "])
            trans_converted = "".join([i for i in trans_converted if not i.isdigit()])
            #print("* ", trans_converted)
            lexicon[w] = trans_converted


    with open(args.output_lexicon, "w") as fo:
        for key in lexicon:
            fo.write(key + " " + lexicon[key] + "\n")

if __name__ == "__main__":
    main()
