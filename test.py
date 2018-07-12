from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import sys
from ngram import Ngram
import numpy as np

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
                ngrams[key].occu_tot
            ngram = Ngram(tmp, n_doc)
            ngrams[key] = ngram
        tmp = []
    return ngrams

def get_max_occu(ngrams):
    res = None
    for k, i in ngrams.items():
        if res == None:
            res = i
            continue
        if res.occu_tot > i.occu_tot:
            res = i
    return res.occu_tot

def compute_tfidf(ngrams, nb_doc):
    max_occu = get_max_occu(ngrams)
    for k, item in ngrams:
        tf = item.occu_tot / max_occu
        idf = np.log(nb_doc / len(item.docs))
        item.tf_idf = tf * idf

def main(argv):
    text = convert_pdf_to_txt("doc.pdf")
    splited = re.findall(r"[\w']+", text)
    ngrams = {}
    ngrams = make_ngram(ngrams, splited, 2, 1)
    for key, item in ngrams.items():
        print(key)


if __name__ == "__main__":
    main(sys.argv[1:])

#ngram = Ngram(['toto'], 1)
#dico = {}
#dico[''.join(ngram.mot)] = ngram
#for key, item in dico.items():
#    print(key + " : ", item)
