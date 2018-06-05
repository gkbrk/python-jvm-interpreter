from .JavaClass import JavaClass

class String(JavaClass):
    def __init__(self):
        super().__init__()
        self.class_name = 'java/lang/String'

    def canHandleMethod(self, name, desc):
        return name in ['length', 'charAt']

    def handleMethod(self, name, desc, frame):
        super().handleMethod(name, desc, frame)
        if name == 'length':
            val = frame.pop()
            frame.push(len(val))
        elif name == 'charAt':
            index = frame.pop()
            s = frame.pop()
            frame.push(s[index])