import sys, nltk
from itertools import product

# core
I01, I02, I03, I04, I05, I06, I07, I08, I09, I10 = [[] for i in range(10)]

# derivative
I08, I09, I10 = [[], [], []]

def check_tags(s, tags):
    out = True
    for i in tags:
        out = out and i in s
       
    return out

def build_deriv(out, b1, b2):
    for lemma, form in b1:
        try:
            out.append((form, dict(b2)[lemma]))
        except:
            pass

for line in sys.stdin:
    if '#' in line:
        continue

    try:
        cols = line.split("\t")
        w = cols[1]
        pos = cols[3]
        feats = cols[5]
    except:
        continue

    # regular plurals
    if pos == 'NOUN' and check_tags(feats, ['Plur', 'Nom']):
        I01.append((cols[2], w))

    # irregular plurals
    I02 = []

    # comp
    I03 = []
    
    # sup
    I04 = []

    # inf
    if pos == 'VERB' and check_tags(feats, ['Person=3', 'Sing', 'Pres']):
        I05.append((cols[2], w))

    # pprs
    if pos == 'VERB' and check_tags(feats, ['Part', 'Number=Sing', 'Case=Nom',
                                            'Tense=Past', 'Gender=Masc']):
        I06.append((cols[2], w))

    # past
    if pos == 'VERB' and check_tags(feats, ['Number=Sing', 'Past',
                                            'Gender=Masc']):
        I07.append((cols[2], w))

build_deriv(I08, I06, I05)
build_deriv(I09, I06, I07)
build_deriv(I10, I05, I07)

final = [I01, I05, I06, I07, I08, I09, I10]

if sys.argv[1] == '--debug':
    [print(len(i)) for i in final]

else:
    freqs = [nltk.FreqDist(i) for i in final]
    final = [[j[0] for j in i.most_common(50)] for i in freqs]

    for I in final:
        for i in product(I, I):
            sys.stdout.write("{} {} {} {}\n".format(i[0][0], i[0][1], i[1][0],
                                                    i[1][1]))
