from pymongo import MongoClient

client = MongoClient('mongodb://192.168.151.14:27017/')
db = client['tutor']


def main():
    while (1):
        # chossing option to do CRUD operations
        selection = input('\nSelect 1 to insert, 2 to update, 3 to read, 4 to delete\n')

        if selection == '1':
            insert()
        elif selection == '2':
            update()
        elif selection == '3':
            read()
        elif selection == '4':
            delete()
        else:
            print('\n INVALID SELECTION \n')


# Function to insert data into mongo db
def insert():
    employeeId = input('Enter Employee id :')
    employeeName = input('Enter Name :')
    employeeAge = input('Enter age :')
    employeeCountry = input('Enter Country :')

    db.tutor.insert_one(
        {
            "id": employeeId,
            "name": employeeName,
            "age": employeeAge,
            "country": employeeCountry
        })
    print('\nInserted data successfully\n')


def read():
    empCol = db.tutor.find()
    print('\n All data from EmployeeData Database \n')
    for emp in empCol:
        print (emp)


def update():
    criteria = input('\nEnter id to update\n')
    name = input('\nEnter name to update\n')
    age = input('\nEnter age to update\n')
    country = input('\nEnter country to update\n')

    db.tutor.update_one(
        {"id": criteria},
        {
            "$set": {
                "name": name,
                "age": age,
                "country": country
            }
        }
    )
    print("\nRecords updated successfully\n")


def delete():

    criteria = input('\nEnter employee id to delete\n')
    db.tutor.delete_many({"id": criteria})

    print ('\nDeletion successful\n')

if __name__ == '__main__':
    main()
