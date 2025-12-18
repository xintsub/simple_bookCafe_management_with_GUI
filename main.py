import dearpygui.dearpygui as dpg
import datetime

class product:
    def __init__(self, price, name, stock):
        self.price = price
        self.name = name
        self.stock = stock

class drink(product):
    def __init__(self, price, name, size, type):
        super().__init__(price, name, 0)
        self.size = size
        self.type = type
    def getDrink(self):
        return self.name + " - " + self.size + " - " + self.type

class book(product):
    def __init__(self, price, name, author):
        super().__init__(price, name, 0)
        self.author = author
    def getBook(self):
        return self.name + " - " + self.author

class table:
    def __init__(self, number):
        self.number = number # Number of the table
        self.books = []
        self.drinks = []
        self.totalBill = 0
        self.drinkCount = 0
        self.bookCount = 0
    def addBook(self, bk):
        self.books.append(bk)
        self.bookCount += 1
    def addDrink(self, drnk):
        self.drinks.append(drnk)
        self.drinkCount += 1
    def bookCount(self):
        return self.bookCount
    def drinkCount(self):
        return self.drinkCount
    def calculateBill(self):
        self.totalBill = 0
        if self.bookCount != 0:
            self.totalBill += float(sum(i.price for i in self.books))
        if self.drinkCount != 0:
            self.totalBill += float(sum(i.price for i in self.drinks))
        return self.totalBill
    def clearTable(self):
        self.books.clear()
        self.drinks.clear()
        self.totalBill = 0
        self.bookCount = 0
        self.drinkCount = 0

# Setting menu colors and styles
def init_style():
    with dpg.theme(tag="custom_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (46, 26, 21, 240))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (185, 185, 185, 110))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (217, 216, 216, 110))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (204, 204, 204, 110))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (70, 66, 66, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 66, 66, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (176, 174, 176, 172))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (201, 199, 201, 172))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (194, 193, 194, 172))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (248, 248, 248, 79))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (244, 244, 245, 204))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (202, 202, 203, 255))

            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3.0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1.0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.490, 0.500)

cT = 0 # Index of currently selected table

# Tab for adding books
def bookTab():
    # Checking if this window already exist
    if dpg.does_item_exist("add_book_window"):
        dpg.delete_item("add_book_window")
    # Creating new window named "Add Book" with size of 400x145 at 200, 200 position
    with dpg.window(label="Add Book", width=400, height=145, pos=(200, 200),
                    tag="add_book_window", no_resize=True, no_collapse=True):
        # Book name input
        dpg.add_text("Name", pos=(28, 49))
        dpg.add_input_text(tag="book_name", width=150, pos=(78, 49))

        # Book author input
        dpg.add_text("Author", pos=(28, 79))
        dpg.add_input_text(tag="book_author", width=150, pos=(78, 79))

        # Book price input
        dpg.add_text("Price", pos=(28, 109))
        dpg.add_input_text(tag="book_price", width=150, pos=(78, 109))

        # Add Book button
        dpg.add_button(label="Add Book", width=130, height=80, pos=(250, 49), callback=bookButton)

# Method for getting current selected table
def curTable():
    global selectedTable
    return int((selectedTable.replace("Table ", ""))) - 1 # Getting string from combo, deleting "Table " part then converting to integer

# Button for adding books
def bookButton():
    toAdd = book(int(dpg.get_value("book_price")), dpg.get_value("book_name"), dpg.get_value("book_author"))
    tables[curTable()].addBook(toAdd)
    updateMenu()

# Method for reducing the stock when a new order is created
def reduceStock(name):
    temp = open("temp.txt", "w") # Open temp file for writing
    counter = 0
    for i in inv: # Looping through items in inventory
        counter += 1
        if (i.name != name): # If current item is not the one we are searching for, print it as same
            temp.write(i.name + "," + str(i.price) + "," + str(i.stock))
        else: # If current item is the one we are searching for, print it by reducing the stock by 1
            temp.write(i.name + "," + str(i.price) + "," + str(i.stock - 1))
        if (counter < len(inv)): # Prevent empty line at the end
            temp.write("\n")

    temp.close() # Close temp file
    temp = open("temp.txt", "r") # Open temp file again, for reading this time
    file = open("inventory.txt", "w") # Open inventory file for writing
    lines = temp.readlines() # Read every line in the temp file
    for i in lines: # Write every line in temp file to inventory file
        file.write(i)
    file.close() # Close the inventory file
    temp.close() # Close the temp file
    updateInventory() # Update the inventory

pos3 = (200,200)
# Button for adding orders
def orderButton():
    name = dpg.get_value("order_name") # Get the order name from combobox
    price = 0
    isInStock = False # Boolean for checking the stock status
    size = dpg.get_value("order_size").split(" ")[0] # Get the order size from combobox
    for i in inv: # Loop through every item in inventory
        if(name == i.name):
            price = i.price # Set price to the items price
            if(i.stock > 0):
                isInStock = True # Set boolean to True if the item is in stock
            break
    if(size == "Medium"):
        price = price + 2 # Increase the price if the size is medium
    elif(size == "Large"):
        price = price + 3 # Increase the price if the size is large

    if(isInStock): # If the item is in stock
        toAdd = drink(float(price), name, size, dpg.get_value("order_type")) # Create drink object
        tables[curTable()].addDrink(toAdd) # Add the drink object to the drinks list of current table
        reduceStock(name) # Reduce the stock of the drink
        if dpg.does_item_exist("outOfStockText"): # If "Out of stock!" text exist, delete it
            dpg.delete_item("outOfStockText")
        updateInventoryWindow() # Update the inventory window
    else: # If the item is not in the stock
        if dpg.does_item_exist("outOfStockText"): # If "Out of stock!" text exist, delete it
            dpg.delete_item("outOfStockText")
        # Print "Out of stock!" text again
        dpg.add_text("Out of stock!", pos=[270, 130], parent="add_order_window", tag="outOfStockText")
    updateMenu() # Update the main window


pos2 = (200, 200) # Position definition for Inventory Tab, to be used when updating Inventory Tab
def addItemButton():
    unique = True
    name = dpg.get_value("item_name") # Get the name from text input field
    name = name.strip() # Remove the spaces
    for i in inv: # Check if there is an item with same name
        if(i.name.lower() == name.lower()):
            unique = False
            break
    if(unique == False): # If the item already exists, raise an error message
        dpg.add_text("This item already exists!", pos=[28, 119], parent="new_item_window")
    else: # If the item doesn't already exist
        global pos2
        file = open("inventory.txt", "a") # Open the file in append mode
        file.write("\n" + name + "," + dpg.get_value("item_price") + "," + dpg.get_value("item_stock"))
        file.close()
        updateInventoryWindow()

def updateInventoryWindow():
    global pos2
    if dpg.does_item_exist("menuInv_window"):
        pos2 = dpg.get_item_pos("menuInv_window")  # Get the position of the Inventory window
        dpg.delete_item("menuInv_window")  # Close the window
        inventoryTab()  # Open the window again to update

def deleteItemButton():
    name = dpg.get_value("delete_name") # Get the name of the item to be deleted from the combobox
    temp = open("temp.txt", "w") # Open temp file for writing
    counter = 1
    for i in inv: # Loop through every item in inventory
        if(i.name != name): # If the name is different from the item to be deleted
            counter += 1
            temp.write(i.name + "," + str(i.price) + "," + str(i.stock)) # Write it in temp file
            if (counter < len(inv)): # Prevent empty line at the end
                temp.write("\n")
    temp.close() # Close the temp file
    temp = open("temp.txt", "r") # Open the temp file again for reading
    file = open("inventory.txt", "w") # Open the inventory file for writing
    lines = temp.readlines() # Read every line in the temp file
    for i in lines:
        file.write(i) # Write every line to the inventory file
    file.close() # Close the inventory file
    temp.close() # Close the temp file

    dpg.delete_item("delete_item_window") # Close the current window
    updateInventoryWindow() # Update the inventory window

revenue = [0.0, 0.0, 0.0]
def calculate_revenue():
    global revenue
    revenue = [0.0, 0.0, 0.0] # Daily profit, Weekly profit, Monthly profit
    curDay = int(datetime.datetime.now().strftime("%j")) # Get the current day of the year (1-365)
    curYear = int(datetime.datetime.now().strftime("%y")) # Get the current year
    file = open("profits.txt", "r")
    lines = file.readlines()
    for i in lines: # Loop through every line in profits file
        i = i.split(",") # Split the lines by ","
        profit = float(i[1]) # Get the profit data of the current line
        day = int(i[0].split("/")[0]) # Get the day of the current line
        year = int(i[0].split("/")[1]) # Get the year of the current line
        # If the year of the data equals current year and if the day of the data is not older than 30 days
        if(year == curYear and curDay - day >= 0 and curDay - day < 31):
            revenue[2] += profit # Add the current lines profit into monthly profit
            if(curDay - day <= 7):
                revenue[1] += profit # Add the current lines profit into weekly profit
                if(curDay - day == 0):
                    revenue[0] += profit # Add the current lines profit into daily profit

# Button for settling the bill
def billButton():
    year = datetime.datetime.now().strftime("%y") # Get the current year
    date = datetime.datetime.now().strftime("%j") # Get the currant day of the year (1-365)
    profit = tables[curTable()].calculateBill() # Calculate the profit for current table
    temp = open("temp2.txt", "w") # Open temp file for writing
    file = open("profits.txt", "r") # Open profits file for reading
    lines = file.readlines() # Read every line in the profits file
    counter = 0 # Counter for preventing empty line at the end of the file

    # If the latest date is different from current date
    firstLine = lines[0]
    if firstLine.split(",")[0].split("/")[0] != date or firstLine.split(",")[0].split("/")[1] != year:
        temp.write(date + "/" + year + "," + str(profit) + "\n") # Create a new line with current profit
    for i in lines: # Loop through every line ( day / year , profit )
        i = i.strip() # Clean the spaces
        counter += 1
        i = i.split(",") # Split the line by ","
        j = i[0].split("/") # Split the first part again by "/"
        if j[0] == date and j[1] == year: # If it is current day
            profit = float(i[1]) + profit # Add profits into current days profits
            temp.write(date + "/" + year + "," + str(profit)) # Write it
        else: # If its not current day
            temp.write(j[0] + "/" + j[1] + "," + i[1]) # Write it without changing
        if counter < len(lines): # Prevent empty line at the end
            temp.write("\n")
    temp.close() # Close the files
    file.close()

    temp = open("temp2.txt", "r") # Open the files again
    file = open("profits.txt", "w")
    lines = temp.readlines()
    for i in lines: # Transfer the datas in temp file to profits file
        file.write(i)
    file.close()
    temp.close()

    tables[curTable()].clearTable() # Clear the current table
    updateMenu() # Update the main window

# Tab for adding new item to the menu
def newItemTab():
    # Checking if this window already exist
    if dpg.does_item_exist("new_item_window"):
        dpg.delete_item("new_item_window")
    # Creating new window named "New Item" with size of 400x145 at 200, 200 position
    with dpg.window(label="New Item", width=400, height=145, pos=(200, 200),
                    tag="new_item_window", no_resize=True, no_collapse=True):
        # Product name input
        dpg.add_text("Name", pos=(28, 29))
        dpg.add_input_text(tag="item_name", width=150, pos=(78, 29))

        # Price input
        dpg.add_text("Price", pos=(28, 59))
        dpg.add_input_text(tag="item_price", width=150, pos=(78, 59))

        # Stock input
        dpg.add_text("Stock", pos=(28, 89))
        dpg.add_input_text(tag="item_stock", width=150, pos=(78, 89))

        # Add Item Button
        dpg.add_button(label="Add Item", width=130, height=80, pos=(250, 29), callback=addItemButton)

# Tab for deleting item from menu
def deleteItemTab():
    # Checking if this window already exist
    if dpg.does_item_exist("delete_item_window"):
        dpg.delete_item("delete_item_window")
    # Creating new window named "New Item" with size of 400x145 at 200, 200 position
    with dpg.window(label="Delete Item", width=400, height=95, pos=(200, 200),
                    tag="delete_item_window", no_resize=True, no_collapse=True):

        invNames = [i.name for i in inv]  # Create seperate list for product names in inv

        # Name input
        dpg.add_text("Name", pos=(28, 49))
        dpg.add_combo(invNames, tag="delete_name", width=150, pos=(78, 49))

        # Add Item Button
        dpg.add_button(label="Delete Item", width=130, height=60, pos=(250, 29), callback=deleteItemButton)

# Tab for editing items in the menu
def editItemTab():
    # Checking if this window already exist
    if dpg.does_item_exist("edit_window"):
        dpg.delete_item("edit_window")

    with dpg.window(label="Edit Item", width=500, height=160, pos=(200, 200),
                    tag="edit_window", no_resize=True, no_collapse=True):
        updateInventory()
        invNames = [i.name for i in inv]  # Create seperate list for product names in inv

        # Editing item input
        dpg.add_text("Editing Item", pos=(28, 49))
        dpg.add_combo(invNames, tag="edit_name", width=110, pos=(120, 49))

        # New name input
        dpg.add_text("New Name", pos=(250, 49))
        dpg.add_input_text(tag="edit_name_new", width=150, pos=(320, 49))

        # New Price input
        dpg.add_text("New Price", pos=(250, 79))
        dpg.add_input_text(tag="edit_price_new", width=150, pos=(320, 79))

        # New Stock input
        dpg.add_text("New Stock", pos=(250, 109))
        dpg.add_input_text(tag="edit_stock_new", width=150, pos=(320, 109))

        # Edit Item button
        dpg.add_button(label="Edit Item", width=202, height=50, pos=(28, 79), callback=editItemButton)

# Button for editing item
def editItemButton():
    name = dpg.get_value("edit_name") # Get the name of the item to be edited from combobox
    temp = open("temp.txt", "w")
    counter = 0
    for i in inv: # Loop through every item in inventory
        counter += 1
        if (i.name != name): # If current item is different from the item to be edited, write it as same
            temp.write(i.name + "," + str(i.price) + "," + str(i.stock))
        else: # If current item is the item to be edited, write it with its new values
            temp.write(dpg.get_value("edit_name_new") + "," + dpg.get_value("edit_price_new") + "," + dpg.get_value("edit_stock_new"))
        if (counter < len(inv)): # Prevent empty line at the end
            temp.write("\n")

    temp.close() # Close the file
    temp = open("temp.txt", "r") # Open the files again
    file = open("inventory.txt", "w")
    lines = temp.readlines()
    for i in lines: # Transfer the datas in temp file to inventory file
        file.write(i)
    file.close() # Close the files
    temp.close()

    dpg.delete_item("delete_item_window") # Close the current window
    updateInventoryWindow() # Update the inventory window

# Menu / Inventory Tab
def inventoryTab():
    # Checking if this window already exists
    if dpg.does_item_exist("menuInv_window"):
        dpg.delete_item("menuInv_window")

    # Setting the window label, width, height, position, tag and characteristics
    with dpg.window(label="Menu / Inventory", width=450, height=350, pos=pos2,
                    tag="menuInv_window", no_resize=True, no_collapse=True):

        dpg.add_text("Product", pos=[10, 25])
        dpg.add_text("Price", pos=[175, 25])
        dpg.add_text("Stock", pos=[250, 25])

        y = 50
        updateInventory()
        for i in inv: # Looping through items in inventory
            dpg.add_text(i.name, pos=[10, y])
            dpg.add_text(str(i.price) + "$", pos=[175, y])
            dpg.add_text(i.stock, pos=[250, y])
            y = y + 20 # Leaving 20 pixes space between each item

        # Buttons
        dpg.add_button(label="Edit Item", pos=[325, 25], height=100, width=100, callback=editItemTab)
        dpg.add_button(label="Delete Item", pos=[325, 130], height=100, width=100, callback=deleteItemTab)
        dpg.add_button(label="New Item", pos=[325, 235], height=100, width=100, callback=newItemTab)


# Tab for adding orders
def orderTab():
    # Checking if this window already exist
    if dpg.does_item_exist("add_order_window"):
        dpg.delete_item("add_order_window")

    with dpg.window(label="Add Order", width=400, height=158, pos=pos3,
                    tag="add_order_window", no_resize=True, no_collapse=True):

        updateInventory()
        invNames = [i.name for i in inv] # Create seperate list for product names in inv

        # Name input
        dpg.add_text("Name", pos=(28, 49))
        dpg.add_combo(invNames, tag="order_name", width=150, pos=(78, 49), default_value=invNames[0])

        # Size input
        dpg.add_text("Size", pos=(28, 79))
        dpg.add_combo(("Small", "Medium (+2$)", "Large (+3$)"), tag="order_size", width=150, pos=(78, 79), default_value="Small")

        # Type input
        dpg.add_text("Type", pos=(28, 109))
        dpg.add_combo(("Hot", "Iced"), tag="order_type", width=150, pos=(78, 109), default_value="Hot")

        # Add Order button
        dpg.add_button(label="Add Order", width=130, height=80, pos=(250, 49), callback=orderButton)

selectedTable = "Table 1"
# Callback method when new table is selected
def tableChange():
    global selectedTable
    selectedTable = dpg.get_value("table_combo")
    updateMenu()

pos = (0, 0) # Window position
# Updating menu with deleting the window and creating a new one at the same position
def updateMenu():
    global pos
    pos = dpg.get_item_pos("main_window")
    dpg.delete_item("main_window")
    draw_menu()

inv = [] # List for storing inventory data
def updateInventory():
    inv.clear() # Clear the previous data
    file = open("inventory.txt", "r")
    lines = file.readlines()
    for i in lines: # Loop through lines in inventory file
        i.strip() # Clear the spaces
        j = i.split(",") # Split the line by ","
        toAdd = product(float(j[1]), j[0], int(j[2]))
        inv.append(toAdd)
    file.close()

# Main menu
def draw_menu():

    with dpg.window(label="Book Cafe", width=900, height=400, tag="main_window", pos=pos, no_resize=True):
        dpg.add_image("bg_tex", pos=(0,0), width=900, height=400)
        # Table selection
        global selectedTable
        dpg.add_text("Table:", pos=[16, 43])
        dpg.add_combo(["Table 1", "Table 2", "Table 3", "Table 4", "Table 5"], default_value=selectedTable, width=150, pos=[64, 41], tag="table_combo", callback=tableChange)
        cT = int((selectedTable.replace("Table ", ""))) - 1 # Current table index

        # Orders list
        dpg.add_text("Orders:", pos=[16, 120])
        for i in range(0,tables[cT].drinkCount):
            dpg.add_text(tables[cT].drinks[i].getDrink(), pos=[70, 120 + (20 * i)]) # Printing each element with 20 pixels space

        # Books list
        dpg.add_text("Books:", pos=[300, 120])
        for i in range(0, tables[cT].bookCount):
            dpg.add_text(tables[cT].books[i].getBook(), pos=[350, 120 + (20 * i)]) # Printing each element with 20 pixels space

        # Current Bill
        dpg.add_text("Current Bill:", pos=[300, 43])
        dpg.add_text(" $" + str(tables[cT].calculateBill()), pos=[390, 43])

        # Buttons
        dpg.add_button(label="Add Order", width=275, height=30, pos=[16, 78], callback=orderTab)
        dpg.add_button(label="Add Book", width=275, height=30, pos=[300, 78], callback=bookTab)
        dpg.add_button(label="Settle Bill", width=126, height=25, pos=[449, 37], callback=billButton)
        dpg.add_button(label="Menu / Inventory", width=280, height=71, pos=[600, 37], callback=inventoryTab)

        # Profits
        calculate_revenue()
        dpg.add_text("Daily   Revenue  : $" + str(revenue[0]), pos=[600, 330])
        dpg.add_text("Weekly  Revenue  : $" + str(revenue[1]), pos=[600, 350])
        dpg.add_text("Monthly Revenue  : $" + str(revenue[2]), pos=[600, 370])

        # Seperating line
        dpg.draw_line((580, 0), (580, 400))


if __name__ == "__main__":
    t1 = table(1)
    t2 = table(2)
    t3 = table(3)
    t4 = table(4)
    t5 = table(5)
    tables = [t1, t2, t3, t4, t5]

    # Dear PyGui methods
    dpg.create_context()
    with dpg.texture_registry():
        width, height, channels, data = dpg.load_image("Dirt_background.png")
        dpg.add_static_texture(width, height, data, tag="bg_tex")
    init_style()
    draw_menu()
    dpg.bind_theme("custom_theme")
    dpg.create_viewport(title='Cafe System', width=1200, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
