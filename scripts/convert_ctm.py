"""
  A script to convert ctm with word_ids to ctm with words
  Amir Harati April 2018
"""
import argparse
from shutil import copyfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_ctm",
                       default=None, help="input ctm with word ids")

    parser.add_argument("-w", "--input_words",
                       default=None, help="input words")
    parser.add_argument("-o", "--output_ctm",
                       default=None, help="output ctm with words")
    args = parser.parse_args()

    if args.input_ctm is None:
      print("You need to specify the input ctm file.")
      exit(0)

    if args.input_words is None:
      print("You need to specify the input words.")
      exit(0)

    if args.output_ctm is None:
      print("You need to specify the output ctm file.")
      exit(0)

    id2word = {}
    lines = [line.strip() for line in open(args.input_words)]
    for line in lines:
      parts = line.split()
      id2word[parts[1]] = parts[0]


    lines = [line.strip() for line in open(args.input_ctm)]
    fo = open(args.output_ctm, "w")
    for line in lines:
      parts = line.split()
      pp = parts[0].split("_")
      new_line = pp[1] + " " + parts[1] + " " + parts[2] + " " + parts[3] + " " + id2word[parts[4]]
      fo.write(new_line + "\n")
    fo.close()

if __name__ == "__main__":
    main()
