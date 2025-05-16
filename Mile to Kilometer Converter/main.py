from tkinter import *


def miles_to_km_converter():
    converted_num = round(float(input.get()) * 1.60934)  # Miles to Km.
    converter.config(text=converted_num)


window = Tk()
window.title('Mile to Km Converter')
window.minsize(width=80, height=50)
window.config(padx=100, pady=50)

# Entry_input
input = Entry(width=10, font=('Times New Roman', 12, 'normal'))
input.grid(column=1, row=0)

# Miles_Label
miles = Label(text="Miles", font=('Times New Roman', 20, 'normal'))
miles.grid(column=2, row=0)
miles.config(padx=10, pady=10)

# Is_Equal_Label
is_equal = Label(text="is equal to", font=('Times New Roman', 20, 'normal'))
is_equal.grid(column=0, row=1)

# Converter_label
converter = Label(text=0, font=('Times New Roman', 20, 'normal'))
converter.grid(column=1, row=1)
# converter.config(padx=7, pady=7)

# Km_Label2
km = Label(text="Km", font=('Times New Roman', 20, 'normal'))
km.grid(column=2, row=1)
km.config(padx=10, pady=10)

# Calculate_button
calculate = Button(text='Calculate', command=miles_to_km_converter)
calculate.grid(column=1, row=2)
calculate.config(padx=7, pady=7)


window.mainloop()
