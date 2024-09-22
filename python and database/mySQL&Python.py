import os
import sys
import mysql.connector
import ignore
import pandas as pd
import sqlalchemy
import text as tx
PASSWORD = ignore.password



mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password=PASSWORD
    )
connection = sqlalchemy.create_engine(f'mysql+mysqlconnector://root:{PASSWORD}@localhost:3306')
#establish a cursor to interact with the database
mycursor = mydb.cursor(buffered=True)
#create the database if it doesnt exists
mycursor.execute("CREATE DATABASE IF NOT EXISTS COUNTRY;")
mydb.commit()
#execute to use the database 
mycursor.execute("USE COUNTRY;")
mydb.commit()


logIn = False
userName = ""
passID = ""
    
def bold(type): 
    sys.stdout.write("\033[1m" + type + "\033[0m") 


def initiate():

    #Initiate path to the database
    path = ignore.path
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


def nameFinderOperation(quickSearch, targetFirstName, targetSecondName, countryCode, fileName):
    
    try:  
        #initiate a list where it will store all the country code that doesnt contain any non-alphabetical name
        quickSearchFileList = []
        
        for i in range(len(fileName)):
            
            try:
                #select name that has non-alphabetical letter
                sql = f"SELECT * FROM `{fileName[i].lower()}` WHERE firstName REGEXP '^[^abcdefghijklmnopqrstuwvzx]*$' OR secondName REGEXP  '^[^abcdefghijklmnopqrstuwvzx]*$'LIMIT 1;"
                mycursor.execute(sql)
                #fetch the data
                data = mycursor.fetchone()
                #if data doesn't exists
                if not data:
                    #append it to the list
                    quickSearchFileList.append(fileName[i].lower())
            #if an error occured
            except:
                #print error code
                print("Error, the initiation of the quick search list has encountered a problem")
                return 1
        #establish a string which we will use for our SQL statement    
        addon = "WHERE "
        #if the user inputted a first name
        if targetFirstName:
            #concatonate it t"o the string
            addon = addon + f"firstName = '{targetFirstName}' "
        #if the user inputted a second name    
        elif targetSecondName:
            #concatonate it to the string
            addon = addon + f"secondName = '{targetSecondName}' "
        elif targetFirstName and targetSecondName:
            addon = addon + f"firstName = '{targetFirstName}' AND secondName = '{targetSecondName}'"
        addon = addon + "LIMIT 1;"
        #if the user inputted a country code
        if countryCode:
            
            try:
                
                countryCode.lower()
                #complete our sql statement         
                sql = f"SELECT * FROM `{countryCode}` " + addon
                mycursor.execute(sql)
                #fetch the data
                data = mycursor.fetchall()
                #if data exists
                if data:
                    #return true
                    return True
                #if there isn't any data
                else:
                    #return false
                    return False
            #if there is an error    
            except:
                #print error message
                print("Error, there has been a problem while trying to search for a name with a specific country code.")
                return 

            
        #if there isn't a country code inputted
        else:
        
            #declare a list which will store all the table that contains this name
            countryCodeExists = []
            #if the user has asked for a quick search
            if quickSearch.lower() == "y":

                try:
                    #loop through all the table
                    for i in range(len(quickSearchFileList)):
                        #complete the sql statement
                        sql = f"SELECT * FROM `{quickSearchFileList[i].lower()}` " + addon
                        mycursor.execute(sql)
                        #fetch the data
                        data = mycursor.fetchone()
                        #if the data exists
                        if data:
                            # append the current country code to the list
                            countryCodeExists.append(quickSearchFileList[i])
                    #return the list    
                    return quickSearchFileList
                #if an error occured
                except:
                    #display the error messsage
                    print("Error, problem occured while trying to do a quick search")
                    return 1
                
            #if quicksearch is off    
            if quickSearch.lower() == 'n':
                
                try:
                    #loop through every single table
                    for i in range(len(fileName)):
                        #complete sql statement
                        sql = f"SELECT * FROM `{fileName[i].lower()}` " + addon
                        mycursor.execute(sql) 
                        #append data
                        data = mycursor.fetchone()
                        #if there is data
                        if data:
                            #append it to the list
                            countryCodeExists.append(fileName[i])
                        print(i / len(fileName) * 100 , "%")
                    #return the list
                    return countryCodeExists
                #if error: display error message
                except:
                    print("Error, problem occured while trying to do a full search")
                    return 1
                                   

    except:
        
        print("Error, there has been some kind of bug within the search operation.")
        return 1
      
        
def repairmentOperation(countryCode, fileList):
    #if the user selected to repair the full database (which means they have to wait for so long)
    
    if countryCode == "*":
        #loop
        for i in range(len(fileList)):
            #initiate the table name
            name = fileList[i]
            name = name.lower()
            #the sql and its commit
            deleteSql = f"DROP TABLE IF EXISTS {name}"
            mycursor.execute(deleteSql,)
            mydb.commit()
            sql = f"CREATE TABLE IF NOT EXISTS `{name}` (firstName varchar(255), secondName varchar(255), Gender varchar(5), countryCode varchar(4) );"
            mycursor.execute(sql,)
            mydb.commit()
            #print a log for the success of creation
            print("System log: table created for", name)
            #read in the data
            df = pd.read_csv(f"{ignore.path}\{fileList[i]}", header=None, dtype={0:'string', 1:'string', 2:'string', 3:'string'})
            df.columns = ["firstName", "secondName", "Gender", "countryCode"]
            #remove all the duplicate
            dfUnique = df.drop_duplicates()
            #push to table in database
            dfUnique.to_sql(name, schema='COUNTRY', con=connection, if_exists='append', index=False, chunksize=500000)
            print(i / len(fileList) * 100 , "%")
            
        print("Success")
        return 0
    #else if the user wants to search for a country code and repair its table
    else:
        #find the name
        
    
        if countryCode in fileList:
            
            countryCode = countryCode.lower()
            deleteSql = f"DROP TABLE IF EXISTS {countryCode}"
            mycursor.execute(deleteSql,)
            mydb.commit()
            sql = f"CREATE TABLE IF NOT EXISTS `{countryCode}` (firstName varchar(255), secondName varchar(255), Gender varchar(5), countryCode varchar(4) );"
            mycursor.execute(sql,)
            mydb.commit()
            print("System log: table created for", name)
            df = pd.read_csv(f"{ignore.path}\{countryCode}", header=None, dtype={0:'string', 1:'string', 2:'string', 3:'string'})
            df.columns = ["firstName", "secondName", "Gender", "countryCode"]
            dfUnique = df.drop_duplicates()
            dfUnique.to_sql(name, schema='COUNTRY', con=connection, if_exists='append', index=False, chunksize=500000)
            print("Success")
            
            return 0
            
        else:
            
            print("Error, could not find the table to repair, make sure you have typed in the right country code.")
            return 0
                

def askName():

    
    firstName = ""
    secondName = ""
    print("Please enter the corrosponding number for your choice:\n1. First name only\n2. Second name only\n3. Both name")
    userInput = input("Enter: ")
    
    validation = False
    while validation == False:
        
        if userInput.isdigit() == False:
            print("Error please enter a number with a digit")
        elif 3 < int(userInput) < 1:
            print("Error please enter between 1 and 3")
        else:
            
            break
        
        userInput = input("Enter: ")
    
    userInput = int(userInput)
    
    match userInput:
        
        case 1:
        
            firstName = input("Please enter a first name (type quit to leave): ")
            firstName = validationNameFinder(firstName)
        
        case 2:
        
            secondName = input("Please enter a second name (type quit to leave): ")
            secondName = validationNameFinder(secondName)

        case 3:
        
            firstName = input("Please enter a first name (type quit to leave): ")
            firstName = validationNameFinder(firstName)
            
            secondName = input("Please enter a second name (type quit to leave): ")
            secondName = validationNameFinder(secondName)
        
        case _:
            print("wtf")
            
    
    return firstName, secondName
        
            
def nameFinder(listName):
    
    #declare variable which will be used to store the user input for the country code
    code = ""
    quickSearch = "n"
    
    bold("Welcome to the name finder tool\n")
    #ask for name
    firstName, secondName = askName()
    
    if firstName != "quit" or secondName != "quit":
        
        code = input("Please enter the country code to give a more precise search (if left blank, will search through every table): ")
        
        if code:
            
            state = nameFinderOperation(quickSearch, firstName, secondName, code, listName)
            
            if state == True:
                
                print("Name is found")
                return 0
            else:
                
                print("Name not found")
                
        else:
            
            print("We have detected that a country code hasn't been entered, would you like to enable quick search? (only works with english names)")
            
            quickSearch = input("Please enter Y or N: ")
            
            arrayOfCountryCode = nameFinderOperation(quickSearch, firstName, secondName, code, listName)
            
            if arrayOfCountryCode:
                
                print("The country code which the name was found:\n====================================\n")
                for i in range(len(arrayOfCountryCode)):
                    
                    print(arrayOfCountryCode[i], end=", ")
                print("\n=======================================\n")
                return 0
            else:
                print("Not found in any table")
      
        
def validationNameFinder(name):
    
    while len(name) == 0 and name != "quit":
        print("Error! Please enter a name")
        name = input("Enter (type quit to leave): ")  
        
    return name     
             
            
def menuSelection():
    
    print("\n"+tx.WELCOMETEXT, tx.CHOICE1, tx.CHOICE2, tx.CHOICE3, tx.CHOICE4, tx.CHOICE5, tx.CHOICE6, tx.CHOICE7)
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
    

def userTool(listName):
    
    if logIn == False:
        print("Error, please log in before accessing this tool")
        return 0

    else:
        
        print(tx.TOOL)
        userInput = input("\nPlease enter a choice: ")   
        validation = False
            
        while validation == False:
            
            if userInput.isdigit() == False:
                print("Error, not a number")
                userInput = input("Enter: ")
            elif  int(userInput) < 1 or int(userInput) > 5:
                print("Error, out of range")
                userInput = input("Enter: ")
            else:
                validation = True
        
        while userInput != 5:
            
            if userInput == 1:
                deleteRecord(listName)
                
            if userInput == 2:
                deleteTable(listName)
            
            if userInput == 3:
                addRecord(listName)
            
            if userInput == 4:
                alterRecord(listName)
             
                
def deleteRecord(listName):
    
    print("To delete a record, please enter the name and the country code of the desired record")
    firstName, secondName = askName()
    if firstName != "quit" and secondName != "quit":
        code = input("Please enter a country code, (type quit to leave): ")
        while ( code not in listName ) and code != "quit":
            print("Error, country code not found")
            code = input("Please enter a country code, (type quit to leave): ")
        
        if code == "quit":
            return 0
        else:
            
            try:
                #establish a string which we will use for our SQL statement    
                addon = ""
                #if the user inputted a first name
                if firstName:
                    #concatonate it to the string
                    addon = f"WHERE firstName = '{firstName}' "
                #if the user inputted a second name    
                if secondName:
                    #concatonate it to the string
                    addon = addon + f"AND secondName = '{secondName}' "
                
                addon = addon + ";"
                
                sql = f"DELETE FROM `{code}` " + addon
                mycursor.execute(sql)
                mydb.commit()
                print("Record deleted")
                return 0
            
            except:
                
                print("There has been an error: there is a potential that the record does not exists.")
                return 0
    else:
        return 0
  
     
def deleteTable(listName):
    
    print("Welcome to the table deleter: please enter the country code of which you want the table deleted for.")
    code = input("Please enter a country code, (type quit to leave): ")
    while ( code not in listName ) and code != "quit":
        print("Error, country code not found")
        code = input("Please enter a country code, (type quit to leave): ")
    
    if code == "quit":
        return 0
    else:
        sql = f"DROP TABLE IF EXISTS {code};"
        mycursor.execute(sql)
        mydb.commit()
        print("Table dropped")
        return 0


def addRecord(listName):
    
    print("Welcome to the record adder, please specify the data for importing and the table to import to")
    firstName, secondName = askName()
    
    while len(firstName) == 0 or len(secondName) == 0:
        print("For this function to work you will need both names")
        firstName, secondName = askName()
    
    code = input("Please enter a country code, (type quit to leave): ")
    
    if firstName != "quit" and secondName !="quit":
        
        while ( code not in listName ) and code != "quit":
            
            print("Error, country code not found")
            code = input("Please enter a country code, (type quit to leave): ")
            
        if code == "quit":
            
            return 0
        
        else:
            
            gender = input("Please enter a gender (F or M): ")
            
            while gender != "F" and gender != "M":
                gender = input("Please enter a gender (F or M): ")
            
            try:
                
                sql = f"INSERT INTO `{code}` (firstName, secondName, gender, countryCode ) VALUES (%s, %s)"
                val = (firstName,secondName, gender, code)
                
                mycursor.execute(sql, val)
                mydb.commit()
                
                print("Success")
                return 0
            
            except:
                
                print("Error while trying to insert record")
                return 1


            
    else:
        return 0

    
def alterRecord(listName):
    
    print("Welcome to the record alternator, to use this, please specify either one of the name WITH the country code of the record you want to change.")
    firstName, secondName = askName()
    
    code = input("Please enter a country code, (type quit to leave): ")
    
    if firstName != "quit" and secondName !="quit":
        
        while ( code not in listName ) and code != "quit":
            
            print("Error, country code not found")
            code = input("Please enter a country code, (type quit to leave): ")
        
        print("Now, we will ask you the NEW data you want to change into, to not alter, leave it blank")
        
        newFirstName = input("first name: ")
        newSecondName = input("second name: ")
        newGender = input("gender: ")
        try:
            addon = "WHERE "
            #if the user inputted a first name
            if firstName:
                #concatonate it to the string
                addon = f"firstName = '{firstName}';"
            #if the user inputted a second name    
            elif secondName:
                #concatonate it to the string
                addon = addon + f"secondName = '{secondName}';"
            elif firstName and secondName:
                
                addon = addon + f"firstName = '{firstName}' AND secondName = '{secondName}';"
            
            
            if newFirstName:
                
                sql = f"UPDATE `{code}` SET firstName = {newFirstName} " + addon
                mycursor.execute(sql)
                mydb.commit()
                
            if secondName:
                
                sql = f"UPDATE `{code}` SET secondName = {newSecondName} " + addon
                mycursor.execute(sql)
                mydb.commit()
            
            if newGender:
                
                sql = f"UPDATE `{code}` SET gender = {newGender} " + addon
                mycursor.execute(sql)
                mydb.commit()
                
            print("Task done")
            return 0
        
        except:
            print("Man, an error has occcured while trying to update data")
            return 0
             

def manageUser():
    
    while True:
        
        if logIn == False:
            print("\nYou are not currently logged on.\n")
        elif logIn == True:
            print("\nYou are logged in as:", userName)
        
        print(" 1.Log In\n 2.Sign up\n 3.Change Username or password\n 4.Log out\n 5.Quit\n")
        try:
            userInput = int(input("Please enter a number between 1-5: "))
            while 1 < userInput > 6:
                print("Error, enter between 1-5")
                userInput = int(input("Please enter a number between 1-5: "))
        except ValueError:
            print("Error, not a number")
            return 0
        
        mycursor.execute("USE COUNTRY")
        mydb.commit()
              
        match userInput:
            
            
            case 1:
                logInFunc()
            case 2:
                signUp()
            case 3:
                changeUser()
            case 4:
                logOut()
            case 5:
                return 0
            case 6:
                print("EH? HOW? (you found an easteregg!)")
            case _:
                print("BREH")


def logInFunc():
    
    global logIn 
    global userName
    global passID
    
    userID = input("Username: ")
    password = input("Password: ")
    
    sql = f"SELECT * FROM USER WHERE BINARY userID = '{userID}' AND BINARY password = '{password}';"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    if data:
        print("Logged on")
        logIn = True
        userName = data[0][0]
        passID = data[0][1]
        return 0
    else:
        print("Error: User not found.\n")
        return 0
    

def signUp():
    
    print("Welcome to the sign up page.")
    print("To quit, type quit.\n")
    
    userID = input("Please enter a username: ")
    
    if userID != "quit":
        
        password = input("Please enter a password: ")
        
        sql = f"SELECT * FROM USER WHERE BINARY userID = '{userID}';"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        if data:
            print("Error, userID exists")
            return 0
        else:
            try:
                sql = f"INSERT INTO USER VALUES('{userID}','{password}');"
                mycursor.execute(sql)
                mydb.commit()
                print("Successfully created user.")
                return 0
            except:
                print("There has been some error while trying to create the user.")
                return 0
    
    
def logOut():
    
    global userName
    global passID
    global logIn
    
    if logIn == False:
        print("Error, you are not logged on")
        return 0
    elif logIn == True:
        
        userInput = input("Do you wish to sign out?\nEnter (Y \ N): ")
        
        while userInput != "Y" and userInput != "N":
            
            print("Please only enter Y or N")
            userInput = input("Do you wish to sign out?\nEnter (Y \ N): ")
        
        match userInput:
            
            case "Y":
                logIn = False
                userName = ""
                passID = ""
                return 0
            case "N":
                return 0        
        
    
def changeUser():
    
    global logIn
    global userName
    global passID
    
    while True:
        if logIn == False:
            print("You are not logged on\n")
            return 0
        else:
            print("\n 1. Change username\n 2. Change password\n 3. Quit")
            userInput = input("Enter: ")
            
        match userInput:
            
            case 1:
                
                newUsername = input("Please enter your new username: ")
                
                while validation == False:
                    print("Are you sure this is the correct username? ", newUsername)
                    validInput = input("Enter (Y \ N): ")
                    
                    if validInput == "N":
                        newUsername = input("Please enter your new username: ")
                        
                    elif validInput == "Y":
                        validation = True
                
                
                sql = f"SELECT * FROM USER WHERE BINARY userID = '{newUsername}';"
                mycursor.execute(sql)
                data = mycursor.fetchall()
                if data:
                    print("Error, userID exists")
                    return 0
                
                else:
                    
                    sql = f"UPDATE user SET userID = '{newUsername}' WHERE userID = '{userName}' AND password = '{passID}';"
                    mycursor.execute(sql)
                    mydb.commit()
                    print("Success")
                    userName == newUsername
                    return 0
                                                  
            case 2:
                
                newPassword = input("Please enter your new password: ")
                confirmPassword = input("Please confirm your new password: ")
                
                while newPassword != confirmPassword:
                    
                    print("Error, the new password and confirmed password is incorrect")
                    newPassword = input("Please enter your new password: ")
                    confirmPassword = input("Please confirm your new password: ")
                
                
                sql = f"UPDATE user SET password = '{newPassword}' WHERE userID = '{userName}' AND password = '{passID}';"
                mycursor.execute(sql)
                mydb.commit()
                print("Success")
                passID = newPassword
                return 0
            
            case 3:
                return 0
            case _:
                
                print("Error, not a valid choice")
        

def repairChoice(listName):
    
    while True:
        
        print("Welcome\n 1.Repair specific table\n 2.Repair whole database (NOT RECOMMENDED)")
        userInput = input("Enter: ")
        
        match userInput:
            
            case 1:
                userInput = input("Please enter a country code: ")              
                repairmentOperation(userInput, listName)
                
                return 0 
            case 2:
                print("ARE YOU SURE YOU WANT TO DO THIS DAWG, IT TAKES ABOUT 1 HOUR TO FIX")
                
                userInput = input("TYPE 'YES' TO PROCEED: ")
                if userInput != "YES":
                    return 0
                else:
                    countryCode = "*"
                    repairmentOperation(countryCode, listName)
                    return 0
            case _:
                print("Invalid input")
                
        
def userGuide():
    
    #initiate the list of guide
    listOfGuide = [tx.GENERALGUIDE, tx.COUNTRYGUIDE, tx.NAMEFINDERGUIDE, tx.USERTOOLGUIDE, tx.MANAGETOOLGUIDE, tx.REPAIRMENT]
    #print the general text
    print(tx.USERGUIDE + tx.GUIDETEXT2 + tx.GUIDETEXT3 + tx.GUIDETEXT4)
    print("Press 7 to exit")
    userInput  = 0 
    
    while userInput != 7:
        #allow user to input a choice
        userInput = str(input("Enter: "))
        validation = False
        #validation
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
        
        if 0 < userInput < 7:
            print(listOfGuide[userInput - 1], end="\n")
            print("To see your choice again, press 8")
        if userInput == 8:
            print(tx.GUIDETEXT4, end="\n")
            
    return 0
    
        
def callFunction(choice, listName, listFile):
    
    
    match choice:
        
        case 1:
            userGuide()
        case 2:
            codeFunction(listName)
        
        case 3:
            nameFinder(listName)
        case 4:
            userTool(listName)
        case 5:
            manageUser()
        case 6:
            repairChoice(listName)
            
            
def main():
    #initiate the program by loading the csv file name
    listFile, listName = initiate()
    menuNum = 0
    #while the user doesn't want to quit
    while menuNum != 7:
        #allow user to select an option
        menuNum = menuSelection()
        #use the relative function the user typed in
        callFunction(menuNum, listName, listFile)
        
    print("Thank you for using the record finder!")
        
    
main()