import pandas as pd
import json
import sys

expenses = []
globalBudgetAmt = 0

def addExpense(expenses):
    date = str(input("Enter date of the expense (YYYY-MM-DD): "))
    category = input("Enter the category of the expense: ")
    amtSpent = str(input("Enter the amount spent in USD: "))
    description = input("Enter short description of expense: ")

    expenses.append({"Date": date, "Category": category, "Amount in USD": amtSpent, "Description": description})
    print("Expense added successfully")
    
    newExpense = input("Would you like to add another expense? Y/N: ")

    if(newExpense.lower() == "y"):
        addExpense(expenses)
    elif(newExpense.lower() == "n"):
        displayMenu()
    else:
        print("Invalid Entry")

    displayMenu()

def viewExpenses(expenses):
    numExpenses = len(expenses)
    if(numExpenses == 0):
        print("You have no expenses to view, please add one")
        displayMenu()
    
    for expense in expenses:
        #print(expense)
        if(expense.get("Date") == ""):
            print("Date for this expense is missing.")
        elif(expense.get("Category") == ""):
            print("Category for this expense is missing.")
        elif(expense.get("Amount in USD") == "") or (expense.get("Amount in USD") == 0):
            print("Amount for this expense is either missing or 0.")
        elif(expense.get("Description") == ""):
            print("This expense is missing a description.")
        else:
            print(expense)
    displayMenu()

def setBudget():
    global globalBudgetAmt
    if(globalBudgetAmt == 0):
        globalBudgetAmt = int(input("What is your total budget in USD? "))

    choice = input(f"Would you like to update your current budget? It is currently {globalBudgetAmt}, Y/N")
    
    if(choice.lower() == "y"):
        globalBudgetAmt = input("Enter the new desired budget in USD: ")
    elif(choice.lower() == "n"):
        calculateExpense(expenses, globalBudgetAmt)
    else:
        print("Invalid response")
        setBudget(globalBudgetAmt)
    displayMenu()

def calculateExpense(expenses, budgetAmt):
    sum = 0
    if(len(expenses) == 0):
        print("You have not logged any expenses, please add 1")

    for expense in expenses:
        amount = int(expense.get("Amount in USD"))
        #print(amount)
        sum += amount
    
    if(sum < budgetAmt):
        print("There is still ", budgetAmt - sum, "left in your budget.")
    elif(sum > budgetAmt):
        print("You are over your budget by ", budgetAmt + sum, ".")
    displayMenu()

def saveExpenses(expense):
    df = pd.DataFrame(expenses)
    df.to_csv("expenses", index=False)
    #Not sure about the return value to verify if saved, just return successful save string
    return "CSV saved"

def readExpenses():
    path = input("Input file path where file is saved")
    df = pd.read_csv(path)
    expenses = df.to_dict(orient='records')
    print(expenses)
    return expenses

def displayMenu():
    choice = "0"
    print("\nWelcome to your personal expense tracker!\n\nWhat would you like to do?")
    list = ["1: Add an expense\n", "2: View your expenses\n", "3: Create or track your budget\n",
            "4: Save your expenses to an external file\n", "5: Save your current expenses and exit\n"]
    for choice in list:
        print(choice)
    
    choice = int(input("Make your selection 1-5: "))
    #print(type(choice))
    while choice != int("5"):
        if(choice < int("1") or choice > int("5")):
            print("Invalid Choice")
            displayMenu()
        else:
            if(choice == int("1")):
                print(globalBudgetAmt)
                addExpense(expenses)
            elif(choice == int("2")):
                viewExpenses(expenses)
            elif(choice == int("3")):
                setBudget()
            elif(choice == int("4")):
                response = saveExpenses(expenses)
                print(response)
                displayMenu()
            elif(choice == int("5")):
                saveExpenses(expenses)
                break

    
displayMenu() 

