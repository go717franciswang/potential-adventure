#!/usr/bin/env python

import re
from p2 import Part2

class Part3(Part2):
    def get_rare_replacement(self, x):
        if re.search('\d', x):
            return '_NUMERIC_'
        elif re.match('[A-Z]+$', x):
            return '_ALL_CAPITAL_'
        elif re.search('[A-Z]$', x):
            return '_LAST_CAPITAL_'
        else:
            return '_RARE_'

if __name__ == '__main__':
    p = Part3()
    # p.map_infreq_words_in_training_data('gene.train_rare2')
    # `python count_freqs.py gene.train_rare2 > gene.counts_rare2`
    p.load_count_freqs_file('gene.counts_rare2')
    # p.gen_viterbi_tags('gene.dev', 'gene_dev.p3.out')

    # `python eval_gene_tagger.py gene.key gene_dev.p3.out`
    # Found 415 GENEs. Expected 642 GENEs; Correct: 222.
    #          precision      recall          F1-Score
    # GENE:    0.534940       0.345794        0.420057

    p.gen_viterbi_tags('gene.test', 'gene_test.p3.out')


