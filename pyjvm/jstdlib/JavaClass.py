class JavaClass:
    def __init__(self):
        self.methods = []
        self.fields = []
        self.attributes = []

        self.instance_fields = {}
        self.file_path = None
        self.class_name = 'java/lang/Object'

    def name(self):
        return self.class_name

    def __repr__(self):
        return '<{} - {}>'.format(self.name(), self.instance_fields)

    def get_field(self, name):
        return self.instance_fields[name]

    def set_field(self, name, value):
        self.instance_fields[name] = value

    def canHandleMethod(self, name, desc):
        return False

    def handleMethod(self, name, desc, frame, code, machine, ip):
        pass