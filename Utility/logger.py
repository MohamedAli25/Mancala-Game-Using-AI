class Logger:
    def __init__(self):
        self.f = open("log.txt", "w")

    def __call__(self, txt):
        print(txt)
        self.f.write(txt)
        self.f.write("\n")

    def __del__(self):
        self.f.close()