from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list += [choice(letters) for char in range(9)]
    password_list += [choice(symbols) for char in range(3)]
    password_list += [choice(numbers) for char in range(3)]

    shuffle(password_list)

    password = "".join(password_list[:length_slider.get()])

    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)


def add_password():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {website: {
        "email": username,
        "password": password
    }}

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Adding failed", message="You can't have any empty fields")
    else:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("passwords.json", "w") as file:
                json.dump(new_data, fp=file, indent=4)
        else:
            data.update(new_data)
            with open("passwords.json", "w") as file:
                json.dump(data, fp=file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


def search():
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
            website = website_input.get()
    except FileNotFoundError:
        messagebox.showerror("Searching failed", "No Data File Found")
    except json.decoder.JSONDecodeError:
        messagebox.showerror("Searching failed", "No details for the website exists")
    else:
        if website in data:
            messagebox.showinfo("Website found", f"Email: {data[website]['email']}\n"
                                                 f"Password: {data[website]['password']}")
        else:
            messagebox.showerror("Searching failed", "No details for the website exists")


screen = Tk()
screen.title("Password Manager")
screen.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website = Label(text="Website: ")
website.grid(column=0, row=1)

username = Label(text="Email/Username: ")
username.grid(column=0, row=2, sticky="EW")

password = Label(text="Password:")
password.grid(column=0, row=3)

website_input = Entry()
website_input.focus()
website_input.grid(column=1, row=1, sticky="EW")

username_input = Entry()
username_input.insert(0, "your_mail@mail.com")
username_input.grid(column=1, row=2, columnspan=2, sticky="EW")

password_input = Entry()
password_input.grid(column=1, row=3, sticky="EW")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", width=36, command=add_password)
add_button.grid(column=1, row=4, sticky="EW")

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="EW")

length_slider = Scale(from_=5, to=15)
length_slider.grid(column=2, row=4)


screen.mainloop()