class Homework():
    
    def __init__(self,number):
        self.number = number
    
    
    def add_3(self, number):
        self.number += 5

    def multi(self, number)
        self.number *= number
    
    def subtract(self, number):
        self.number -= number

    def divide(self, number):
        if number != 0:
            self.number /= 0
        else:
            raise ValueError("Can't divide by zero.")
            
    def power(self, exponent):
        self.number **= exponent
