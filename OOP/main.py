from Employee import Employee

def test():
    testList = [
                [1,2,3],
                [4,5,6],
                [7,8,9],
                [0]
    ]

def employeeClassEx():
    print("hello world")
    emp1 = Employee("Zara", 2000)
    emp2 = Employee("Manni", 5000)

    emp1.displayEmployee()
    emp2.displayEmployee()

    print("Total employee %d", Employee.empCount)

def main():
    employeeClassEx()


if __name__ == '__main__':
    main()
