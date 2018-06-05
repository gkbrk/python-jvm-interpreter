from .JavaClass import JavaClass

def argumentCount(desc):
    arg = desc.split(')', 2)[0][1:]
    i = 0

    parsingClass = False
    for c in arg:
        if parsingClass:
            if c == ';':
                parsingClass = False
            continue
        if c == 'L':
            parsingClass = True
        i += 1

    return i

class PrintStream(JavaClass):
    def __init__(self):
        super().__init__()
        self.class_name = 'java/io/PrintStream'

    def canHandleMethod(self, name, desc):
        return name in ['println']

    def handleMethod(self, name, desc, frame):
        if name == 'println':
            for i in range(argumentCount(desc)):
                print(frame.stack.pop())
            frame.stack.pop()
