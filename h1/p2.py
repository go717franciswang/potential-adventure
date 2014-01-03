#!/usr/bin/env python

from decimal import *
from p1 import Part1

class Part2(Part1):

    def q(self, y_i0, y_i1, y_i2):
        tri = float(self.ngram.get((3, y_i2, y_i1, y_i0), 0))
        bi = float(self.ngram.get((2, y_i2, y_i1), 0))

        if tri == 0:
            return 0
        else:
            return tri / bi

    def S(self, k, length):
        tags = []
        if k < 0:
            tags.append('*')
        elif k >= length:
            tags.append('STOP')
        else:
            tags += ['O', 'I-GENE']

        return tags

    def viterbi(self, words):
        pi = {(-1,'*','*'): Decimal('1')}
        bp = {}
        length = len(words)
        op_tags = [''] * length
        op_tags.append('STOP')

        for k in range(length+1):
            for u in self.S(k-1, length):
                for w in self.S(k, length):
                    max_pi = 0
                    best_v = ''

                    e = 1
                    if k < length:
                        x = words[k]
                        if self.is_rare(x):
                            x = '_RARE_'
                        e = self.e(x,w)

                    for v in self.S(k-2, length):
                        this_pi = pi[(k-1,u,v)] * Decimal('%s' % (self.q(w,u,v) * e,))
                        if this_pi >= max_pi:
                            max_pi = this_pi
                            best_v = v

                    pi[(k,w,u)] = max_pi
                    bp[(k,w,u)] = best_v

        w = 'STOP'
        max_pi = 0
        for u in self.S(length-1, length):
            if pi[(length,w,u)] > max_pi:
                max_pi = pi[(length,w,u)]
                op_tags[length-1] = u


        for k in range(length-2, -1, -1):
            w = op_tags[k+2]
            u = op_tags[k+1]
            v = bp[(k+2,w,u)]

            op_tags[k] = v

        return op_tags[:-1]

    def gen_viterbi_tags(self, filepathin, filepathout):
        filein = file(filepathin, 'r')
        fileout = file(filepathout, 'w')
        line = filein.readline()
        sentence = []

        while line:
            line = line.strip()
            if line:
                sentence.append(line)
            else:
                tags = self.viterbi(sentence)
                for i in range(len(tags)):
                    word = sentence[i]
                    tag = tags[i]
                    fileout.write(word + ' ' + tag + '\n')

                fileout.write('\n')
                sentence = []

            line = filein.readline()

        filein.close()
        fileout.close()

if __name__ == '__main__':
    p = Part2()
    p.load_count_freqs_file('gene.counts_rare')
    # p.gen_viterbi_tags('gene.dev', 'gene_dev.p2.out')
    # `python eval_gene_tagger.py gene.key gene_dev.p1.out`
    p.gen_viterbi_tags('gene.test', 'gene_test.p2.out')

