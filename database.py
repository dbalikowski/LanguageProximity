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
    def setCategories(self, fruitsAndVegetables, animals, colors):
        self.categories["fruitsAndVegetables"] = fruitsAndVegetables
        self.categories["animals"] = animals
        self.categories["colors"] = colors

    # Method to pull content for a single category from a CSV file
    def pullSingleCategory(self, category):
        fileName = category + ".csv"  
        with open(fileName, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                self.content[category].append(row)

    # Method to check and pull database categories
    def pullDatabase(self):
        try:
            categoriesChecker(self.categories)
        except CustomError as e:
            print(e)

    # Method to print the content of a specific category
    def printCategory(self, category):
        for row in self.content[category]:
            print(row)  


