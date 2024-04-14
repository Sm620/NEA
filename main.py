import csv
from tkinter import *
from tkinter import ttk
import customtkinter
import smtplib
import random
import socket
import threading

randomCodeValue = str(random.randint(99999,999999))

def loginPage():
    def login():
        loggedIn = False
        # Gets username and password from the input boxes and stores as variables
        attemptUsername = usernameInput.get()
        attemptPassword = passwordInput.get()
        while loggedIn == False:
            # Reading the csv file
            with open("credentials.csv","r") as csvFileCredentials:
                csvReader = csv.reader(csvFileCredentials)
                next(csvReader)
                # For each line
                for line in csvReader:
                    if attemptUsername.lower() == line[0] and attemptPassword == line[1]: # If credentials are correct
                        loggedIn = True
                        # Storing name of logged in user
                        with open("currentSessionID.txt","w") as file:
                            file.write(attemptUsername.lower())
                            file.close()
                        break
                    else:
                        continue
                # If details are incorrect
                if loggedIn == False:
                    del attemptUsername, attemptPassword
                    # Deleting input boxes data
                    usernameInput.delete(0,END)
                    passwordInput.delete(0,END)
                    # Add Incorrect Label
                    incorrectLabel = customtkinter.CTkLabel(loginFrame,
                                            text = "Incorrect",
                                            width = 50,
                                            height = 20,
                                            bg_color = "white",
                                            font = customtkinter.CTkFont(size = 18),
                                            text_color = "red")
                    incorrectLabel.place(x = 215, y = 360)
                # If correct details
                elif loggedIn == True:
                    # displaying next page depening on whether the user is a catering staff member or student
                    loginFrame.destroy()
                    with open("credentials.csv","r") as credentialsFile:
                        csv_reader = csv.DictReader(credentialsFile)
                        for row in csv_reader:
                            if row['Username'] == attemptUsername:
                                userType = row["Usertype"]

                    if userType == "Student":
                        menuPage()
                    elif userType == "Staff":
                        cateringPage()
                else:
                    print("Error")

    def sendEmailPage():

        def sendEmail():

            def check():
                if otpInput.get() == randomCodeValue:
                    # Removing widgets
                    otpInput.destroy()
                    otpButton.destroy()
                    otpInstructions.destroy()
                    menuPage()
                else:
                    incorrectLabel = customtkinter.CTkLabel(forgotFrame,
                                                            text = "incorrect",
                                                            text_color = "red",
                                                            bg_color = "white")
                    incorrectLabel.place(x = 10, y = 130)

            # Reading the csv file
            with open("credentials.csv","r") as csvFile:
                csvReader = csv.reader(csvFile)
                next(csvReader)
                # getting username and email
                username = passwordForgotInput.get()
                for line in csvReader:
                    if username == line[0]:
                        recipientEmail = line[2]

            # Details to sign into account and send email
            senderEmail = "orderingsystem531@example.com"
            senderEmailPassword = "example"
            body = 'Subject: One Time Passcode .\nDear user, \n\n' + 'Your One Time Passcode is below:' + '\n\n' + randomCodeValue
            # Testing for errors
            try:
                smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587) # 587 is port number
            except Exception as e:
                # If error occurs do this
                print(e)
                smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465) # 465 is port number
            # Logging in and sending the email
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(senderEmail, senderEmailPassword)
            smtpObj.sendmail(senderEmail, recipientEmail, body)
            smtpObj.quit()

            # Removing send email button, input and instuctions
            instructionsLabel.destroy()
            passwordForgotInput.destroy()
            sendButton.destroy()

            # One Time Passcode Instuctions
            otpInstructions = customtkinter.CTkLabel(forgotFrame,
                                                    text = "Enter the OTP sent to your email below.",
                                                    bg_color = "white",
                                                    text_color = "gray50",
                                                    font = customtkinter.CTkFont(size = 14))
            otpInstructions.place(x = 35, y = 100)

            # Enter One Time Passcode entry box
            otpInput = customtkinter.CTkEntry(forgotFrame,
                                              placeholder_text = "Input OTP")
            otpInput.place(x = 50, y = 170)

            # One Time Passcode enter button
            otpButton = customtkinter.CTkButton(forgotFrame,
                                                text = "Enter",
                                                command = check)
            otpButton.place(x = 50, y = 250)

        # destroying login frame to add new frame
        loginFrame.destroy()
        # Forgot Frame
        forgotFrame = customtkinter.CTkFrame(backgroundFrame,
                                            width = 300,
                                            height = 300,
                                            corner_radius = 10,
                                            fg_color = "white",
                                            border_color = "orange3",
                                            border_width = 1.5,
                                            bg_color = "floralwhite")
        forgotFrame.place(x = 800, y = 300)
       
        # Forgot Label
        forgotLabel = customtkinter.CTkLabel(forgotFrame,
                                             text = "Forgot Password?",
                                             text_color = "Orange",
                                             font = customtkinter.CTkFont(family = "Bahnschrift SemiBold Condensed",
                                                                     size = 40))
        forgotLabel.place(x = 40, y = 20)

        # Instructions Label
        instructionsLabel = customtkinter.CTkLabel(forgotFrame,
                                                   text = "Enter your username and a one\ntime passcode will be sent to the email\nregistered with that account",
                                                   bg_color = "white",
                                                   text_color = "gray50",
                                                   font = customtkinter.CTkFont(size = 14))
        instructionsLabel.place(x = 35, y = 100)

        # Username Input if forgot password
        passwordForgotInput = customtkinter.CTkEntry(forgotFrame,
                                                    width = 200,
                                                    height = 40,
                                                    corner_radius = 7,
                                                    placeholder_text = "Please enter your Username",
                                                    bg_color = "white",
                                                    border_color = "orange",
                                                    fg_color = "white",
                                                    text_color = "black")
        passwordForgotInput.place(x = 50, y = 170)

        # Send Email Button
        sendButton = customtkinter.CTkButton(forgotFrame,
                                        text = "Send Email",
                                        width = 200,
                                        height = 30,
                                        command = sendEmail,
                                        corner_radius = 20,
                                        bg_color = "white",
                                        fg_color = "orange3",
                                        hover_color = "orange4",
                                        font = customtkinter.CTkFont(size = 17,
                                                                    weight = "bold"))
        sendButton.place(x = 50, y = 250)

        # Reading the csv file
        with open("credentials.csv","r") as csvFile:
            csvReader = csv.reader(csvFile)
            next(csvReader)
            # getting username and email
            username = passwordForgotInput.get()
            for line in csvReader:
                if username == line[0]:
                    recipientEmail = line[2]
                    # Sending email to user
                    sendEmail()

    # Background Frame
    backgroundFrame = customtkinter.CTkFrame(app,
                                        width = 1920,
                                        height = 1080,
                                        corner_radius = 0,
                                        fg_color = "floralwhite")
    backgroundFrame.place(x = 0, y = 0)

    # Login Frame
    loginFrame = customtkinter.CTkFrame(backgroundFrame,
                                        width = 500,
                                        height = 500,
                                        corner_radius = 10,
                                        fg_color = "white",
                                        border_color = "orange3",
                                        border_width = 1.5,
                                        bg_color = "floralwhite")
    loginFrame.place(x = 715, y = 200)

    # Login Button
    loginButton = customtkinter.CTkButton(loginFrame,
                                        text = "Login",
                                        width = 400,
                                        height = 30,
                                        command = login,
                                        corner_radius = 20,
                                        bg_color = "white",
                                        fg_color = "orange3",
                                        hover_color = "orange4",
                                        font = customtkinter.CTkFont(size = 17,
                                                                    weight = "bold"))
    loginButton.place(x = 50, y = 400)

    # Login Label
    loginLabel = customtkinter.CTkLabel(loginFrame,
                                        text = "Login",
                                        corner_radius = 8,
                                        bg_color = "white",
                                        text_color = "orange",
                                        font = customtkinter.CTkFont(family = "Bahnschrift SemiBold Condensed",
                                                                     size = 70))
    loginLabel.place(x = 170, y = 10)

    # Progress Bar 1
    progressbar1 = customtkinter.CTkProgressBar(loginFrame,
                                            width = 400,
                                            height = 5,
                                            border_width = 0,
                                            progress_color = "orange")
    progressbar1.place(x = 48, y = 120)
    progressbar1.set(1)

    # Progress Bar 2
    progressbar2 = customtkinter.CTkProgressBar(loginFrame,
                                            width = 100,
                                            height = 5,
                                            border_width = 0,
                                            progress_color = "orange")
    progressbar2.place(x = 190, y = 150)
    progressbar2.set(1)

    # Username Label
    usernameLabel = customtkinter.CTkLabel(loginFrame,
                                           bg_color = "white",
                                           text_color = "gray50",
                                           text = "Username: ",
                                           font = customtkinter.CTkFont(size = 20))
    usernameLabel.place(x = 55, y = 180)

    # Username Input Box
    usernameInput = customtkinter.CTkEntry(loginFrame,
                                        width = 400,
                                        height = 40,
                                        corner_radius = 7,
                                        placeholder_text = "Please enter your username",
                                        bg_color = "white",
                                        border_color = "orange",
                                        fg_color = "white",
                                        text_color = "black")
    usernameInput.place(x = 50, y = 210)

    # Password Label
    passwordLabel = customtkinter.CTkLabel(loginFrame,
                                           bg_color = "white",
                                           text_color = "gray50",
                                           text = "Password: ",
                                           font = customtkinter.CTkFont(size = 20))
    passwordLabel.place(x = 55, y = 270)

    # Password Input Box
    passwordInput = customtkinter.CTkEntry(loginFrame,
                                        width = 400,
                                        height = 40,
                                        corner_radius = 7,
                                        placeholder_text = "Please enter your password",
                                        bg_color = "white",
                                        border_color = "orange",
                                        fg_color = "white",
                                        text_color = "black")
    passwordInput.place(x = 50, y = 300)

    # Forgot Password Button
    forgotButton = customtkinter.CTkButton(loginFrame,
                                           text = "Forgot Password?",
                                           bg_color = "white",
                                           command = sendEmailPage)
    forgotButton.place(x = 180, y = 450)

def cateringPage():

    # Catering Frame
    cateringFrame = customtkinter.CTkFrame(app,
                                        width = 1920,
                                        height = 930,
                                        fg_color = "white",
                                        bg_color = "white")
    cateringFrame.place(x = 0, y = 150)

    # Catering Frame for Label
    cateringLabelFrame = customtkinter.CTkFrame(app,
                                            width = 1920,
                                            height = 150,
                                            fg_color = "orange",
                                            bg_color = "orange",
                                            corner_radius = 0)
    cateringLabelFrame.place(x = 0, y = 0)

    # Catering Label
    cateringLabel = customtkinter.CTkLabel(cateringLabelFrame,
                                       text = "Catering Page",
                                       text_color = "white",
                                       font = customtkinter.CTkFont(family = "Bahnschrift SemiBold Condensed",
                                                                     size = 70))
    cateringLabel.place(x = 850, y = 25)

    # Function to remove an item from the CSV file
    def removeItem(itemName):
        headerRow = []
        # Opening file and reading data
        with open("catering.csv", "r") as basket_file:
            csv_reader = csv.reader(basket_file)
            data = list(csv_reader) # Stores as a list

            # Search for the item to be removed and remove it from the updated data
            headerRow = [data[0]]  # Header row
            for row in data[1:]:
                if row[0] != itemName:  # Assuming the item name is in the first column
                    headerRow.append(row)
            
            # Write the updated data back to the user's basket file
            with open("catering.csv", "w", newline='') as cateringFile:
                csv_writer = csv.writer(cateringFile)
                csv_writer.writerows(headerRow)

        # Redisplaying items after csv updated
        cateringPage()

    def orderDisplay():
        # Opening basket and reading data
        with open("catering.csv", "r") as cateringFile:
            csvReader = csv.reader(cateringFile)
            data = list(csvReader)

            # Check if there is at least one row of data
            if len(data) > 1:

                # Extract column headers and data
                headers = data[0]
                data_rows = data[1:]

                # Create labels for column headers
                itemNameLabel = customtkinter.CTkLabel(cateringFrame, text=headers[0], font=("Arial", 12, "bold"), text_color="black", bg_color="white")
                itemNameLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

                usernameLabel = customtkinter.CTkLabel(cateringFrame, text=headers[1], font=("Arial", 12, "bold"), text_color="black", bg_color="white")
                usernameLabel.grid(row=0, column=1, padx=10, pady=10, sticky="w")

                # Display item names and prices in separate labels
                for rowIndex, row in enumerate(data_rows):
                    itemName = row[0]  # Item name is in the first column
                    username = row[1]  # Username is in the second column

                    itemNameLabel = customtkinter.CTkLabel(cateringFrame, text=itemName, text_color="black")
                    itemNameLabel.grid(row=rowIndex + 1, column=0, padx=10, pady=5, sticky="w")

                    usernameLabel = customtkinter.CTkLabel(cateringFrame, text=username, text_color="black")
                    usernameLabel.grid(row=rowIndex + 1, column=1, padx=10, pady=5, sticky="w")

                # Display a Remove button for each item
                for rowIndex, row in enumerate(data_rows):
                    itemName = row[0]  # Item name is in the first column

                    # Create a Remove button for each item
                    remove_button = customtkinter.CTkButton(cateringFrame,
                                                            text="Remove",
                                                            command=lambda item=itemName: removeItem(item))
                    remove_button.grid(row=rowIndex + 1, column=2, padx=10, pady=5, sticky="w")

    orderDisplay()

# Function to display money in users account
def displayMoney():
    # Getting name of logged in user
    with open("currentSessionID.txt", "r") as textFile:
        name = textFile.readline().strip()

        # Getting basket depending on the name that was recieved
        with open("credentials.csv", "r") as credentials_file:
            csv_reader = csv.DictReader(credentials_file)
            for row in csv_reader:
                if row["Username"] == name:
                    return row["Money"]
                
# Storing return value in variable
currentMoney = displayMoney()

def menuPage():

    #When basket button is pressed
    def basketRedirect():
        menuFrame.destroy()
        basketPage()

    #When add to cart button is pressed
    def addCart(itemName, price):
        #Returning name of currently logged in user
        with open("currentSessionID.txt", 'r') as text_file:
            name = text_file.readline().strip()

            #Getting basket depending on the name that was recieved
            with open("credentials.csv", 'r') as credentials_file:
                csv_reader = csv.DictReader(credentials_file)
                for row in csv_reader:
                    if row["Username"] == name:
                        userBasket = row["Basket"]

                        #Opening basket and adding menu item with price
                        with open(userBasket, "a", newline = '') as basket_file:
                            fieldnames = ["Item Name", "Price"]
                            csv_append = csv.DictWriter(basket_file, fieldnames = fieldnames)
                            csv_append.writerow({"Item Name": itemName, "Price": price})

    #Menu Frame
    menuFrame = customtkinter.CTkFrame(app,
                                        width = 1920,
                                        height = 1080,
                                        fg_color = "white")
    menuFrame.place(x = 0, y = 0)

    #Menu Frame for Label
    menuLabelFrame = customtkinter.CTkFrame(menuFrame,
                                            width = 1920,
                                            height = 150,
                                            fg_color = "orange",
                                            corner_radius = 0)
    menuLabelFrame.place(x = 0, y = 0)

    #Menu Label
    menuLabel = customtkinter.CTkLabel(menuLabelFrame,
                                       text = "Menu",
                                       text_color = "white",
                                       font = customtkinter.CTkFont(family = "Bahnschrift SemiBold Condensed",
                                                                     size = 70))
    menuLabel.place(x = 900, y = 25)

    #Food Item Frame 1
    foodItemFrame1 = customtkinter.CTkFrame(menuFrame,
                                        width = 300,
                                        height = 400,
                                        bg_color = "white",
                                        fg_color = "white",
                                        border_color = "orange3",
                                        border_width = 1.5,
                                        corner_radius = 10)
    foodItemFrame1.place(x = 200, y = 300)

    #Food Item 1 Details
    item1Name = customtkinter.CTkLabel(foodItemFrame1,
                                       text = "Chicken Burger",
                                       text_color = "black",
                                       font = customtkinter.CTkFont(size = 30))
    item1Name.place(x = 5, y = 10)

    item1Price = customtkinter.CTkLabel(foodItemFrame1,
                                       text = "£2",
                                       text_color = "black")
    item1Price.place(x = 5, y = 40)

    item1Ingredients = customtkinter.CTkLabel(foodItemFrame1,
                                       text = "Ingredients: Water",
                                       text_color = "black")
    item1Ingredients.place(x = 5, y = 60)

    item1AddCart = customtkinter.CTkButton(foodItemFrame1,
                                       text = "Add to cart",
                                       text_color = "black",
                                       command = lambda: addCart("Chicken Burger","2"))
    item1AddCart.place(x = 5, y = 100)

    #Food Item Frame 2
    foodItemFrame2 = customtkinter.CTkFrame(menuFrame,
                                        width = 300,
                                        height = 400,
                                        bg_color = "white",
                                        fg_color = "white",
                                        border_color = "orange3",
                                        border_width = 1.5,
                                        corner_radius = 10)
    foodItemFrame2.place(x = 600, y = 300)

    #Food Item 2 Details
    item2Name = customtkinter.CTkLabel(foodItemFrame2,
                                       text = "Pizza",
                                       text_color = "black",
                                       font = customtkinter.CTkFont(size = 30))
    item2Name.place(x = 5, y = 10)

    item2Price = customtkinter.CTkLabel(foodItemFrame2,
                                       text = "£1.10",
                                       text_color = "black")
    item2Price.place(x = 5, y = 40)

    item2Ingredients = customtkinter.CTkLabel(foodItemFrame2,
                                       text = "Ingredients: Water",
                                       text_color = "black")
    item2Ingredients.place(x = 5, y = 60)

    item2AddCart = customtkinter.CTkButton(foodItemFrame2,
                                       text = "Add to cart",
                                       text_color = "black",
                                       command = lambda: addCart("Pizza","1.10"))
    item2AddCart.place(x = 5, y = 100)

    #Food Item Frame 3
    foodItemFrame3 = customtkinter.CTkFrame(menuFrame,
                                        width = 300,
                                        height = 400,
                                        bg_color = "white",
                                        fg_color = "white",
                                        border_color = "orange3",
                                        border_width = 1.5,
                                        corner_radius = 10)
    foodItemFrame3.place(x = 1000, y = 300)

    #Food Item 3 Details
    item3Name = customtkinter.CTkLabel(foodItemFrame3,
                                       text = "Chicken Wrap",
                                       text_color = "black",
                                       font = customtkinter.CTkFont(size = 30))
    item3Name.place(x = 5, y = 10)

    item3Price = customtkinter.CTkLabel(foodItemFrame3,
                                       text = "£1.80",
                                       text_color = "black",
                                       font = customtkinter.CTkFont(size = 20))
    item3Price.place(x = 5, y = 60)

    item3Ingredients = customtkinter.CTkLabel(foodItemFrame3,
                                       text = "Ingredients: Water",
                                       text_color = "black")
    item3Ingredients.place(x = 5, y = 100)

    item3AddCart = customtkinter.CTkButton(foodItemFrame3,
                                       text = "Add to cart",
                                       text_color = "black",
                                       command = lambda: addCart("Chicken Wrap","1.80"))
    item3AddCart.place(x = 5, y = 140)

    #Basket Button
    basketButton = customtkinter.CTkButton(menuFrame,
                                           text = "Basket",
                                           width = 30,
                                           height = 20,
                                           font = customtkinter.CTkFont(size = 30),
                                           command = basketRedirect)
    basketButton.place(x = 1800, y = 400)

    # Creating a label for the money the user has in the account
    moneyText = customtkinter.CTkLabel(menuFrame, 
                                        text = "",
                                        text_color = "orange",
                                        bg_color = "white",
                                        font = customtkinter.CTkFont(size = 22))
    moneyText.place(x = 50, y = 150)

    # Calling function to display money remaining after purchase and changes text
    moneyText.configure(text = f"Balance: £{currentMoney}")

def basketPage():
    
    def purchasePage():

        # Creating variable to store total price of all items in the users basket
        priceOfItems = 0

        # Calculating total cost of items in users basket
        # Getting name of currently logged in user
        with open("currentSessionID.txt", 'r') as textFile:
            name = textFile.readline().strip()

            # Getting basket depending on the name that was recieved
            with open("credentials.csv", 'r') as credentialsFile:
                csv_reader = csv.DictReader(credentialsFile)
                for row in csv_reader:
                    if row["Username"] == name:
                        userBasket = row["Basket"]
                        currentBalance = row["Money"]

                        # Opening basket and reading data to add up values of items in the users basket
                        with open(userBasket, "r") as basketFile:
                            csvReader = csv.DictReader(basketFile)
                            for item in csvReader:
                                price = (float(item["Price"]))
                                priceOfItems += round(price,2) # Rounding to 2 decimal places

        # Calculating whether the user has enough money to purchase items in basket
        # If user has enough money
        currentBalance = float(currentBalance) # Converting data to float type
        if currentBalance >= priceOfItems and priceOfItems != 0:
            currentBalance -= priceOfItems
            currentBalance = round(currentBalance,2) # Rounding to 2dp
            
            # Changing money in users account after item purchase
            # Getting name of logged in user
            with open("currentSessionID.txt", "r") as textFile:
                name = textFile.readline().strip()

            # Getting basket depending on the name that was recieved
            with open("credentials.csv", "r") as credentialsFile:
                # Getting fieldnames from header
                csvReader = csv.DictReader(credentialsFile) 
                fieldnames = csvReader.fieldnames
                data = list(csvReader) # Storing information in csv file as a list in a newly created variable
                print(data)

            # Updating money for specific user
            for row in data:
                if row["Username"] == name:
                    row["Money"] = currentBalance

            # Writing data back to credentials.csv
            with open("credentials.csv", "w", newline='') as credentialsFile:
                csvWriter = csv.DictWriter(credentialsFile, fieldnames = fieldnames)
                csvWriter.writeheader()  # Write the header row with all fieldnames
                csvWriter.writerows(data)

            # Removing everything from the users basket file and then rewiritng the headers
            # Reading header files
            with open(userBasket, "r", newline='') as csvFile:
                reader = csv.reader(csvFile)
                # Reading and creating a variable for the first row of the csv file containing the headers
                header = next(reader)
            
            # Opening with write function
            with open(userBasket, "w", newline='') as csvFile:
                writer = csv.writer(csvFile)
                # Writing the header after clearing the file
                writer.writerow(header)

            # Updating currentMoney variable to output correct amount of money remaining after purhchase
            currentMoney = displayMoney()

            def sendToServer(itemName):
                # Server configuration
                serverAddress = ('192.168.0.100', 138)  # Server ip and port 
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket: # Address family and socket type

                    try:
                        # Connect to the server
                        clientSocket.connect(serverAddress)
                        # Add name of person who ordered
                        dataToSend = itemName.strip() + name
                        # Send data to the server
                        clientSocket.sendall(dataToSend.encode())
                        print(f"Sent data: {dataToSend}")
                        clientSocket.close()
                    
                    except Exception as e:
                        print("Error:", str(e))

            with open(userBasket, 'r') as csvFile:
                csvReader = csv.reader(csvFile)
                next(csvReader) # Skip header
                for row in csvReader:
                    itemName = row[0]
                    sendToServer(itemName) 

            # Creating Purchase Frame
            purchaseFrame = customtkinter.CTkFrame(app,
                                                width = 800,
                                                height = 600,
                                                bg_color = "white",
                                                border_color = "orange3",
                                                border_width = 1,
                                                fg_color = "white")
            purchaseFrame.place(x = 580, y = 200)

            # Creating purchase text for purchase frame
            purchaseText = customtkinter.CTkLabel(purchaseFrame,
                                                text = "Successful Purchase",
                                                text_color = "Orange",
                                                bg_color = "white",
                                                font = customtkinter.CTkFont(family = "Bahnschrift SemiBold Condensed",
                                                                                size = 70))
            purchaseText.place(x = 20, y = 10)

            # Creating a label for the remaining money the user has
            moneyText = customtkinter.CTkLabel(purchaseFrame, 
                                                text = "",
                                                text_color = "orange",
                                                bg_color = "white",
                                                font = customtkinter.CTkFont(size = 22))
            moneyText.place(x = 50, y = 120)

            # Calling function to display money remaining after purchase and changes text
            moneyText.configure(text = f"Account Balance: £{currentMoney}")

        else:
            errorLabel = customtkinter.CTkLabel(basketFrame,
                                                text = "Error")
            errorLabel.place(x = 800, y = 800)


    # Function to remove an item from the CSV file
    def removeItem(itemName):
        # Getting name of currently logged in user
        with open("currentSessionID.txt", 'r') as text_file:
            name = text_file.readline().strip()

            # Getting basket depending on the name that was recieved
            with open("credentials.csv", 'r') as credentials_file:
                csv_reader = csv.DictReader(credentials_file)
                for row in csv_reader:
                    if row["Username"] == name:
                        userBasket = row["Basket"]

                        # Opening basket and reading data
                        with open(userBasket, "r") as basket_file:
                            csv_reader = csv.reader(basket_file)
                            data = list(csv_reader)

        # Find the user's row in the credentials.csv file
        headerRow = []

        # Read the user's basket file
        with open(userBasket, "r") as basket_file:
            csv_reader = csv.reader(basket_file)
            data = list(csv_reader)
            
        # Search for the item to be removed and remove it from the updated data
        headerRow = [data[0]]  # Header row
        for row in data[1:]:
            if row[0] != itemName:  # Assuming the item name is in the first column
                headerRow.append(row)
        
        # Write the updated data back to the user's basket file
        with open(userBasket, "w", newline='') as basket_file:
            csv_writer = csv.writer(basket_file)
            csv_writer.writerows(headerRow)

        # Redisplaying items after csv updated
        basketPage()

    def itemDisplay():
        # Returning name of currently logged in user
        with open("currentSessionID.txt", 'r') as text_file:
            name = text_file.readline().strip()

            # Getting basket depending on the name that was recieved
            with open("credentials.csv", 'r') as credentials_file:
                csv_reader = csv.DictReader(credentials_file)
                for row in csv_reader:
                    if row["Username"] == name:
                        userBasket = row["Basket"]

                        # Opening basket and reading data
                        with open(userBasket, "r") as basket_file:
                            csv_reader = csv.reader(basket_file)
                            data = list(csv_reader)

                            # Check if there is at least one row of data
                            if len(data) > 1:

                                # Extract column headers and data
                                headers = data[0]
                                data_rows = data[1:]

                                # Create labels for column headers
                                itemNameLabel = customtkinter.CTkLabel(itemFrame, text=headers[0], font=("Arial", 12, "bold"), text_color="black")
                                itemNameLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

                                itemPriceLabel = customtkinter.CTkLabel(itemFrame, text=headers[1], font=("Arial", 12, "bold"), text_color="black")
                                itemPriceLabel.grid(row=0, column=1, padx=10, pady=10, sticky="w")

                                # Display item names and prices in separate labels
                                for rowIndex, row in enumerate(data_rows):
                                    itemName = row[0]  # Item name is in the first column
                                    itemPrice = row[1]  # Item price is in the second column

                                    itemNameLabel = customtkinter.CTkLabel(itemFrame, text=itemName, text_color="black")
                                    itemNameLabel.grid(row=rowIndex + 1, column=0, padx=10, pady=5, sticky="w")

                                    itemPriceLabel = customtkinter.CTkLabel(itemFrame, text=itemPrice, text_color="black")
                                    itemPriceLabel.grid(row=rowIndex + 1, column=1, padx=10, pady=5, sticky="w")

                                # Display a Remove button for each item
                                for rowIndex, row in enumerate(data_rows):
                                    itemName = row[0]  # Item name is in the first column

                                    # Create a Remove button for each item
                                    remove_button = customtkinter.CTkButton(itemFrame,
                                                                            text="Remove",
                                                                            command=lambda item=itemName: removeItem(item))
                                    remove_button.grid(row=rowIndex + 1, column=2, padx=10, pady=5, sticky="w")

    # Outputting basket page
    basketFrame = customtkinter.CTkFrame(app,
                                        width = 1920,
                                        height = 1080,
                                        fg_color = "white")
    basketFrame.place(x = 0, y = 0)

    # Creating frame for Basket header
    basketFrameLabel = customtkinter.CTkLabel(basketFrame,
                                            width = 1920,
                                            height = 150,
                                            fg_color = "orange")
    basketFrameLabel.place(x = 0, y = 0)

    # Basket label
    basketLabel = customtkinter.CTkLabel(basketFrameLabel,
                                        text = "Basket",
                                        text_color = "white",
                                        font = customtkinter.CTkFont(family = "Bahnschrift SemiBold Condensed",
                                                                     size = 70))
    basketLabel.place(x = 900, y = 25)

    # Scrollable frame where basket data will be displayed
    itemFrame = customtkinter.CTkScrollableFrame(basketFrame,
                                                 width = 800,
                                                 height = 300,
                                                 fg_color = "white",
                                                 scrollbar_button_color="black")
    itemFrame.place(x = 400, y = 250)

    # Purchase Button
    purchaseButton = customtkinter.CTkButton(basketFrame,
                                             text = "Purchase",
                                             command = purchasePage)
    purchaseButton.place(x = 800, y = 900)

    # Creating a label for the money the user has in the account
    moneyText = customtkinter.CTkLabel(basketFrame, 
                                        text = "",
                                        text_color = "orange",
                                        bg_color = "white",
                                        font = customtkinter.CTkFont(size = 22))
    moneyText.place(x = 50, y = 150)

    # Calling function to display money remaining after purchase and changes text
    moneyText.configure(text = f"Balance: £{currentMoney}")

    itemDisplay()

# Creating the display window for the GUI
app = customtkinter.CTk()
app.title("Ordering System")
app.geometry("1920x1080")

#Running program
loginPage()

#Looping window
app.mainloop()
