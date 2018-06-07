from .JavaClass import JavaClass

class StringBuilder(JavaClass):
    def __init__(self):
        super().__init__()
        self.class_name = 'java/lang/StringBuilder'

    def python_initialize(self, *args):
        self.string = ''

    def canHandleMethod(self, name, desc):
        return name in ['append', 'toString']

    def handleMethod(self, name, desc, frame):
        super().handleMethod(name, desc, frame)
        if name == 'append':
            v2 = str(frame.stack.pop())
            v1 = frame.stack.pop()
            v1.string += v2
            return v1
            #frame.stack.append(v1)
        elif name == 'toString':
            v1 = frame.stack.pop()
            frame.stack.pop()
            #frame.stack.append(v1.string)
            return v1.string