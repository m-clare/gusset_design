class Employee:

    __Tax= 0.6 

    def __init__(self, name, salary):
        self._name = name
        self._salary = salary

    @property
    def salary(self):
        tax_amount = self._salary * (Employee.__Tax / 100 ) 
        return self._salary - tax_amount

    @salary.setter
    def salary(self, value):
        self._salary = value
    
    @salary.deleter
    def salary(self):
        del self._salary

if __name__ == '__main__':
    emp = Employee('John Doe', 3000)
    print(emp.salary)
    emp.salary = 1000000
    print(emp.salary)
    del emp.salary