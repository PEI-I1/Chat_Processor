#Run with: python3 frequency_words.py in.txt > out.txt

import sys, operator, re

filename = sys.argv[1]

with open(filename) as f:
    fw = {}

    for line in f.readlines():
        words = line.split()

        for word in words:
            wl = word.lower()
            if re.match(r'[-.:!,\'"#%&\/()[\]{}?]|\d+([.,]\d+)?|--', wl) == None:
                fw[wl] = fw.get(wl, 0) + 1

    sorted_fw = sorted(fw.items(), key=operator.itemgetter(1), reverse=True)

    for (key, value) in sorted_fw:
        if value == 50:
            break
        print(key + " " + str(value))
