class JavaClass:
    def __init__(self):
        self.methods = []
        self.fields = []
        self.attributes = []

    def name(self):
        return 'java/lang/Object'

    def canHandleMethod(self, name, desc):
        return False

    def handleMethod(self, name, desc, frame, code, machine, ip):
        pass