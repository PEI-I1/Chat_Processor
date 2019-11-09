#Run with: python3 frequency_words_bi.py in.txt > out.txt

import sys, operator, re

filename = sys.argv[1]

with open(filename) as f:
    fw = {}

    for line in f.readlines():
        words = line.split()

        wls = []
        for word in words:
            wl = word.lower()
            if re.match(r'[-.:!,\'"#%&\/()[\]{}?]|\d+([.,]\d+)?|--', wl) == None:
                wls.append(wl)
        
        twograms = [" ".join(wls[i:i+2]) for i in range(len(wls)-(2-1))]

        for twogram in twograms:
            fw[twogram] = fw.get(twogram, 0) + 1

    sorted_fw = sorted(fw.items(), key=operator.itemgetter(1), reverse=True)

    for (key, value) in sorted_fw:
        if value == 50:
            break
        print(key + " " + str(value))
