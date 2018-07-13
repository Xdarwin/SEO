import cmd

completions= ['toto', 'hihi', 'baba']


class myCmd(cmd.Cmd):
    def __init__(self, ngrams, result):
        cmd.Cmd.__init__(self)
        self.ngrams = ngrams
        if result == None:
            self.result = 10
        else:
            self.result = result


    def do_quit(self, s):
        return True

    def do_write(self, s):
        pass

    def complete_write(self, text, line, begidx, endidx):
        if not text:
            res = self.ngrams
        else:
            res = []
            for i in range(len(self.ngrams)):
                mot = ' '.join(self.ngrams[i].mot)
                if mot.startswith(text):
                    res.append(self.ngrams[i])
            min_res = min(len(res), self.result)
            print("\nThis is the best ngrams we can find:")
            for i in range(min_res):
                tmp = ' '.join(res[i].mot)
                print(tmp + " => score tf_idf: " + str(res[i].tf_idf))
        print(text, end='', flush=True)
        return res 

    """
    Print the nb first ngrams.
    """
    def print_ngrams(nb, ngrams):
        print("The most significant ngrams are: ")
        for i in range(nb):
            print(' '.join(ngrams[i].mot))
