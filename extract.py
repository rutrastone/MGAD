import sys, nltk, pdb
from itertools import product


# core
core = {}
out = []


template = """
NOUN|Number=Plur    NOUN|Number=Sing
"""

template_ar = """
NOUN|Number=Plur|Case=Nom|Definite=Ind   NOUN|Number=Sing|Case=Nom|Definite=Ind
NOUN|Number=Plur|Case=Acc|Definite=Ind   NOUN|Number=Sing|Case=Acc|Definite=Ind
NOUN|Number=Plur|Case=Gen|Definite=Ind   NOUN|Number=Sing|Case=Gen|Definite=Ind
NOUN|Number=Sing|Case=Acc|Definite=Ind   NOUN|Number=Sing|Case=Nom|Definite=Ind
NOUN|Number=Sing|Case=Gen|Definite=Ind   NOUN|Number=Sing|Case=Nom|Definite=Ind
NOUN|Number=Sing|Case=Gen|Definite=Ind   NOUN|Number=Sing|Case=Acc|Definite=Ind
VERB|Aspect=Imp|Gender=Masc|Person=3|Number=Sing    VERB|Aspect=Perf|Gender=Masc|Person=3|Number=Sing
VERB|Aspect=Imp|Gender=Masc|Person=3|Number=Plur    VERB|Aspect=Perf|Gender=Masc|Person=3|Number=Plur
VERB|Aspect=Imp|Gender=Masc|Person=3|Number=Sing    VERB|Aspect=Imp|Gender=Masc|Person=3|Number=Plur
VERB|Aspect=Perf|Gender=Masc|Person=3|Number=Sing   VERB|Aspect=Perf|Gender=Masc|Person=3|Number=Plur
"""

template_ru = """
NOUN|Number=Plur|Case=Nom   NOUN|Number=Sing|Case=Nom
VERB|Person=3|Number=Sing|Tense=Pres    VERB|Aspect=Imp|VerbForm=Inf
VERB|VerbForm=Part|Number=Sing|Case=Nom|Tense=Past|Gender=Masc  VERB|Aspect=Imp|VerbForm=Inf
VERB|Number=Sing|Tense=Past|Gender=Masc VERB|Aspect=Imp|VerbForm=Inf
VERB|Person=3|Number=Sing|Tense=Pres    VERB|VerbForm=Part|Number=Sing|Case=Nom|Tense=Past|Gender=Masc
VERB|Person=3|Number=Sing|Tense=Pres    VERB|Number=Sing|Tense=Past|Gender=Masc
VERB|VerbForm=Part|Number=Sing|Case=Nom|Tense=Past|Gender=Masc  VERB|Number=Sing|Tense=Past|Gender=Masc
"""

template = template_ar

def check_tags(s, tags, disallow=[]):
    out = True
    for i in tags:
        out = out and i in s
    
    for i in disallow:
        out = out and i not in a

    return out

def build_deriv(b1, b2):
    out = []
    for lemma, form in b1:
        try:
            out.append((form, dict(b2)[lemma]))
        except:
            pass

    return out

# read template
for line in template.split("\n"):
    if line == "":
        continue
    x, y = line.split()
    core[x], core[y] = [], []


lines = sys.stdin.readlines()
sys.stdin = open('/dev/tty')

for line in lines:
    if '#' in line:
        continue

    try:
        cols = line.split("\t")
        word = cols[1]
        lemma = cols[2] 
        pos = cols[3]
        feats = cols[5]
    except:
        continue

    for i in core.keys():
        t_pos, t_feats = i.split("|", maxsplit=1)
        if pos == t_pos and check_tags(feats, t_feats.split("|")):
            core[i].append((lemma, word))


for line in template.split("\n"):
    if line == "":
        continue
    x, y = line.split()
    out.append(build_deriv(core[x], core[y]))    

 
if sys.argv[1] == '--debug':
    [print(len(i)) for i in out]

else:
    sys.stdout.write(": test\n")
    freqs = [nltk.FreqDist(i) for i in out]
    out = [[j[0] for j in i.most_common(50)] for i in freqs]

    for I in out:
        for i in product(I, I):
            sys.stdout.write("{} {} {} {}\n".format(i[0][0], i[0][1], i[1][0],
                                                    i[1][1]))
   
'''
    # regular plurals
    if pos == 'NOUN' and check_tags(feats, ['Plur', 'Nom', 'Definite=Ind']):
        I01.append((cols[2], w))

    # acc
    if pos == 'NOUN' and check_tags(feats, ['Sing', 'Acc', 'Definite=Ind']):
        I02.append((cols[2], w))

    # gen
    if pos == 'NOUN' and check_tags(feats, ['Sing', 'Gen', 'Definite=Ind']):
        I03.append((cols[2], w))

    # +3MSg+Impf : +3MSg+Perf
    if pos == 'VERB' and check_tags(feats, ['Aspect=Imp', 'Gender=Masc',
                                            'Person=3', 'Number=Sing',
                                            'VerbForm=Fin'], ['Mood']):
        I04.append((cols[2], w))

    # +3MPl+Impf : 
    if pos == 'VERB' and check_tags(feats, ['Aspect=Imp', 'Masc',
                                            'VerbForm=Part', 'Sing',
                                            'Person=3']):
        I06.append((cols[2], w))

    # past
    if pos == 'VERB' and check_tags(feats, ['VerbForm=Conv']):
        I07.append((cols[2], w))

build_deriv(I08, I06, I05)
build_deriv(I09, I06, I07)
build_deriv(I10, I05, I07)

final = [I01, I05, I06, I07, I08, I09, I10]

'''                                                    
