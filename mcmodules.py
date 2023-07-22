#================================================================
class Module:
    def __init__(self):
        self.input_parameters = []
        self.output_parameters = []
        self.relationships = []
        self.name=''
        self.ID = []

    def add_input(self,inputparam):
        self.input_parameters.append(inputparam)

    def add_output(self,outputparam):
        self.output_parameters.append(outputparam)

    def add_relationships(self,relationship):
        #self.relationships.append(relationship)
        self.relationships=relationship

    def define_ID(self,ID):
        self.ID=ID

    def define_name(self,name):
        self.name=name

    def activate(self):
        self.active = 1

    def deactivate(self):
        self.active = 0

    def visualize(self):
        self.visualization = 1

    def execute(self):
        print('No instructions to execute')
        #This will be replaced with the instructions to execute in the module
