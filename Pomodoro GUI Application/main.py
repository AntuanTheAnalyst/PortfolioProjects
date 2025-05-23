from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
check_mark_text = ""
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer
    if timer is not None:
        window.after_cancel(timer)
        timer = None # Reset timer variable
        
    # timer_text = 00:00
    canvas.itemconfigure(timer_text, text="00:00")
    reps = 1
    # title_label = "Timer"
    timer_label.config(text="Timer", fg=GREEN)
    # reset check_marks
    check_marks.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, timer
    if timer is not None:
        return # Prevent starting a new timer if one is already running

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # if it's the 1st/3rd/5th/7th rep:
    if reps % 2 == 1 and reps < 9:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)
    # if it's the 8th rep:
    elif reps == 8:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    # if it's the second/fourth/sixth rep:
    elif reps % 2 == 0 and reps < 9:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
        # check_marks.config(text=check_mark_text)
        # check_mark_text += "✔"

    reps += 1

    if reps >= 9:
        print("Cycle completed! Restarting...")
        reps = 1  # Reset reps to restart the timer


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global check_mark_text
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    print(count)
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Pomodoro')
window.config(padx=100, pady=100, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_ing = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_ing)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(column=1, row=1)

timer_label = Label(text="Timer", font=(FONT_NAME, 50, "bold"), fg=GREEN, bg=YELLOW, highlightthickness=0)
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW, highlightthickness=0)
check_marks.grid(column=1, row=3)

window.mainloop()
