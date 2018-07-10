from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import sys
from ngram import Ngram

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
def make_ngram(splited, n, n_doc):
    tmp = []
    ngrams = []
    len_splited = int((len(splited) / n) + 0.5)
    print(len_splited)
    for i in range(0, len_splited):
        for j in range(0, n):
            if i * n + j < len( splited):
                tmp.append(splited[i * n + j])
        ngram = Ngram(tmp, n_doc)
        ngrams.append(ngram)
        tmp = []
    return ngrams

def main(argv):
    text = convert_pdf_to_txt("doc.pdf")
    splited = re.findall(r"[\w']+", text)
    ngrams = make_ngram(splited, 4, 1)
    for i in range(len(ngrams)):
        print(ngrams[i].mot)


if __name__ == "__main__":
    main(sys.argv[1:])


