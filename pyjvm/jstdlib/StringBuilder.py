from .JavaClass import JavaClass

class StringBuilder(JavaClass):
    def __init__(self):
        super().__init__()
        self.class_name = 'java/lang/StringBuilder'

    def python_initialize(self, *args):
        self.string = ''

    def canHandleMethod(self, name, desc):
        if name == '<init>' and desc == '(Ljava/lang/String;)V':
            return True
        
        return name in ['append', 'toString', 'reverse']

    def handleMethod(self, name, desc, frame):
        super().handleMethod(name, desc, frame)
        if name == 'append':
            v2 = str(frame.stack.pop())
            v1 = frame.stack.pop()
            v1.string += v2
            return v1
        elif name == 'toString':
            v1 = frame.stack.pop()
            return v1.string
        elif name == 'reverse':
            v1 = frame.stack.pop()
            v1.string = v1.string[::-1]
            return v1
        elif name == '<init>' and desc == '(Ljava/lang/String;)V':
            s = frame.stack.pop()
            v1 = frame.stack.pop()
            v1.string = s
