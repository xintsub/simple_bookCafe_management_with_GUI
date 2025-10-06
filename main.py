import dearpygui.dearpygui as dpg

class product:
    def __init__(self, price, name):
        self.price = price
        self.name = name

class drink(product):
    def __init__(self, price, name, size, type):
        super().__init__(price, name)
        self.size = size
        self.type = type
    def getDrink(self):
        return self.name + " - " + self.size + " - " + self.type

class book(product):
    def __init__(self, price, name, author):
        super().__init__(price, name)
        self.author = author
    def getBook(self):
        return self.name + " - " + self.author

class table:
    def __init__(self, number):
        self.number = number
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
            self.totalBill += int(sum(i.price for i in self.books))
        if self.drinkCount != 0:
            self.totalBill += int(sum(i.price for i in self.drinks))
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
    willAdd = book(int(dpg.get_value("book_price")), dpg.get_value("book_name"), dpg.get_value("book_author"))
    tables[curTable()].addBook(willAdd)
    updateMenu()

# Button for adding orders
def orderButton():
    willAdd = drink(int(dpg.get_value("order_price")), dpg.get_value("order_name"), dpg.get_value("order_size"), dpg.get_value("order_type"))
    tables[curTable()].addDrink(willAdd)
    updateMenu()

# Button for settling the bill
def billButton():
    tables[curTable()].clearTable()
    updateMenu()

# Tab for adding orders
def orderTab():
    # Checking if this window already exist
    if dpg.does_item_exist("add_order_window"):
        dpg.delete_item("add_order_window")

    with dpg.window(label="Add Order", width=400, height=175, pos=(200, 200),
                    tag="add_order_window", no_resize=True, no_collapse=True):
        # Name input
        dpg.add_text("Name", pos=(28, 49))
        dpg.add_input_text(tag="order_name", width=150, pos=(78, 49))

        # Size input
        dpg.add_text("Size", pos=(28, 79))
        dpg.add_combo(("Small", "Medium", "Large"), tag="order_size", width=150, pos=(78, 79))

        # Type input
        dpg.add_text("Type", pos=(28, 109))
        dpg.add_combo(("Iced", "Hot"), tag="order_type", width=150, pos=(78, 109))

        # Price input
        dpg.add_text("Price", pos=(28, 139))
        dpg.add_input_text(tag="order_price", width=150, pos=(78, 139))

        # Add Order button
        dpg.add_button(label="Add Order", width=130, height=110, pos=(250, 49), callback=orderButton)

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


# Main menu
def draw_menu():

    with dpg.window(label="Book Cafe", width=600, height=400, tag="main_window", pos=pos, no_resize=True):
        dpg.add_image("bg_tex", pos=(0,0))
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
        dpg.add_text("$" + str(tables[cT].calculateBill()), pos=[390, 43])

        # Buttons
        dpg.add_button(label="Add Order", width=275, height=30, pos=[16, 78], callback=orderTab)
        dpg.add_button(label="Add Book", width=275, height=30, pos=[300, 78], callback=bookTab)
        dpg.add_button(label="Settle Bill", width=146, height=25, pos=[429, 37], callback=billButton)


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
    dpg.create_viewport(title='Cafe System', width=640, height=480)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
