# map_kaldi_transitionids.py
# Amir Harati, July 2019
"""
    map transitionids into phoneme states.
"""
import argparse
import re

pat1  = re.compile("\s*Transition-state.*phone\s+=\s+(.*)\s+hmm-state\s+=\s+(.*)\s+pdf.*")
pat2  = re.compile("\s*Transition-id\s+=\s+(.*)\s+p.*")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_transitions", default=None, help="transition file")
    parser.add_argument("--input",
                       default=None, help="input transitionid")
    parser.add_argument("--output",
                       default=None, help="output mapped file")

   
    args = parser.parse_args()

    if args.input_transitions is None:
      print("You need to specify the input transitions")
      exit(0)  
    if args.input is None:
      print("You need to specify the input")
      exit(0)
    if args.output is None:
      print("You need to specify the output")
      exit(0)
 

    lines = [line.strip() for line in open(args.input)]
    input_trs = {}
    for line in lines:
        parts = line.split()
        input_trs[parts[0]] = parts[1:]

    lines = [line.strip() for line in open(args.input_transitions)]

    trans2state = {}
    for line in lines:
        x = pat1.match(line)
        y = pat2.match(line)
        if x is not None:
            curr_phoneme = x.group(1).split("_")[0]
            curr_state = x.group(2)
        #print(line)
        #print(y)
        if y is not None:
            ti = y.group(1)
            #print(ti)
            trans2state[ti] = curr_phoneme + "_" + curr_state

    #print(trans2state)
    with open(args.output, "w") as fo:
        for key in input_trs:
            fo.write(key + " ")
            for v in input_trs[key]:
                fo.write(trans2state[v] + " ")
            fo.write("\n")


if __name__ == "__main__":
    main()


