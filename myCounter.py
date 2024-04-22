class myTaskCounter:
    n=1
    def __init__(self):
        self.n=1
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 1000:
            result = self.n
            self.n += 1
            return f"Feature {result}:"
        else:
            raise StopIteration
    def reset(self):
        # setattr(self, 'n', 0)
        self.n = 1
        return f"Feature {self.n}:"

##a = myTaskCounter()
##for i in range(20):
##    n = next(a)
##    if i == 10:
##        print("Reseting counter: ", a.reset())
##        n = next(a) # next will
##        print(n)
##    else:
##        print(n)


