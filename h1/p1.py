#! /usr/bin/python

class Part1:
    def __init__(self):
        self.wordtag = {}
        self.igram = {}
        self.wordcount = {}
        self.infrequent_wordcount = {}
        self.tags = set()

    def load_count_freqs_file(self, file_path):
        filein = file(file_path, 'r')
        line = filein.readline()

        while line:
            line = line.strip()
            if line:
                items = line.split(' ')
                count = int(items[0])
                category = items[1]

                if category == 'WORDTAG':
                    tag = items[2]
                    word = items[3]
                    self.wordtag[(tag,word)] = count

                    if not self.wordcount.has_key(word):
                        self.wordcount[word] = 0
                    self.wordcount[word] += count

                else:
                    i = int(category[0])
                    tags = items[2:]
                    key = tuple([i] + tags)
                    self.igram[key] = count

                    for tag in tags:
                        self.tags.add(tag)

            line = filein.readline()

    def get_emission(self, x, y):
        if self.wordtag.has_key((y,x)):
            return float(self.wordtag[(y,x)]) / self.igram[(1,y)]
        elif self.wordtag.has_key((y,'_RARE_')):
            return float(self.wordtag[(y,'_RARE_')]) / self.igram[(1,y)]
        else:
            return 0

    def get_op_tag(self, x):
        max_emission = 0
        op_tag = ''

        for tag in self.tags:
            e = self.get_emission(x, tag)
            if e > max_emission:
                max_emission = e
                op_tag = tag

        return op_tag

    def map_infreq_words_in_training_data(self, freq_threshold):
        self.load_count_freqs_file('gene.counts')
        self.get_infrequent_word_count(freq_threshold)
        self.transform_training_data()

    def get_infrequent_word_count(self, freq_threshold):
        for (word,count) in self.wordcount.items():
            if count < freq_threshold:
                self.infrequent_wordcount[word] = count

    def transform_training_data(self):
        filein = file('gene.train', 'r')
        fileout = file('gene.train_rare', 'w')
        line = filein.readline()

        while line:
            line = line.strip()
            if line:
                items = line.split(' ')
                if self.infrequent_wordcount.has_key(items[0]):
                    items[0] = '_RARE_'

                line = ' '.join(items) + '\n'
                fileout.write(line)

            line = filein.readline()

        filein.close()
        fileout.close()

    def gen_baseline(self, filepathin, filepathout):
        filein = file(filepathin, 'r')
        fileout = file(filepathout, 'w')
        line = filein.readline()

        while line:
            line = line.strip()
            if line:
                tag = self.get_op_tag(line)
                fileout.write(line + ' ' + tag + '\n')
            else:
                fileout.write('\n')

            line = filein.readline()

        filein.close()
        fileout.close()

if __name__ == '__main__':
    p = Part1()
    # `python count_freqs.py gene.train > gene.counts`
    # p.map_infreq_words_in_training_data(5)
    # `python count_freqs.py gene.train_rare > gene.counts_rare`
    p.load_count_freqs_file('gene.counts_rare')
    p.gen_baseline('gene.dev', 'gene_dev.p1.out')
    # `python eval_gene_tagger.py gene.key gene_dev.p1.out`
    # p.gen_baseline('gene.test', 'gene_test.p1.out')



