class Frame:
    def __init__(self, maxStack, maxLocal):
        self.stack  = []
        self.locals = [0 for i in range(maxLocal)]

    def set_local(self, i, value):
        self.locals[i] = value

    def get_local(self, i):
        return self.locals[i]