class MyClass:

    def __init__(self,name):
        self.name = name

    def reverse_name(self):
        self.name = self.name[::-1]
        
    def print_name(self):
        print self.name

    def get_name(self):
        #return self.name
        return "herp"
        
if __name__ == '__main__':
    something = MyClass("pekka")
    something.print_name()
    something.reverse_name()
    something.print_name()