# extract_likelihood_per_frame.py
# Amir Harati, AUg 2019
"""
    Extract the likelihood per frame
"""
import sys
import re
pat = ".*Overall\s+likelihood\s+per\s+frame\s+was\s+(.*)\s+per.*"
lpf = "-1000.0"
def main():
    inp = sys.argv[1]
    out = sys.argv[2]
    lines = [line for line in open(inp)]
    for line in lines:
        m = re.match(pat, line)
        if  m is not None:
            lpf = m.group(1)
            break
        
    with open(out, "w") as fo:
        fo.write(lpf + "\n")



if __name__ == "__main__":
    main()
