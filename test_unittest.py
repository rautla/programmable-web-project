#import random
from myclass import MyClass
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.something = MyClass("pekka")

    def test_return(self):
        name = self.something.get_name()
        self.assertEqual(name, "pekka")
            
        
if __name__ == '__main__':
    unittest.main()