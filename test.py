from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import sys
from ngram import Ngram
import numpy as np
import argparse
import os.path

# taken from stackoverflow.com/questions/26494211/extracting-text-from-file-using-pdfminer-in-python
def convert_pdf_to_txt(path):
    rsrmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password="", caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

"""
Get the n-grams of the text given in parameter.
A n-gram is a group of n words.

:param splitted: list containing the text 
:type list
:param n: the number of words in a ngram
:type int
:param n_doc: number of the doc we found the word
:type int

:return: the ngrams
:typer: list
"""
def make_ngram(ngrams, splited, n, n_doc):
    tmp = []
    for i in range(0, len(splited)):
        for j in range(0, n):
            if i + j < len(splited):
                tmp.append(splited[i + j])
        if len(tmp) == n:
            key = ' '.join(tmp)
            if key in ngrams:
                ngrams[key].occu_tot += 1
                ngrams[key].docs.add(n_doc)
            else:
                ngram = Ngram(tmp, n_doc)
                ngrams[key] = ngram
        tmp = []
    return ngrams

"""
Get the ngram with highest occurence.

:param ngrams: the dictionnary of ngrams
:type dict

:return: the nb of ngram with highest occurence.
:typer: int
"""
def get_max_occu(ngrams):
    res = None
    for k, i in ngrams.items():
        if res == None:
            res = i
            continue
        if res.occu_tot > i.occu_tot:
            res = i
    return res.occu_tot

"""
Compute the TF-IDF of each ngram
"""
def compute_tfidf(ngrams, nb_doc):
    max_occu = get_max_occu(ngrams)
    for k in ngrams:
        item = ngrams[k]
        tf = item.occu_tot / max_occu
        tmp = nb_doc / len(item.docs)
        idf = np.log(tmp)
        item.tf_idf = tf * idf
    return ngrams

def compute_files(argv):
    docs = argv['documents']
    ngram_degree = argv['ngram_degree']
    nb_doc = 0
    ngrams = {}
    for f in docs:
        if not os.path.isfile(f):
            continue
        nb_doc += 1
        text = convert_pdf_to_txt(f)
        splited = re.findall(r"[\w']+", text)
        ngrams = make_ngram(ngrams, splited, ngram_degree, nb_doc + 1)
    return ngrams, nb_doc

"""
Sort the ngrams by the number of occurence.
Return a list
"""
def sort_ngrams(ngrams):
    list_ngrams = []
    for k, item in ngrams:
        list_ngrams.append(item)
    res = sorted(list_ngrams, key=lambda ngram: ngrams.occu_tot)
    return res

"""
Print the nb first ngrams.
"""
def print_ngrams(nb, ngrams):
    for i in range(nb):
        print(ngrams[i])

def main(argv):
    if argv['ngram_degree'] == None:
        argv['ngram_degree'] = 3
    if argv['result'] == None:
        argv['result'] = 10
    ngrams, nb_doc = compute_files(argv)
    if nb_doc == 0 or len(ngrams) == 0:
        print("No documents found or those files are empty")
        return
    ngrams = compute_tfidf(ngrams, nb_doc)
    ngrams_sorted = sort_ngrams(ngrams)
    print_ngrams(argv['result'], ngrams_sorted)

def defparser():
    parser = argparse.ArgumentParser(description="Compute the firsts significants ngrams of the provided PDF documents")
    parser.add_argument('-n', '--ngram-degree', metavar='deg', type=int, nargs='?', action='store', help="Degree of ngrams. Default is 3")
    parser.add_argument('-r', '--result', metavar='res', type=int, nargs='?', action='store', help="Get the r first significant ngrams. Default is 10.")
    parser.add_argument('documents', metavar='docs', type=str, nargs='+', action="store", default="", help="Documents to analyse")
    return parser


if __name__ == "__main__":
    parser = defparser()
    argv = vars(parser.parse_args())
    main(argv)
