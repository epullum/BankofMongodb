import pymongo as py
from tkinter import *
import random



#Class is used to update the Mongo database with information.
class Database:

    def __init__(self):
        self.client = py.MongoClient()
        self.db = "myBanking"
        self.accountinfo = "accountinfo"
        self.accountholder = "accountholder"
        self.nonacct = "User doesn't exists"

        

    def __repr__(self):
        return "This is the database class"
    
    def createUser(self, firstName, lastName):
        if firstName in self.getAccNum(firstName,lastName):
            return "\nThere is an account under that name\n"
            
        else:
            while True:
                accountNum = random.randint(10000,1000000)
                checkacct = self.client[self.db][self.accountholder].find({"accountNum": accountNum})
                if bool(checkacct):
                    break
                else:
                    accountNum = random.randint(10000,1000000)
            query = {
                    "_id":accountNum,
                    "FirstName": firstName,
                    "LastName": lastName,
                    "accountNum": accountNum
                    }
            query2 = {
                    "_id":accountNum,
                    "accountNum": accountNum,
                    "balance": 0
                    }
            self.client[self.db][self.accountholder].insert_one(query)
            self.client[self.db][self.accountinfo].insert_one(query2)
            return "{f} {l} account has been created. The account number is {a}\n".format(
                                                                                        f=firstName,
                                                                                        l=lastName,
                                                                                        a=accountNum
                                                                                        )
    
    def depWidth(self, accountNum, funds):
        self.client[self.db][self.accountinfo].update_one(
                                                        {"accountNum": accountNum},
                                                        {'$inc': {"balance": funds}}
                                                        )

        
    def balance(self, accountNum):
        balance = list(self.client[self.db][self.accountinfo].find(
                                                                {"accountNum": accountNum},
                                                                {"_id": 0, "balance": 1}
                                                                ))
        for bal in balance:
            return bal.get("balance")
        
    def getAccNum(self, firstname, lastname):
        acc = list(self.client[self.db][self.accountholder].find(
                                                                    {"LastName": lastname,
                                                                     "FirstName": firstname},
                                                                    {"_id": 0}
                                                                    ))
        if bool(acc):
            for num in acc:
                return "{f} {l} account number is {a}\n".format(
                                                        f=num.get("FirstName"),
                                                        l=num.get("LastName"),
                                                        a=num.get("accountNum")
                                                        )
        else:                                                           
            return self.nonacct


            
#Class creates the user interface and set the interaction for users.
class Gui:
    
    # The init creates the buttons, entry, labels, and text box
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        
        #Top label to show application name an grid position
        self.tlabel = Label(
                            frame,text="Banking Application",
                            font=("Courier", 44)
                            )
        self.tlabel.grid(
                        row=0,
                        column=0,
                        columnspan = 10
                        )
        
        
        #Account number label and grid position
        self.alabel = Label(
                            frame,
                            text="Account\nNumber:"
                            )
        self.alabel.grid(
                        row=1,
                        column=0,
                        sticky=E
                        )
        
        #first name label and grid position
        self.flabel = Label(
                            frame,text="First Name:"
                            )
        self.flabel.grid(
                        row=2,
                        column=0,
                        sticky=E
                        )
        
        #Last name label and grid position
        self.llabel = Label(
                            frame,
                            text="Last Name:"
                            )
        self.llabel.grid(
                        row=3,
                        column=0,
                        sticky=E
                        )
        
        #Dollar amount label and grid position
        self.dlabel = Label(frame,text="Amount:")
        self.dlabel.grid(
                        row=4,
                        column=0,
                        sticky=E
                        )
        
        #Account number Entry and grid position
        self.aentry = Entry(frame)
        self.aentry.grid(
                        row=1,
                        column=1,
                        columnspan=3,
                        sticky=W
                        )
        
        #First name Entry and grid position
        self.fentry = Entry(frame)
        self.fentry.grid(
                        row=2,
                        column=1,
                        columnspan=3,
                        sticky=W
                        )
        
        #Last name Entry and grid position
        self.lentry = Entry(frame)
        self.lentry.grid(
                        row=3,
                        column=1,
                        columnspan=3,
                        sticky=W
                        )
        
        #Dollar amount Entry and grid position
        self.dentry = Entry(frame)
        self.dentry.grid(
                        row=4,
                        column=1,
                        columnspan=3,
                        sticky=W
                        )
        
        #Creates a button to create a new account
        self.accButton = Button(
                                frame,
                                text="Acct Create",
                                command=self.createUser
                                ) 
        self.accButton.grid(row=5,column=0,sticky=W)   
        
        #Creates a button for Deposit
        self.depButton = Button(
                                frame,
                                text="  Deposit   ",
                                command=self.deposit
                                ) 
        self.depButton.grid(row=5,column=1,sticky=W)
        
        #Creates a button for withdraw   
        self.withButton = Button(
                                frame,
                                text="  Withdraw  ",
                                command=self.withdraw
                                ) 
        self.withButton.grid(row=5,column=2,sticky=W)
        
        #Creates a button for Balance
        self.balButton = Button(
                                frame,
                                text="  Balance   ",
                                command=self.printBalanceMessage
                                ) 
        self.balButton.grid(row=5,column=3,sticky=W)   
        
        #Create a button for search
        self.serButton = Button(
                                frame,
                                text="   Search   ",
                                command=self.searchUser
                                ) 
        self.serButton.grid(row=6,column=0,sticky=W)
        
        
        
        #Create a Text box
        self.txt = Text(
                        frame,
                        width=50,
                        height=30,
                        wrap=WORD,
                        highlightbackground="grey",)
        self.txt.grid(row=1, column=5, rowspan=10)
  
        


    #Function to print balance of the account.
    def printBalanceMessage(self):
        dbconnect = Database()
        if self.accountCheck():
            clientN = "The balance of the account is ${:,.2f}\n".format(
                                                                dbconnect.balance(
                                                                                    int(self.aentry.get())
                                                                                        ))
            self.txt.insert(0.0, clientN)
        else:
            clientN = "Please input an account number to view the balance of the account.\n"
            self.txt.insert(0.0, clientN)
            
    #Deposit money into the account.
    def deposit(self):
        dbconnect = Database()
        if self.amountCheck() and self.accountCheck():
            dbconnect.depWidth(
                            int(self.aentry.get()),
                            float(self.dentry.get())
                            )
            clientN = "The new balance of the account is {:,.2f}\n".format(dbconnect.balance(int(self.aentry.get())))
            self.txt.insert(0.0, clientN)
        elif self.amountCheck():
            clientN = "Please input an account number.\n"
            self.txt.insert(0.0, clientN)
        elif self.accountCheck():
            clientN = "Please input the dollar amount.\n"
            self.txt.insert(0.0, clientN)
        else:
            clientN = "Please input an account number and dollar amount.\n"
            self.txt.insert(0.0, clientN)
            
    #Function to withdraw money from the account.
    def withdraw(self):
        if self.amountCheck() and self.accountCheck():
            dbconnect = Database()
            if dbconnect.balance(int(self.aentry.get())) < float(self.dentry.get()):
                self.txt.insert(0.0, "There are not enough funds to with draw that amount\n")
            else:
                dbconnect.depWidth(
                                   int(self.aentry.get()),
                                   (-1*float(self.dentry.get()))
                                   )
                clientN = "The new balance of the account is ${:,.2f}\n".format(dbconnect.balance(int(self.aentry.get())))
                self.txt.insert(0.0, clientN)
        elif self.amountCheck():
            clientN = "Please input an account number.\n"
            self.txt.insert(0.0, clientN)
        elif self.accountCheck():
            clientN = "Please input the dollar amount.\n"
            self.txt.insert(0.0, clientN)
        else:
            clientN = "Please input an account number and dollar amount.\n"
            self.txt.insert(0.0, clientN)
    #Function to Create a new account.
    def createUser(self):
        dbconnect = Database()
        clientN=dbconnect.createUser(
                                    self.fentry.get(),
                                    self.lentry.get()
                                    )
        self.txt.insert(0.0, clientN)
   
    #Function to search for User's account number using first and last name.        
    def searchUser(self):
        dbconnect = Database()
        clientN=dbconnect.getAccNum(
                                    self.fentry.get(),
                                    self.lentry.get()
                                    )
        self.txt.insert(0.0, clientN)

    #Function checks to make sure first name and last name is not empty/
    def inputCheck(self):
        if (len(self.fentry.get()) == 0) or (len(self.lentry.get()) == 0):
            return False
        else:
            return True

    #Function checks to make sure dollar amount field is not empty.    
    def amountCheck(self):
        if (len(self.dentry.get()) == 0):
            return False
        else:
            return True

    #Function check to make sure the entry for account number is not empty.
    def accountCheck(self):
        if (len(self.aentry.get())==0):
            return False
        else:
            return True




#Function to build the application GUI.
def main():
    myGui = Tk()
    myGui.title("BankofPython")
    Gui(myGui)
    myGui.mainloop()




#Calls the main function to start the application.
main()

