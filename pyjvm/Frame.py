class Frame:
    def __init__(self, code, current_class, machine):
        self.code = code.code
        self.stack  = []
        self.locals = [current_class] + [0 for i in range(code.max_locals)]
        self.current_class = current_class
        self.ip = 0
        self.machine = machine

    def set_local(self, i, value):
        self.locals[i] = value

    def get_local(self, i):
        return self.locals[i]

    def push(self, arg):
        self.stack.append(arg)

    def pop(self):
        return self.stack.pop()