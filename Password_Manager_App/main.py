from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # password_list = []
    #
    # for char in range(nr_letters):
    #     password_list.append(random.choice(letters))
    #
    # for char in range(nr_symbols):
    #     password_list += random.choice(symbols)
    #
    # for char in range(nr_numbers):
    #     password_list += random.choice(numbers)

    password_list = [random.choice(letters) for char in range(nr_letters)]

    password_list += [random.choice(symbols) for char in range(nr_symbols)]

    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    # password = ""
    # for char in password_list:
    #     password += char
    #
    password = "".join(password_list)
    # print(f"Your password is: {password}")
    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading the old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating the old data with new data
            data.update(new_data)

            with open("data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH BUTTON ------------------------------- #


def search():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    try:
        with open("data.json", mode="r") as data_file:
            # Reading the old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        for (key, value) in data.items():
            if website == key:
                messagebox.showinfo(title=website, message=f"Email: {value['email']}\nPassword: {value['password']}")
            elif website == "":
                messagebox.showinfo(title="Error", message=f"Yaz bir sey mk. Nasıl search yapayim!")
            else:
                messagebox.showinfo(title="Error", message="No details for the website exists.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "angela@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="EW")
add_button = Button(text="Add", width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")
search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()



def find_password():
    website = website_entry.get()
    with open("data.json") as data_file:
        data = json.load(data_file)
        if website in data:
            email = data[website]['email']
            password = data[website]['password']