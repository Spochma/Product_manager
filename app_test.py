import sqlite3
from tkinter import ttk
from tkinter import *


class Product:
    # Attn:. To access the database you must put its absolute path in the code.
    # Exemple: db = 'abolute path of database'
    db = '/database/products'

    def __init__(self, root):
        self.window = root
        self.window.title("Product manager app")
        self.window.resizable(1, 1)
        # self.window.wm_iconbitmap('sources/icon.ico')
        self.window.geometry("400x635")

        frame = LabelFrame(self.window, text="Register new product", font=('calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        self.label_name = Label(frame, text="Name: ", font=('calibri', 13))
        self.label_name.grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        self.label_price = Label(frame, text="Price: ", font=('calibri', 13))
        self.label_price.grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.focus()
        self.price.grid(row=2, column=1)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.table = ttk.Treeview(height=20, columns=str(2), style="mystyle.Treeview")
        self.table.grid(row=4, column=0, columnspan=2)
        self.table.heading('#0', text='Name', anchor=CENTER)
        self.table.heading('#1', text='Price', anchor=CENTER)

        s = ttk.Style()
        s.configure('my.TButton', font=('calibri', 14, 'bold'))

        self.delete_button = ttk.Button(text='Delete', style='my.TButton', command=self.del_product)
        self.delete_button.grid(row=5, column=0, sticky=W + E)

        self.edit_button = ttk.Button(text='Edit', style='my.TButton', command=self.edit_products)
        self.edit_button.grid(row=5, column=1, sticky=W + E)

        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        self.add_button = ttk.Button(frame, text="Save product", style='my.TButton', command=self.add_product)
        self.add_button.grid(row=4, columnspan=2, sticky=W + E)

    def db_check(self, check, parameter=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            result = cursor.execute(check, parameter)
            con.commit()
        return result

    def get_products(self):
        # if you have old residual data when starting the app, it will be cleaned.
        table_record = self.table.get_children()
        for line in table_record:
            self.table.delete(line)

        # Check the database
        query = 'SELECT * FROM product ORDER BY name DESC'
        record = self.db_check(query)

        for line in record:
            print(line)
            self.table.insert('', 0, text=line[1], values=line[2])

    def check_name(self):
        nameinput = self.name.get()
        return len(nameinput) != 0

    def check_price(self):
        priceinput = self.price.get()
        return len(priceinput) != 0

    def add_product(self):
        if self.check_name() and self.check_price():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'  # consulta SQL (sem os dados)

            parameter = (self.name.get(), self.price.get())  # Parametros da consulta SQL

            self.db_check(query, parameter)
            self.message['text'] = f'Product {self.name.get()} saved with success'
            self.name.delete(0, END)
            self.price.delete(0, END)

            # Para debug
            # print(self.name.get())
            # print(self.price.get())

        elif self.check_name() and self.check_price() == False:
            print("Price is mandatory")
            self.message['text'] = f'Price is mandatory!'

        elif self.check_name() == False and self.check_price():
            print("Name is mandatory")
            self.message['text'] = f'Name is mandatory'
        else:
            print("Name and price is mandatory!")
            self.message['text'] = f'Name and price is mandatory'

        self.get_products()

    def del_product(self):
        # Debug
        # print(self.table.item(self.table.selection()))
        # print(self.table.item(self.table.selection())['text'])
        # print(self.table.item(self.table.selection())['values'])
        # print(self.table.item(self.table.selection())['values'][0])

        self.message['text'] = ''
        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'PLease, select one product.'
            return

        self.message['text'] = ''
        name = self.table.item(self.table.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.db_check(query, (name,))
        self.message['text'] = f'Product {name} deleted with success!'
        self.get_products()

    def edit_products(self):
        self.message['text'] = ''
        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select one product.'
            return

        name = self.table.item(self.table.selection())['text']
        old_price = self.table.item(self.table.selection())['values'][0]

        self.edit_window = Toplevel()
        self.edit_window.title = 'Edit product.'
        self.edit_window.resizable(1, 1)
        # self.edit_window.wm_iconbitmap('sources/icon.ico')

        title = Label(self.edit_window, text='Edit products', font=('Calibri', 50, 'bold'))
        title.grid(column=0, row=0)

        frame_ep = LabelFrame(self.edit_window, text='Edit the product', font=('calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label old name
        self.old_name = Label(frame_ep, text='Old name: ', font=('calibri', 13))
        self.old_name.grid(row=2, column=0)
        self.input_old_name = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=name), state='readonly',
                                    font=('calibri', 13))

        self.input_old_name.grid(row=2, column=1)

        # Label new name
        self.input_new_name = Label(frame_ep, text='New name: ', font=('calibri', 13))
        self.input_new_name.grid(row=3, column=0)

        self.input_new_name = Entry(frame_ep, text='New name: ', font=('calibri', 13))
        self.input_new_name.grid(row=3, column=1)
        self.input_new_name.focus()

        # old price
        self.old_price = Label(frame_ep, text='Old price: ', font=('calibri', 13))
        self.old_price.grid(row=4, column=0)

        self.input_old_price = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=old_price),
                                     state='readonly', font=('calibri', 13))
        self.input_old_price.grid(row=4, column=1)

        # Label new price
        self.new_price = Label(frame_ep, text='New price: ', font=('calibri', 13))
        self.new_price.grid(row=5, column=0)

        self.input_new_price = Entry(frame_ep, font=('calibri', 13))
        self.input_new_price.grid(row=5, column=1)

        # Button for update
        s = ttk.Style()
        s.configure('my.TButton', font=('calibri', 14, 'bold'))
        self.update_button = ttk.Button(frame_ep, text='Update product', style='my.TButton', command=lambda:
        self.update_products(self.input_new_name.get(), self.input_old_name.get(), self.input_new_price.get(),
                             self.input_old_price.get()))

        self.update_button.grid(row=6, columnspan=2, sticky=W + E)

    def update_products(self, new_name, old_name, new_price, old_price):
        modify_product = False
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'

        if new_name != '' and new_price != '':
            # update name and price
            parameter = (new_name, new_price, old_name, old_price)
            modify_product = True

        elif new_name != '' and new_price == '':
            # Update only name, if the space for a new price was empty.
            parameter = (new_name, old_price, old_name, old_price)
            modify_product = True

        elif new_name == '' and new_price != '':
            # Update only price, if the space for a new name was empty.
            parameter = (old_name, new_price, old_name, old_price)
            modify_product = True

        if (modify_product):
            self.db_check(query, parameter)
            self.edit_window.destroy()
            self.message['text'] = f'The product {old_name} was updated with success'
            self.get_products()
        else:
            self.edit_window.destroy()
            self.message['text'] = f"The product {old_name}, wasn't updated"

    # font=('calibri', 13)

if __name__ == '__main__':
    root = Tk()  # Main window instance
    app = Product(root)  # Control over the window root is sent to the Product class
    root.mainloop()  # We start the application cycle, it's like a while True
