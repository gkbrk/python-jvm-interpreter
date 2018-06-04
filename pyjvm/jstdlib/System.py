from .JavaClass import JavaClass

class System(JavaClass):
    def __init__(self):
        super().__init__()
        pass

    def canHandleMethod(self, name, desc):
        return name in ['append', 'toString']

    def handleMethod(self, name, desc, frame, code, machine, ip):
        if name == 'append':
            v2 = str(frame.stack.pop())
            v1 = str(frame.stack.pop())
            frame.stack.append(v1 + v2)
        elif name == 'toString':
            v1 = frame.stack.pop()
            frame.stack.pop()
            frame.stack.append(v1)