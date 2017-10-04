# MGAD: Multilingual Generation of Analogy Datasets
_Submitted to LREC2018_

### Description
We present a novel, minimally supervised method of generating word embedding evaluation datasets for a large number of languages. Our approach utilizes existing dependency treebanks and parsers in order to create language-specific syntactic analogy datasets that do not rely on translation or human annotation. As part of our work, we offer syntactic analogy datasets for three previously unexplored languages: Arabic, Hindi, and Russian. *These can be found in the `data/` subdirectory.* 

### Usage
Prior to running `extract.py`, it is recommended that a feature template for generating synactic analogies be provided. The following is a sample template written for Hindi:

```
NOUN|Number=Plur|Case=Nom   NOUN|Number=Sing|Case=Nom
VERB|Aspect=Perf|Gender=Masc|Number=Sing|VerbForm=Part  VERB|Case=Nom|VerbForm=Inf
```

The features expressed here can be found at [the Universal Dependencies website](http://universaldependencies.org/u/feat/index.html). 

To run `extract.py`, enter the following command in terminal, where the corpus is a connllu-formatted UD treebank:

`cat corpus.connllu | python extract.py --all > output_file.txt`

###
