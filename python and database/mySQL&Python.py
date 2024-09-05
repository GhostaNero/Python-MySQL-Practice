import os
import sys
import mysql.connector
import ignore
import pandas as pd
import sqlalchemy
import time
import text as tx
PASSWORD = ignore.password


def bold(type): 
    sys.stdout.write("\033[1m" + type + "\033[0m") 


def initiate():

    #Initiate path to the database
    path = "C:\Coding Portfolio\Python\python and database\dataset\data"

    #read all file name into a list
    try:
        listFile = os.listdir(path)
    except:
        print("Error 01: Cannot load the csv file names into a list")
        sys.exit()
        
    #declare an empty list with the length of the listFile
    listName = [""] * len(listFile)


    #removes the csv extension and this allows the listName to be used to check if the country code the user inputed was correct
    for i in range(0,len(listFile)):
        listName[i] = listFile[i].replace(".csv", "")
    
    
    return listFile, listName


def codeFunction(list):
    
    #asks user for input
    userInput = input("Please type in the country code to search! \nNote: If left blank the program will display every country code. \nInput: ")
    
    #if the input exists:
    if userInput:
        
        for i in range(len(list)):
            #if found return the code
            if userInput == list[i]:
                print("Exists")
                return 0
                 
                    
    #if user left it blank then return false       
    else:
        for i in range(len(list)):
            print(list[i], end=", ")
        print("\n")
        return 0

    #else then its definitetly not found, display error code
    print("Error: Country Code not found.")
    
    #initiate a list of the potential code that could've been
    potential = [""]
    boolean = False
    #initiate a loop to find the potential code by matching the first letter of the user input to all the country code
    for i in range(len(list)):
        
        if userInput[0:1] in list[i][0:1]:
            boolean = True
            potential.append(list[i])
    #if suggestion is found        
    if boolean == True:
        print("Did you mean: ", end="")
        for i in range(len(potential)):
            print(potential[i], end = " ")
  
    #quit 
    print("\n")
    return 0 


def askName():
    
    #title to display
    bold("\nName Search!")
    #user info
    print("\nIf either first name or second name is left blank. \nThe returned result will be a number if the result exceed more than 30 people. \nLeaving it blank will result in a number result.")
    firstName = input("\nPlease enter the FIRST name for your desired search. \nError will be displayed if numeric value is typed in. \nInput: ")
    print("\n")
    secondName = input("Please enter the SECOND name for your desired search. \nError will be displayed if numeric value is typed in \nInput: ")
    
    #checking if user entered values for firstName
    if firstName:
        #if non-alphabetic values are detected
        if firstName.isdigit() == True: 
            #print error message
            print("Error Code: 03. Invalid first name.")
            #back to menu
            menuSelection()
    #if value empty
    else:
        #replace value with * operator so mySql search for everything
        firstName = "*" 
    
    #same thing as above
    if secondName:
        
        if secondName.isdigit() == True:
            
            print("Error code: 04. Invalid second name.")
            sys.exit()
            
    else:
        
        secondName = "*"
    
    return firstName, secondName
            
    

def databaseOperation(countryCode, fileList):
    
    #establish connection to database
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password=PASSWORD
    )
    connection = sqlalchemy.create_engine(f'mysql+mysqlconnector://root:{PASSWORD}@localhost:3306')
    #establish a cursor to interact with the database
    mycursor = mydb.cursor()
    #create the database if it doesnt exists
    mycursor.execute("CREATE DATABASE IF NOT EXISTS COUNTRY;")
    mydb.commit()
    #execute to use the database 
    mycursor.execute("USE COUNTRY;")
    mydb.commit()
    #if the user selected to repair the full database (which means they have to wait for so long)
    if countryCode == "*":
        #loop
        for i in range(len(fileList)):
            #initiate the table name
            name = fileList[i].replace(".csv", "")
            name = name.lower()
            #the sql and its commit
            sql = f"CREATE TABLE IF NOT EXISTS `{name}` (firstName varchar(255), secondName varchar(255), Gender varchar(5), countryCode varchar(4) );"
            mycursor.execute(sql,)
            mydb.commit()
            #print a log for the success of creation
            print("System log: table created for", name)
            #read in the data
            df = pd.read_csv(f"C:\Coding Portfolio\Python\python and database\dataset\data\{fileList[i]}", header=None, dtype={0:'string', 1:'string', 2:'string', 3:'string'})
            df.columns = ["firstName", "secondName", "Gender", "countryCode"]
            #remove all the duplicate
            dfUnique = df.drop_duplicates()
            #push to table in database
            dfUnique.to_sql(name, schema='COUNTRY', con=connection, if_exists='append', index=False, chunksize=500000)
            print("Success")
    #else if the user wants to search for a country code and repair its table
    else:
        #find the name
        for i in range(len(fileList)):
    
            if countryCode == (name := fileList[i].replace(".csv", "").lower() ):
                sql = f"CREATE TABLE IF NOT EXISTS `{name}` (firstName varchar(255), secondName varchar(255), Gender varchar(5), countryCode varchar(4) );"
                mycursor.execute(sql,)
                mydb.commit()
                print("System log: table created for", name)
                df = pd.read_csv(f"C:\Coding Portfolio\Python\python and database\dataset\data\{fileList[i]}", header=None, dtype={0:'string', 1:'string', 2:'string', 3:'string'})
                df.columns = ["firstName", "secondName", "Gender", "countryCode"]
                dfUnique = df.drop_duplicates()
                dfUnique.to_sql(name, schema='COUNTRY', con=connection, if_exists='append', index=False, chunksize=500000)
                print("Success")
                
                
                
            
def menuSelection():
    
    print(tx.WELCOMETEXT, tx.CHOICE1, tx.CHOICE2, tx.CHOICE3, tx.CHOICE4, tx.CHOICE5, tx.CHOICE6, tx.CHOICE7)
    userInput = input("\nPlease enter a choice: ")   
    validation = False
        
    while validation == False:
        
        if userInput.isdigit() == False:
            print("Error, not a number")
            userInput = input("Enter: ")
        elif  int(userInput) < 1 or int(userInput) > 7:
            print("Error, out of range")
            userInput = input("Enter: ")
        else:
            validation = True
            
    return int(userInput)


def userGuide():
    
    print(tx.USERGUIDE + tx.GUIDETEXT2 + tx.GUIDETEXT3 + tx.GUIDETEXT4)
    print("Press 7 to exit")
    userInput  = 0 
    
    while userInput != 7:
        
        userInput = str(input("Enter: "))
        validation = False
        
        while validation == False:
            
            if userInput.isdigit() == False:
                print("Error, not a number")
                userInput = input("Enter: ")
            elif  int(userInput) < 1 or int(userInput) > 8:
                print("Error, out of range")
                userInput = input("Enter: ")
            else:
                validation = True
                 
        
        userInput = int(userInput)

        
        listOfGuide = [tx.GENERALGUIDE, tx.COUNTRYGUIDE, tx.NAMEFINDERGUIDE, tx.USERTOOLGUIDE, tx.MANAGETOOLGUIDE, tx.REPAIRMENT]
        if 0 < userInput < 7:
            print(listOfGuide[userInput - 1], end="\n")
            print("To see your choice again, press 8")
        if userInput == 8:
            print(tx.GUIDETEXT4, end="\n")
    return 0
    
    
        
def callFunction(choice, listName, listFile):
    
    if choice == 1:
        userGuide()
    elif choice == 2:
        codeFunction(listName)
    
            
def main():
    listFile, listName = initiate()
    menuNum = 0
    while menuNum != 7:
        menuNum = menuSelection()
        callFunction(menuNum, listName, listFile)
        
    print("Thank you for using the record finder!")
        
    
main()