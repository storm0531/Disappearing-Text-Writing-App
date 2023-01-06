from tkinter import *

#constants
BG_COLOR = "skyblue"
BG_LOSE_COLOR = "#9A1663"
timer_sec = 60
timer_min = 4
past_word_count = 0
color_thickness = 0
continue_id = ""
stop_timer = False


def start_game():
    #reset game for reuse
    global timer_sec,timer_min,stop_timer,past_word_count
    timer_sec = 60
    timer_min = 4
    past_word_count = 0
    stop_timer = False

    start_label.config(text="click to end")
    start_button.config(text="end game",command=end_game)
    
    text_box.config(state="normal",fg="black")
    text_box.delete("1.0",END)
    text_box.focus()

    set_typing()
    game_running()

def game_running():
    global continue_id,stop_timer
    
    check_typing()
    run_timer()
    
    #if user reaches 5min count down without stoping over 4 seconds user win
    if timer_min == 0 and timer_sec == 0:
        stop_timer = True
        end_game()
        end_popup(font_color="#FED049",
                  bg_color="#68B984",
                  title="you win",
                  end_results=f"you win with {past_word_count} words wrote \n"
                  f",and for finishing continuously \n"
                  f"write for 5 Minutes,congratulations")
        
    #continue tile either user win the contest or lose the contest
    if not stop_timer:
        continue_id = window.after(1000, game_running)
    else:
        window.after_cancel(continue_id)
        
def run_timer():
    global timer_sec, timer_min
    
    # reduce 1 second from time remaining
    timer_sec -= 1
    if timer_sec < 10:
        sec = f"0{timer_sec}"
    else:
        sec = timer_sec
    if timer_sec < 0:
        timer_sec = 59
        sec = f"0{timer_sec}"
        timer_min -= 1
    timer.config(text=f"{timer_min}:{sec}")

def check_typing():
    #check if user is still typing and if stoped it will indicate by color of window
    #and if stoped typing over 5 sec then it will end the game
    global past_word_count,color_thickness
    
    #get length of all words writen by user
    new_word_count = len(text_box.get("1.0",END))
    
    #if user stop typing 
    if new_word_count == past_word_count:
        color_thickness += 1
        if color_thickness == 1:
            text_box.config(bg="#FF97C1")
        elif color_thickness == 2:
            text_box.config(bg="#FF5858")
        elif color_thickness == 3:
            canvas.config(bg="#F49D1A")
        elif color_thickness == 4:
            canvas.config(bg="#93ABD3")
        else:
            end_game()
            remaining_time = f"{4 - timer_min} min ,{60 - timer_sec} sec"
            end_popup(font_color="#EEEEEE",
                      bg_color="#EB455F",
                      title="yoy lost", 
                      end_results=f"you lost with {past_word_count} words wrote \n"
                                  f",and for not typing continued at\n"
                                  f"{remaining_time} elapsed time")
    else:
        #user still typing or continue typing
        color_thickness = 0
        set_typing()
        past_word_count = new_word_count

def set_typing():
    window.config(bg=BG_COLOR)
    start_label.config(bg=BG_COLOR)
    timer_label.config(bg=BG_COLOR)
    timer.config(bg=BG_COLOR)
    canvas.config(bg="green")
    text_box.config(bg="#FDF1D6")

def end_game():
    global stop_timer
    window.config(bg=BG_LOSE_COLOR)
    start_label.config(bg=BG_LOSE_COLOR)
    timer_label.config(bg=BG_LOSE_COLOR)
    timer.config(bg=BG_LOSE_COLOR)
    text_box.config(state="disabled",fg="white")
    start_label.config(text="click to restart")
    start_button.config(text="retry",command=start_game)
    stop_timer = True

def end_popup(font_color,bg_color,title,end_results):
    popup = Toplevel()
    popup.minsize(200,50)
    popup.title(title)
    popup.config(padx=20,pady=10,bg=bg_color)

    results = Label(popup,text=end_results, font=('arial 18 bold'),bg=bg_color,fg=font_color)
    results.grid(column=0,row=0,columnspan=1,rowspan=1)

# ------------------- graphical user interface(GUI) -----------------# 
window = Tk()
window.title("most dangerous typing game")
window.minsize(600,400)
window.config(pady=50,padx=50,highlightthickness=0,bg=BG_COLOR)

timer_label = Label(text="time remaining:",font=("arial",25,"bold"),fg="red",bg=BG_COLOR)
timer_label.grid(column=0,row=0)

timer = Label(text="5:00",font=("arial",25,"bold"),fg="red",bg=BG_COLOR)
timer.grid(column=1,row=0)

start_label = Label(text="click to start:" ,font=("arial",25,"bold"),fg="green",bg=BG_COLOR)
start_label.grid(column=0,row=1)

start_button = Button(text="START",width=30,bg="green",padx=30,pady=10,command=start_game)
start_button.grid(column=1,row=1,columnspan=2)

canvas = Canvas(width=600,height=300,bg="green",highlightthickness=0)
text_box = Text(width=38,height=8,font=("arial",20,"bold"),bg="yellow",highlightthickness=0,state="disabled")
canvas_window = canvas.create_window(300,150,window=text_box)
canvas.grid(column=0,row=2,columnspan=2,pady=20)


mainloop()
