import tkinter as tk
import random
from datetime import datetime, timedelta


class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Test App")

        self.word_label = tk.Label(root, text="", font=("Helvetica", 24), wraplength=700,
                                   justify="center",  # Center-align text
                                   anchor="center",   # Center-anchor the text within the label
                                   highlightthickness=1, highlightbackground="black")
        self.word_label.pack(pady=70)

        self.timer_frame = tk.Frame(root)
        self.timer_frame.pack(pady=10)
        self.timer_canvas = tk.Canvas(self.timer_frame, width=70, height=70)
        self.timer_canvas.pack()
        self.timer_text = self.timer_canvas.create_text(35, 35, text="", font=("Helvetica", 18))

        self.input_entry = tk.Entry(root, font=("Helvetica", 18), highlightthickness=1, highlightbackground="black",
                                    highlightcolor="black")
        self.input_entry.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_test, bd=1, relief="solid")
        self.start_button.pack(pady=(5, 15))

        self.correct_count_label = tk.Label(root, text="Correct Words: 0", font=("Helvetica", 10))
        self.correct_count_label.pack(pady=1)

        self.wrong_count_label = tk.Label(root, text="Wrong Words: 0", font=("Helvetica", 10))
        self.wrong_count_label.pack(pady=1)

        self.keystrokes_label = tk.Label(root, text="Keystrokes: 0", font=("Helvetica", 10))
        self.keystrokes_label.pack(pady=1)

        self.correction_label = tk.Label(root, text="Corrections: 0", font=("Helvetica", 10))
        self.correction_label.pack(pady=1)

        self.wpm_label = tk.Label(root, text="WPM: 0", font=("Helvetica", 10))
        self.wpm_label.pack(pady=1)

        self.word_list = self.load_word_list()
        self.words_per_set = 10
        self.spacebar_count = 0
        self.current_set_index = 0
        self.current_word_index = 0
        self.start_time = None
        self.correct_count = 0
        self.wrong_count = 0
        self.keystrokes = 0
        self.correction_count = 0
        self.timer_interval = 1000  # in milliseconds

    def load_word_list(self):
        with open("word_list.txt", "r") as file:
            word_list = file.read().splitlines()
        return word_list

    def start_test(self):
        if self.start_button.cget("text") == "Start":
            self.start_button.config(text="Stop")
            self.input_entry.config(state="normal")
            self.input_entry.delete(0, "end")
            self.input_entry.focus()

            # Reset statistics
            self.correct_count = 0
            self.wrong_count = 0
            self.keystrokes = 0
            self.wpm_label.config(text="WPM: 0")
            self.correct_count_label.config(text="Correct Words: 0")
            self.wrong_count_label.config(text="Wrong Words: 0")
            self.keystrokes_label.config(text="Keystrokes: 0")
            self.correction_label.config(text="Corrections: 0")  # Update correction count label

            self.current_set_index = 0
            self.current_word_index = 0
            self.spacebar_count = 0
            self.start_time = datetime.now()
            self.update_timer()
            self.show_next_set()
        else:
            self.start_button.config(text="Start")
            self.input_entry.config(state="disabled")
            self.word_label.config(text="Test stopped.")
            self.start_time = None  # Stop the timer

            self.timer_canvas.delete("all")
            self.timer_canvas.create_oval(5, 5, 65, 65, outline="black", width=2)
            self.timer_canvas.create_text(35, 35, text="60", font=("Helvetica", 18))

    def show_next_set(self):
        if self.current_set_index >= len(self.word_list) // self.words_per_set:
            if self.start_time is not None:
                elapsed_time = datetime.now() - self.start_time
                if elapsed_time >= timedelta(minutes=1):
                    self.word_label.config(text="Test finished!")
                    self.input_entry.config(state="disabled")
                    self.start_button.config(state="normal")
                    return

        random_indices = random.sample(range(len(self.word_list)), self.words_per_set)
        words_to_show = [self.word_list[i] for i in random_indices]
        self.word_label.config(text=" ".join(words_to_show))
        self.current_set_index += 1
        self.current_word_index = 0  # Reset current word index

        # Modify this part to split words into lines
        words_per_line = self.words_per_set // 2
        words_line1 = words_to_show[:words_per_line]
        words_line2 = words_to_show[words_per_line:]

        padded_words_line1 = " ".join(words_line1)
        padded_words_line2 = " ".join(words_line2)

        self.word_label.config(text="\n".join([padded_words_line1, padded_words_line2]),
                               padx=40,  # Add horizontal padding
                               pady=40)  # Add vertical padding

    def space_pressed(self, event):
        typed_word = self.input_entry.get().strip()
        expected_word = self.word_label.cget("text").replace("\n", " ").split()[self.current_word_index]
        self.keystrokes += len(typed_word) + 1  # Include space in keystrokes count

        if typed_word == expected_word:
            self.correct_count += 1
        else:
            self.wrong_count += 1
            self.correction_count += 1  # Increment correction count

        self.correct_count_label.config(text="Correct Words: {}".format(self.correct_count))
        self.wrong_count_label.config(text="Wrong Words: {}".format(self.wrong_count))
        self.keystrokes_label.config(text="Keystrokes: {}".format(self.keystrokes))
        self.correction_label.config(
            text="Corrections: {}".format(self.correction_count))  # Update correction count label

        self.input_entry.delete(0, "end")  # Clear the input entry
        self.current_word_index += 1

        if self.current_word_index == self.words_per_set:
            self.current_word_index = 0
            self.show_next_set()

    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = datetime.now() - self.start_time
            remaining_time = timedelta(minutes=1) - elapsed_time
            remaining_seconds = int(remaining_time.total_seconds())
            seconds = remaining_seconds % 60

            # Clear previous content on the canvas
            self.timer_canvas.delete("all")

            # Draw circular border
            self.timer_canvas.create_oval(5, 5, 65, 65, outline="black", width=2)

            # Draw timer text within the circular border
            self.timer_canvas.create_text(35, 35, text="{:02d}".format(seconds), font=("Helvetica", 18))

            if elapsed_time < timedelta(minutes=1):
                self.root.after(self.timer_interval, self.update_timer)
                self.calculate_wpm(elapsed_time)

    def calculate_wpm(self, elapsed_time):
        total_chars_typed = self.keystrokes  # Include spaces as well
        minutes = elapsed_time.total_seconds() / 60
        wpm = (total_chars_typed / 5.5) / minutes if minutes > 0 else 0
        self.wpm_label.config(text="WPM: {:.2f}".format(wpm))

    def run(self):
        self.root.bind("<space>", self.space_pressed)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    app.show_next_set()  # Display initial words
    app.run()
