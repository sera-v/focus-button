import customtkinter as ctk
import json
import os
import sys
import threading
import time
import tkinter as tk
import webbrowser

# mac app setup
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

json_path = os.path.join(base_path, "links.json")


def load_links():
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)
    return []


class FocusButton:
    def __init__(self, root):
        self.root = root
        self.timer_stopped = False
        self.timer_running = False
        self.timer_paused = False
        self.timer_duration = 25
        self.pages_open = False
        self.urls = load_links()
        self.pop = None
        self.duration_entry = None
        self.listbox = None
        self.setup_gui()

    def setup_gui(self):
        self.root.title("focus button")
        self.root.geometry("400x200")
        self.root.configure(bg="#f9f9f9")

        self.countdown_label = tk.Label(
            self.root,
            text=f"{self.format_time(self.timer_duration)}:00",
            font=("Helvetica", 36),
            width=10,
            height=2,
            anchor="center",
            fg="#5c5c5c",
            bg="#f9f9f9",
            bd=2,
        )

        self.focus = ctk.CTkButton(
            self.root,
            text="focus",
            command=self.start_focus,
            width=150,
            height=60,
            corner_radius=35,
            border_width=2,
            fg_color="#5AA9E6",
            hover_color="#83BFEC",
            text_color="#f9f9f9",
            border_color="#f9f9f9",
            font=("Helvetica", 28),
        )
        self.focus.place(relx=0.5, rely=0.35, anchor="center")

        self.settings = ctk.CTkButton(
            self.root,
            text="settings",
            command=self.timer_settings,
            width=60,
            height=35,
            corner_radius=35,
            border_width=2,
            fg_color="#E7E6EA",
            hover_color="#F4F4F6",
            border_color="#f9f9f9",
            text_color="#5c5c5c",
            font=("Helvetica", 14),
        )
        self.settings.place(relx=0.5, rely=0.65, anchor="center")

        self.play = ctk.CTkButton(
            self.root,
            text="play",
            command=self.resume_focus,
            width=80,
            height=35,
            corner_radius=35,
            border_width=2,
            fg_color="#5AA9E6",
            hover_color="#83BFEC",
            border_color="#F9F9F9",
            text_color="#F9F9F9",
            font=("Helvetica", 14),
        )

        self.pause = ctk.CTkButton(
            self.root,
            text="pause",
            command=self.pause_focus,
            width=80,
            height=35,
            corner_radius=35,
            border_width=2,
            fg_color="#5AA9E6",
            hover_color="#83BFEC",
            border_color="#F9F9F9",
            text_color="#F9F9F9",
            font=("Helvetica", 14),
        )

        self.stop = ctk.CTkButton(
            self.root,
            text="stop",
            command=self.stop_focus,
            width=80,
            height=35,
            corner_radius=35,
            border_width=2,
            fg_color="#5AA9E6",
            hover_color="#83BFEC",
            border_color="#F9F9F9",
            text_color="#F9F9F9",
            font=("Helvetica", 14),
        )

        self.finished_label = tk.Label(self.root, text="", font=("Helvetica", 12))

    def open_pages(self, urls):
        for url in urls:
            webbrowser.open_new_tab(url)

    def pomo_timer(self, duration):
        time_pom = duration * 60
        self.timer_running = True
        while time_pom >= 0 and not self.timer_stopped:
            if not self.timer_paused:
                mins, secs = divmod(time_pom, 60)
                timer_text = "{:02d}:{:02d}".format(mins, secs)
                self.countdown_label.config(text=timer_text)
                time.sleep(1)
                time_pom -= 1
            else:
                time.sleep(0.1)
        if not self.timer_stopped and time_pom < 0:
            os.system("afplay 'alarm_sound.wav' &")
            time.sleep(4)

        # cleanup
        self.timer_running = False
        self.countdown_label.place_forget()
        self.focus.place(relx=0.5, rely=0.35, anchor="center")
        self.play.place_forget()
        self.pause.place_forget()
        self.stop.place_forget()
        self.settings.place(relx=0.5, rely=0.65, anchor="center")

    def start_focus(self):
        if self.timer_running:
            return

        # cleanup prev runs
        self.timer_stopped = False
        self.timer_paused = False
        self.timer_running = True
        self.finished_label.config(text=" ")

        self.focus.place_forget()
        self.countdown_label.place(relx=0.5, rely=0.35, anchor="center")

        # hide settings
        self.settings.place_forget()
        # replace btns
        self.play.place(relx=0.25, rely=0.65, anchor="center")
        self.pause.place(relx=0.5, rely=0.65, anchor="center")
        self.stop.place(relx=0.75, rely=0.65, anchor="center")

        if not self.pages_open and self.urls:
            self.open_pages(self.urls)
            self.pages_open = True

        threading.Thread(
            target=self.pomo_timer, args=(self.timer_duration,), daemon=True
        ).start()

    def stop_focus(self):
        self.timer_stopped = True
        self.timer_running = False
        self.countdown_label.config(text=f"{self.format_time(self.timer_duration)}:00")
        self.finished_label.config(text=" ")
        self.settings.place(relx=0.5, rely=0.65, anchor="center")
        print("timer stopped")

    def pause_focus(self):
        self.timer_paused = True

    def resume_focus(self):
        self.timer_paused = False

    def timer_settings(self):
        # there can only be 1
        if self.pop and self.pop.winfo_exists():
            self.pop.lift()
            return

        self.pop = tk.Toplevel(self.root)
        self.pop.geometry("350x400")
        self.pop.title("settings")

        tk.Label(self.pop, text="🕐", font=("Helvetica", 12)).place(
            x=60, y=40, anchor="w"
        )

        options = [
            "5",
            "10",
            "15",
            "20",
            "25",
            "30",
            "35",
            "40",
            "45",
            "50",
            "55",
            "60",
        ]
        self.duration_entry = tk.StringVar(value=options[4])
        dropdown = tk.OptionMenu(self.pop, self.duration_entry, *options)
        dropdown.place(x=90, y=40, anchor="w")
        tk.Label(self.pop, text="minutes", font=("Helvetica", 12)).place(
            x=150, y=40, anchor="w"
        )

        tk.Label(self.pop, text="🔗", font=("Helvetica", 12)).place(
            x=60, y=90, anchor="w"
        )
        link_entry = tk.Entry(self.pop, width=21)
        link_entry.place(x=90, y=90, anchor="w")

        tk.Button(
            self.pop,
            text="+",
            width=1,
            height=1,
            command=lambda: self.append_links(link_entry),
        ).place(x=140, y=130, anchor="w")

        tk.Button(self.pop, text="-", width=1, height=1, command=self.pop_links).place(
            x=190, y=130, anchor="w"
        )

        self.listbox = tk.Listbox(self.pop, height=4)
        for link in self.urls:
            self.listbox.insert(tk.END, link)
        self.listbox.place(x=90, y=170, width=200, height=150)

        tk.Button(self.pop, text="save", width=6, command=self.save_settings).place(
            x=180, y=370, anchor="s"
        )

    def save_settings(self):
        try:
            new_duration = int(self.duration_entry.get())
            if new_duration > 0 and new_duration != self.timer_duration:
                self.timer_duration = new_duration
        except:
            print(*self.urls)
        if self.pop and self.pop.winfo_exists():
            self.pop.destroy()
            self.pop = None
        self.countdown_label.config(text=f"{self.format_time(self.timer_duration)}:00")

    def append_links(self, link):
        url = link.get().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.urls.append(url)
        self.listbox.insert(tk.END, url)
        self.save_link()
        link.delete(0, tk.END)

    def pop_links(self):
        if len(self.urls) >= 1:
            self.urls.pop()
            self.listbox.delete(tk.END)
            self.save_link()
        if len(self.urls) == 0:
            self.pages_open = False

    def save_link(self):  # persistently
        with open(json_path, "w") as f:
            json.dump(self.urls, f, indent=4)

    def format_time(self, duration):
        if duration < 10:
            display = f"{duration:02}"  # add leading zero
        else:
            display = str(duration)
        return display


if __name__ == "__main__":
    root = tk.Tk()
    app = FocusButton(root)
    root.mainloop()
