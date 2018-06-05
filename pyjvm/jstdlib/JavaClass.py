class JavaClass:
    def __init__(self):
        self.methods = []
        self.fields = []
        self.attributes = []

        self.instance_fields = {}
        self.file_path = None
        self.class_name = 'java/lang/Object'
        self.static_initialized = False
        self.initialized = False

    def name(self):
        return self.class_name

    def python_initialize(self, *args):
        pass

    def __repr__(self):
        return '<{} - {}>'.format(self.name(), self.instance_fields)

    def get_field(self, name):
        return self.instance_fields[name]

    def set_field(self, name, value):
        self.instance_fields[name] = value

    def canHandleMethod(self, name, desc):
        pass

    def handleMethod(self, name, desc, frame):
        pass