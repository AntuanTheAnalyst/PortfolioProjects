from tkinter import *
from tkinter import messagebox
import pandas
import random
import time


last_length = 0
TIME_LIMIT = 60
time_left = TIME_LIMIT
timer_running = False

correct_chars = 0
start_time = None

window = Tk()
window.title('Typing Speed Test')
window.minsize(width=800, height=600)
window.config(padx=15, pady=15)

window.columnconfigure(2, weight=1)


def calculate_accuracy():
    typed_length = len(typing_entry.get())
    if typed_length == 0:
        return 0
    return (correct_chars / typed_length) * 100


def generate_sentences(n=12):

    with open("data/random_english_sentences.txt", "r", encoding="utf-8") as file:
        sentences = [line.strip() for line in file if line.strip()]

    chosen = random.sample(sentences, n)

    return " ".join(chosen)


Label(window, text='WPM').grid(row=0, column=3, padx=5)
wpm_value_label = Label(window, text="0")
wpm_value_label.grid(row=0, column=4, padx=5)

Label(window, text='Time left:').grid(row=0, column=5, padx=5)
time_label = Label(window, text=str(TIME_LIMIT))
time_label.grid(row=0, column=6, padx=5)


def restart_test():
    global test_text, last_length, correct_chars
    global time_left, timer_running, start_time


    last_length = 0
    correct_chars = 0
    timer_running = False
    start_time = None
    time_left = TIME_LIMIT

    time_label.config(text=str(TIME_LIMIT))
    wpm_value_label.config(text="0")

    typing_entry.config(state="normal")
    typing_entry.delete(0, END)
    typing_entry.focus()

    text_display.config(state="normal")
    text_display.delete("1.0", END)

    test_text = generate_sentences()
    text_display.insert("1.0", test_text)

    text_display.tag_remove("correct", "1.0", END)
    text_display.tag_remove("wrong", "1.0", END)
    text_display.config(state="disabled")

    typing_entry.focus_set()


Button(window, text='Restart', command=restart_test).grid(row=0, column=7, padx=5)


text_display = Text(window, height=6, wrap="word", font=("Arial", 14), padx=10, pady=10)
text_display.grid(row=1, column=0, columnspan=8, pady=(20, 10), sticky="ew")
text_display.tag_config("correct", background="#c8f7c5")
text_display.tag_config("wrong", background="#f7c5c5")


test_text = generate_sentences()
text_display.insert("1.0", test_text)

text_display.config(state='disabled')

typing_entry = Entry(
    window,
    font=("Arial", 14)
)


def countdown():
    global time_left

    if not timer_running:
        return

    if time_left > 0:
        time_left -= 1
        time_label.config(text=str(time_left))
        window.after(1000, countdown)
    else:
        end_test()


def on_key_release(event):
    global timer_running
    global last_length
    global start_time
    global correct_chars

    if time_left <= 0:
        return

    if not timer_running and event.keysym != "BackSpace":
        timer_running = True
        start_time = time.time()
        window.after(1000, countdown)

    if event.keysym == "BackSpace":
        handle_backspace()
        update_wpm()
        return

    typed_text = typing_entry.get()
    current_length = len(typed_text)

    if current_length > len(test_text):
        return

    for index in range(last_length, current_length):
        typed_char = typed_text[index]
        target_char = test_text[index]

        start = f"1.{index}"
        end = f"1.{index + 1}"

        text_display.config(state="normal")

        if typed_char == target_char:
            text_display.tag_add("correct", start, end)
            text_display.tag_remove("wrong", start, end)
            correct_chars += 1
        else:
            text_display.tag_add("wrong", start, end)
            text_display.tag_remove("correct", start, end)

        text_display.config(state="disabled")

    update_wpm()
    last_length = current_length


def update_wpm():
    if not start_time:
        return

    elapsed_seconds = time.time() - start_time
    elapsed_minutes = elapsed_seconds / 60

    if elapsed_minutes == 0:
        return

    wpm = (correct_chars / 5) / elapsed_minutes
    wpm_value_label.config(text=str(int(wpm)))


def end_test():
    typing_entry.config(state="disabled")
    update_wpm()

    wpm = wpm_value_label.cget("text")
    accuracy = calculate_accuracy()

    messagebox.showinfo(
        title="Typing Test Finished 🏁",
        message=(
            f"⏱ Time: {TIME_LIMIT} seconds\n"
            f"⌨️ WPM: {wpm}\n"
            f"🎯 Accuracy: {accuracy:.1f}%"
        )
    )


def handle_backspace():
    global last_length, correct_chars

    current_text = typing_entry.get()
    current_length = len(current_text)

    text_display.config(state="normal")

    for i in range(current_length, last_length):
        start = f"1.{i}"
        end = f"1.{i+1}"

        if "correct" in text_display.tag_names(start):
            correct_chars -= 1

        text_display.tag_remove("correct", start, end)
        text_display.tag_remove("wrong", start, end)

    text_display.config(state="disabled")

    last_length = current_length


typing_entry.grid(row=2, column=0, columnspan=8, sticky="ew")
typing_entry.focus()
typing_entry.bind('<KeyRelease>', on_key_release)

window.mainloop()

