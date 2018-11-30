import sqlite3
import pandas as pd
import scipy.stats
import seaborn
import matplotlib.pyplot as plt
from pylab import savefig
import numpy as np

conn = sqlite3.connect('LeVinEmployee.db')

# boolean for loops
match = False


# Function to allow user to login by querying the selected data in the database
def retrieve(email, password):

    cur = conn.cursor()
    try:

        cur.execute("SELECT * FROM Employee WHERE (Email = '" + email.strip() + "') AND (Password = '" + password.strip() + "')")
        results = cur.fetchall() 

        # if statement checks if 'results' is false, indicating it's empty 
        if results:
            print ("\nLogged on Successfully!\n") 
            #print (results)
            return (results)

    except:

        print("\nAn error occured!\n")

#Main menu function 
def Menu():
    
    while True:
        Question = input ("Would you like to:\
                          \n\n 1) Register a new employee? \n \
                          \n 2) Test associations for red & white wines? \n \
        \n 3) Test user value? \n \
        \n 4) Box Plot and Correlation of Wine Characteristics in both wine types? \n \
        \n 5) Pair Plots of Wine Characteristics? \n \
        \n 6) Quit \n \
        \n Please select '1', '2', '3', '4', '5', or  '6': \n")
        if (Question == "1"):
            empID = input ("To register a new employee, first enter his/ her EmployeeID: ")
          # Parameters passsed as arguments to check if employee ID exists 
            PKCheck(empID)
            break
        if (Question == "2"): 
            WineCheck()
            break
        if (Question == "3"):
            WineCheck2()
            break
        if (Question == "4"):
            ChooseWine()
            break
        if (Question == "5"):
            choose()
            break
        if (Question == "6"):
            print("\nThank you, come again!\n")
            break

# Function to check if Employee ID is taken       
def PKCheck(StripEmpID):

    with conn:
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT COUNT (*) FROM Employee WHERE (EmployeeID = '" + StripEmpID + "')")
            results = cur.fetchone()

            while results[0] == 1:
                empID = input("That EmployeeID is already in use.\t Please enter a different one or type 'q' to quit: ")           

                # if user enter 'q', then the program will quit. 
                if (empID == 'q'):
                    print ("\nThank you, come again!\n")
                    raise SystemExit
                    
                StripEmpID = empID.strip()
                cur.execute("SELECT COUNT (*) FROM Employee WHERE (EmployeeID = '"+ StripEmpID + "')")
                results = cur.fetchone()

            # Print statement if ID is not taken
            print("\nEmployeeID, " + StripEmpID + ", is accepted")         

            # Call on function to add entry into database
            addEntry(StripEmpID)
       

        except sqlite3.Error as e:
            print(e)


# Function to create new database entry with the user provided values        
def addEntry (ID):

    with conn:
        cur = conn.cursor()

        try:
            
            email = input ("Enter his/ her email: ")
            password = input ("Enter his/her password: ")
            firstname = input ("Enter his/her first name: ")            
            lastname = input ("Enter his/her last name: ")            
            streetaddress = input ("Enter his/her street address: ")            
            city = input ("Enter City: ")            
            state = input ("Enter state: ")            
            zipcode = input ("Enter zipcode: ")


            cur.execute('''INSERT INTO Employee (EmployeeID, FirstName, LastName,
                                                 StreetAddress, City, State, Zipcode, Email, Password)
                        VALUES (?, ?, ?, ?,?, ?, ?, ?, ?)''', (ID, firstname, lastname, streetaddress, city, state, zipcode, email, password))

            cur.execute("SELECT * FROM Employee WHERE (EmployeeID = '" + ID + "')")
            results3 = cur.fetchall()    

            if (results3):
                print ("\nUser added sucessfully!\n")
            
            #While loop provide users the option to return to main menu or quit
            while True:
                Return = input ("Would you like to return to the main menu? \
                               \n\n 1) Yes \n \
                \n 2) No, Quit \n \
                \n Please select '1', or '2': \n")
                if (Return == "1"):
                    Menu()
                    break
                if (Return == "2"):
                    print("\nThank you, come again!\n")
                    break

        except:
            print ("\nFailed to add values!\n")
            

#Function to choose test association or quit
def WineCheck():

    #While loop only breaks if user choose quit, or have a valid response
    while True:
        WineType = input("Would you like to test the association for:\
                             \n\n 1) Red wine \n \
            \n 2) White wine \n \
                \n 3) Quit \n \
            \n please select '1', '2', or '3': \n ")
        quickquit = False
        if (WineType == "3"):
            print("\nThank you, come again!\n")
            quickquit = True
            break
        if (WineType == "1" or WineType == "2"):
            break

    #Assign variable that matches the database
    if (WineType == "1"):
        WineType = "red"
                
    if (WineType == "2"):
        WineType = "white"

    #While loop only breaks if user choose quit, or have a valid response            
    while True:
        if quickquit == True:
            break
        if quickquit == False:
            Acheck = input ("You can check test the following associations for red wines and for white wines:\
                       \n\n 1) Volatile acidity and wine quality \n \
                \n 2) Fixed acidity and wine quality \n \
                \n 3) Alcohol percent and wine quality \n \
                \n 4) Residual sugar and wine quality \n \
                \n 5) Quit \n \
                \n please select '1', '2', '3','4', or '5': \n")
            if(Acheck == "5"):
                print("\nThank you, come again!\n")
                quickquit = True
                break
            if (Acheck == "1" or Acheck == "2" or Acheck == "3" or Acheck == "4"):
            
                #Assign variable that matches the database
                if (Acheck == "1"):
                    Acheck = "volatile acidity"
                    break
                            
                if (Acheck == "2"):
                    Acheck = "fixed acidity"
                    break
            
                if (Acheck == "3"):
                    Acheck = "alcohol"
                    break
                        
                if (Acheck == "4"):
                    Acheck = "residual sugar"   
                    break
    
    if quickquit == False:            
        WineAssociate(WineType, Acheck)

    
#Function that tests wine association & graphs            
def WineAssociate(WineType, Acheck):
    try:
        WineCharX = "quality"
        WineCharY = Acheck
        allWines = pd.read_csv('winequality-both.csv')
        UserWineType = allWines.loc[allWines['type']== WineType,:]
        
        getCorr = scipy.stats.pearsonr(UserWineType[WineCharX], UserWineType[WineCharY])
        correlation = str(getCorr[0])
        pValue = str(getCorr[1])
        
       
        print("For " + WineType + " wine, the correlation between " + WineCharX + " and " + WineCharY + " is: " + correlation)
        print ("With p value of: " + pValue)
        
        seaborn.lmplot(x=WineCharX, y=WineCharY, data=UserWineType)
        
        plt.xlabel(WineCharX)
        plt.ylabel(WineCharY)
        
        plt.title(WineType + " Wine: " + WineCharX + " X " + WineCharY)
        
        #show graph before the while loop
        plt.show()
       
        #While loop to check more associations, quit and show results, or return to main menu for more options
        while True:
            Rerun = input ("Would you like to test another association? \
                           \n\n 1) Yes \n \
            \n 2) No, Quit. \n \
            \n 3) Main Menu \n \
            \n Please select '1', '2', or '3': \n")
            if (Rerun == "1"):
                WineCheck()
                break
            if (Rerun == "2"):
                print("\nThank you, come again!\n")
                break
            if (Rerun == "3"):
                Menu()
                break
              
    except(KeyError) as e:
        print ("Please check the spelling of the wine characteristics you want to test")


#Function to ask for wine type & characteristics to test on
def WineCheck2():
#While loop only breaks if user choose quit, or have a valid response
    while True:
        WineType = input("Would you like to test the association for:\
                             \n\n 1) Red wine or \n \
            \n 2) White wine? \n \
                \n 3) Quit \n \
            \n please select '1', '2', or '3': \n ")
        quickquit = False
        if (WineType == "3"):
            print("\nThank you, come again!\n")
            quickquit = True
            break
        if (WineType == "1" or WineType == "2"):
            break

    #Assign variable that matches the database
    if (WineType == "1"):
        WineType = "red"
                
    if (WineType == "2"):
        WineType = "white"

    #While loop only breaks if user choose quit, or have a valid response            
    while True:
        if quickquit == True:
            break
        if quickquit == False:
            Acheck = input ("You can check test the following associations for red wines and for white wines:\
                       \n\n 1) Volatile acidity and wine quality \n \
                \n 2) Fixed acidity and wine quality \n \
                \n 3) Alcohol percent and wine quality \n \
                \n 4) Residual sugar and wine quality \n  \
                \n 5) Quit \n \
                \n please select '1', '2', '3','4', or '5': \n")
            if(Acheck == "5"):
                print("\nThank you, come again!\n")
                quickquit = True
                break
            if (Acheck == "1" or Acheck == "2" or Acheck == "3" or Acheck == "4"):
            
                #Assign variable that matches the database
                if (Acheck == "1"):
                    Acheck = "volatile acidity"
                    break
                            
                if (Acheck == "2"):
                    Acheck = "fixed acidity"
                    break
            
                if (Acheck == "3"):
                    Acheck = "alcohol"
                    break
                        
                if (Acheck == "4"):
                    Acheck = "residual sugar"   
                    break
            
            
    
    if quickquit == False:            
        UserValue(WineType, Acheck)


#Function for user-provided wine characteristic value
def UserValue(WineType, Acheck):
    
    allWines = pd.read_csv('winequality-both.csv')
    #collects either red or white wine data
    UserWineType = allWines.loc[allWines['type']== WineType,:]
    #rename headers to allow easy retrieval of min and max values
    df = UserWineType.rename(columns = {'volatile acidity':'volatileAcidity', \
                                            'fixed acidity':'fixedAcidity', \
                                            'citric acid':'citricAcid', \
                                            'residual sugar':'residualSugar', \
                                            'free sulfur dioxide':'freeSulfurDioxide', \
                                            'total sulfur dioxide':'totalSulfurDioxide'} )    

    try:
        if (Acheck == "volatile acidity"):
            minimum = float(df.volatileAcidity.min())
            maximum = float(df.volatileAcidity.max())
            print ("\nEnter a value from range:", minimum, " to ", maximum)
            validRange = True
            while validRange:
                WineValue = input("Volatile acidity value: ")
                try:
                    WineValue = float(WineValue)
                    if (WineValue < minimum or WineValue > maximum):
                        print ("You must enter a value within the range. Try again: ")
                    else:
                        break
                except ValueError:
                    print ("Please enter numeric values only!\n")
                
        if (Acheck == "fixed acidity"):
            minimum = float(df.fixedAcidity.min())
            maximum = float(df.fixedAcidity.max())
            print ("\nEnter a value from range:", minimum, " to ", maximum)
            validRange = True
            while validRange:
                WineValue = input("fixed acidity value: ")
                try:
                    WineValue = float(WineValue)
                    if (WineValue < minimum or WineValue > maximum):
                        print ("You must enter a value within the range. Try again: ")
                    else:
                        break
                except ValueError:
                    print ("Please enter numeric values only!\n")
            
        if (Acheck == "alcohol"):
            minimum = float(df.alcohol.min())
            maximum = float(df.alcohol.max())
            print ("\nEnter a value from range:", minimum, " to ", maximum)
            validRange = True
            while validRange:
                WineValue = input("alcohol value: ")
                try:
                    WineValue = float(WineValue)
                    if (WineValue < minimum or WineValue > maximum):
                        print ("You must enter a value within the range. Try again: ")
                    else:
                        break
                except ValueError:
                    print ("Please enter numeric values only!\n")
            
        if (Acheck == "residual sugar"):
            minimum = float(df.residualSugar.min())
            maximum = float(df.residualSugar.max())
            print ("\nEnter a value from range:", minimum, " to ", maximum)
            validRange = True
            while validRange:
                WineValue = input("sugar value: ")
                try:
                    WineValue = float(WineValue)
                    if (WineValue < minimum or WineValue > maximum):
                        print ("You must enter a value within the range. Try again: ")
                    else:
                        break
                except ValueError:
                    print ("Please enter numeric values only!\n")
                
    except (TypeError, ValueError):
        print("error")
            
    TestingWine(WineType, Acheck, WineValue)              
  

#Function to show histogram with the given values
def TestingWine (WineType, Acheck, WineValue):
    
    try:
        WineChar = Acheck
        WineCharValue = float(WineValue)
        WineChar2 = "quality"
        
        allWines = pd.read_csv('winequality-both.csv')
        UserWineType = allWines.loc[allWines['type']== WineType,:]
        
        TestChar = UserWineType.loc[UserWineType[WineChar]== WineCharValue,:]
        
        WineCharValueDataset = TestChar.loc[:, WineChar2]
        
        seaborn.distplot(WineCharValueDataset, bins=10, kde=False)
        plt.title(WineChar + " value " + str(WineCharValue) + " frequencies by " + WineChar2)
        
        plt.ylabel("Number of wines")
        
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
        plt.show()
        
        while True:
            Rerun = input ("Would you like to test again? \
                           \n\n 1) Yes \n \
            \n 2) No, Quit. \n \
            \n 3) Main Menu \n \
            \n Please select '1', '2', or '3': \n")
            if (Rerun == "1"):
                WineCheck2()
                break
            if (Rerun == "2"):
                print("\nThank you, come again!\n")
                break
            if (Rerun == "3"):
                Menu()
                break
    
    except(KeyError, ZeroDivisionError) as e:
        print(e)
        
        
#Choosing wine to show on boxplot for citric acid
def ChooseWine():
    #While loop only breaks if user choose quit, or have a valid response
    while True:
        WineType = input("Would you like to test the association for:\
                             \n\n 1) Red wine or \n \
            \n 2) White wine? \n \
                \n 3) Quit \n \
            \n please select '1', '2', or '3': \n ")
        quickquit = False
        if (WineType == "3"):
            print("\nThank you, come again!\n")
            quickquit = True
            break
        if (WineType == "1" or WineType == "2"):
            break

    #Assign variable that matches the database
    if (WineType == "1"):
        WineType = "red"
                
    if (WineType == "2"):
        WineType = "white"
    
    
    #While loop only breaks if user choose quit, or have a valid response            
    while True:
        if quickquit == True:
            break
        if quickquit == False:
            Acheck = input ("You can check test the following associations for red wines and for white wines:\
                       \n\n 1) Citric Acid \n \
                \n 2) pH \n \
                \n 3) Total sulfur dioxide \n \
                \n 4) Free sulfur dioxide \n \
                \n 5) Quit \n \
                \n please select '1', '2', '4' or '5': \n")
            if(Acheck == "5"):
                print("\nThank you, come again!\n")
                quickquit = True
                break
            if (Acheck == "1" or Acheck == "2" or Acheck == "3" or Acheck == "4"):
            
                #Assign variable that matches the database
                if (Acheck == "1"):
                    Acheck = "citric acid"
                    break
                            
                if (Acheck == "2"):
                    Acheck = "pH"
                    break
                
                if (Acheck == "3"):
                    Acheck = "total sulfur dioxide"
                    break
                
                if (Acheck == "4"):
                    Acheck = "free sulfur dioxide"
                    break
            
    if quickquit == False:            
        Boxplot(WineType, Acheck)

                
#Creating a box plot to show distribution of different wine types
def Boxplot(WineType, Acheck):
    try:
        allWines = pd.read_csv('winequality-both.csv')
        UserWineType = allWines.loc[allWines['type']== WineType,:]
        wine_data = UserWineType.groupby ('type')
        wine_data.boxplot(column = [Acheck])
        
        WineCharY = Acheck
        WineCharX = 'quality'
        
        
        getCorr = scipy.stats.pearsonr(UserWineType[WineCharX], UserWineType[WineCharY])
        correlation = str(getCorr[0])
               
        print("For " + WineType + " wine, the correlation between " + WineCharX + " and " + WineCharY + " is: " + correlation)
        
        plt.show()
        
        while True:
            Rerun = input ("Would you like to test again? \
                           \n\n 1) Yes \n \
            \n 2) No, Quit. \n \
            \n 3) Main Menu \n \
            \n Please select '1', '2', or '3': \n")
            if (Rerun == "1"):
                ChooseWine()
                break
            if (Rerun == "2"):
                print("\nThank you, come again!\n")
                break
            if (Rerun == "3"):
                Menu()
                break

    except(KeyError) as e:
        print (e)
        
def choose():
#While loop only breaks if user choose quit, or have a valid response
    while True:
        choice1 = input("Choose the first characteristic for the pair plot:\
                             \n\n 1) chlorides or \n \
                        \n 2) sulphates? \n \
                        \n 3) density? \n \
                \n 4) Quit \n \
            \n please select '1', '2', '3', or '4': \n ")
        quickquit = False
        if (choice1 == "4"):
            print("\nThank you, come again!\n")
            quickquit = True
            break
        if (choice1 == "1" or choice1 == "2" or choice1== "3"):
            break

    #Assign variable that matches the database
    if (choice1 == "1"):
        choice1 = "chlorides"
                
    if (choice1 == "2"):
        choice1 = "sulphates"
    
    if (choice1 == "3"):
        choice1 = "density"
    
    
    #While loop only breaks if user choose quit, or have a valid response            
    while True:
        if quickquit == True:
            break
        if quickquit == False:
            choice2 = input ("Choose the second characteristic for the pair plot:\
                       \n\n 1) density \n \
                \n 2) volatile acidity \n \
                \n 3) citric acid \n \
                \n 4) Quit \n \
                \n please select '1', '2', '3' or '4': \n")
            if(choice2 == "4"):
                print("\nThank you, come again!\n")
                quickquit = True
                break
            if (choice2 == "1" or choice2 == "2" or choice2 == "3"):
            
                #Assign variable that matches the database
                if (choice2 == "1"):
                    choice2 = "density"
                    break
                            
                if (choice2 == "2"):
                    choice2 = "volatile_acidity"
                    break
                
                if (choice2 == "3"):
                    choice2 = "citric_acid"
                    break
            
    if quickquit == False:            
        histogram(choice1, choice2)
    

def histogram(choice1, choice2):
    try:
        wine = pd.read_csv('winequality-both.csv', sep=',', header=0)
        wine.columns = wine.columns.str.replace(' ', '_')
        
        reds_sample = (wine.loc[wine['type']=='red', :])
        whites_sample = (wine.loc[wine['type']=='white', :])
        wine_sample = pd.concat([reds_sample, whites_sample])
        wine['in_sample'] = np.where(wine.index.isin(wine_sample.index), 1.,0.)
        # Look at relationship between pairs of variables
        seaborn.set_style("dark")
        g = seaborn.pairplot(wine_sample, kind='reg', plot_kws={"ci": False,\
        "x_jitter": 0.25, "y_jitter": 0.25}, hue='type', diag_kind='hist',\
        diag_kws={"bins": 10, "alpha": 1.0}, palette=dict(red="red", white="orange"),\
        markers=["o", "s"], vars=[choice1, choice2, 'quality'])
        print(g)
        plt.suptitle('Histograms and Scatter Plots of Quality ' + choice1 + ' and ' + choice2 , \
                     fontsize=14, horizontalalignment='center', verticalalignment='top',\
        x=0.5, y=0.999)
        plt.show()
        
        while True:
            Rerun = input ("Would you like to test again? \
                           \n\n 1) Yes \n \
            \n 2) No, Quit. \n \
            \n 3) Main Menu \n \
            \n Please select '1', '2', or '3': \n")
            if (Rerun == "2"):
                print("\nThank you, come again!\n")
                break
            if (Rerun == "3"):
                Menu()
                break
            if (Rerun == "1"):
                choose()
                break
        
    except KeyError as e:
        print(e)
        
             
# While-loop will continue unless query finds a match or if the user decides not to proceed
while (match == False): 

    # Allow user to enter credentials to login in order to modify database
    userEmail = input("Please enter employee's email: ")
    userPass = input("Please enter employee's password: ")
           
    # Calls on 'retrieve' function and stores a boolean, True if found, False if not
    info = retrieve(userEmail, userPass)    

    # control flow / exception handling 
    if info:
        Menu()                            
        match = True

    elif not info:
        print ("\nThe information you entered is incorrect or there wasn't a match.")
        
        # Control flow. Loop will continue for as long as answer1 is False
        answer1 = False
        while (answer1 == False):
            
            again = input("Would you like to try again? \n \
                          \n 1) No, Quit \n \
                          \n 2) Yes \n \
                          \n Please select either '1' or '2' ")

            if (again == "1"):
                print ("\nThank you, come again!\n")
                answer1 = True
                match = True
            
            elif (again == "2"):
                match == False
                break
            
            else:
                print ("\nYou need to either enter '1' for Yes, or '2' for No")
                
            