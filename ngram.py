class Ngram:
    def __init__(self, mot, doc):
        self.mot = mot
        self.occu_tot = 1
        self.docs = set()
        self.docs.add(doc)
        self.tf_idf = 0.0
