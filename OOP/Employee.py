class Employee:
    empCount = 0;                      #empCount is a public variable

    def __init__(self, name, salary):  #constructor name, salary are private variables
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("total employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name : ", self.name, "Salary : ", self.salary)


class HighlyPaidEmployees(Employee):
    specialEmployeeCount = 0;

    def __init__(self,name,salary):
        self.name = name
        self.salary = salary+100
        Employee.empCount +=1
        HighlyPaidEmployees.specialEmployeeCount += 1


    # def displayEmployee(self):
    #     print("Name: ",self.name, "Salary: ", self.salary)


class EmptyClassExample:
    pass
    def EmptyMemberExample(self):
        pass