import csv

# Define a custom exception to handle specific error cases
class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Function to check if there are any active categories
def categoriesChecker(categories):
    activeCounter = 0 
    for value in categories.values():
        if(value): 
            activeCounter += 1
    if(not activeCounter):
        raise CustomError("no active categories")

# Database class to manage categories and their corresponding data
class Database:
    def __init__(self):
        # Dictionary to track the status of categories (active or inactive)
        self.categories = {
            "fruitsAndVegetables": False,
            "animals": False,
            "colors": False
        }

        # Dictionary to store content of each category
        self.content = {
            "fruitsAndVegetables": [],
            "animals": [],
            "colors": []     
        }

    # Method to set the status of categories (active/inactive)
    def setCategories(self, fruitsAndVegetables=0, animals=0, colors=0):
        self.categories["fruitsAndVegetables"] = fruitsAndVegetables
        self.categories["animals"] = animals
        self.categories["colors"] = colors

    # Method to pull content for a single category from a CSV file
    def pullSingleCategory(self, category):
        fileName = category + ".csv"
        try:
            with open(fileName, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    self.content[category].append(row)
        except FileNotFoundError:
            print(f"File {fileName} not found!")


    # Method to check and pull database categories
    def pullDatabase(self):
        try:
            categoriesChecker(self.categories)
        except CustomError as e:
            print(e)

        for key, value in self.categories.items():
            if value:
                self.pullSingleCategory(key)

    # Method to print the content of a specific category
    def printCategory(self, category):
        print(f"<=={category}==>")
        for row in self.content[category]:
            print(row)  

    # Method to print the whole db
    def printDatabase(self):
        for key, value in self.categories.items():
            if value:
                self.printCategory(key)


db = Database()
db.setCategories(fruitsAndVegetables=True,animals=True)
db.pullDatabase()
db.printDatabase()


