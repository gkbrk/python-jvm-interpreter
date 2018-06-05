from .JavaClass import JavaClass

class StringBuilder(JavaClass):
    def __init__(self):
        super().__init__()
        self.string = ''
        self.class_name = 'java/lang/StringBuilder'

    def canHandleMethod(self, name, desc):
        return name in ['append', 'toString']

    def handleMethod(self, name, desc, frame, code, machine, ip):
        if name == 'append':
            v2 = str(frame.stack.pop())
            v1 = frame.stack.pop()
            v1.string += v2
            frame.stack.append(v1)
        elif name == 'toString':
            v1 = frame.stack.pop()
            frame.stack.pop()
            frame.stack.append(v1.string)