import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import pygame
import os

class QuizApp:
    # This comment fixes the previous error line
    # I use a comment here so Python doesn't crash

    def __init__(self, master):
        self.master = master
        master.title("✨ MATH MASTER: The Ultimate Quiz")

        # FULL-SCREEN IMPLEMENTATION
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.end_fullscreen)

        # SCRIPT DIRECTORY: helps to get images/audio paths correctly
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # COLOR PALETTE
        self.BG_DARK = "#000000"
        self.BG_LIGHT = "#FFFFFF"
        self.ACCENT_YELLOW = "#CCAA00"
        self.ACCENT_BLACK = "#333333"
        self.TEXT_COLOR = "#000000"
        self.HIGHLIGHT = "#CCAA00"

        master.configure(bg=self.BG_DARK)

        # AUDIO SETUP
        self.setup_audio()  # Advanced: I got help from ChatGPT to setup pygame correctly

        # BACKGROUND IMAGE
        self.set_image_background("math.jpg")  # Image file in the same folder

        # FONT STYLES
        self.font_style = ("Segoe UI", 12)
        self.header_font = ("Segoe UI", 20, "bold")
        self.problem_font = ("Segoe UI", 32, "bold")

        # GAME VARIABLES
        self.difficulty = 0
        self.score = 0
        self.question_count = 0
        self.current_problem = {}
        self.attempts = 0

        self.current_frame = None
        self.display_menu()

    # --- AUDIO METHODS ---
    def setup_audio(self):
        """Initialize pygame mixer for music"""
        try:
            pygame.mixer.init()  # Advanced: ChatGPT helped me use mixer correctly
        except pygame.error as e:
            print(f"Audio setup failed: {e}")

    def play_background_music(self, music_file="chill.mp3"):
        """Play background music in loop with low volume"""
        try:
            full_path = os.path.join(self.script_dir, music_file)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Could not play music: {e}. Check if file '{music_file}' exists at {full_path}.")

    # --- FULL SCREEN EXIT ---
    def end_fullscreen(self, event=None):
        """Exit fullscreen on Escape"""
        self.master.attributes('-fullscreen', False)
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>', lambda e: self.master.destroy())

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    # --- IMAGE HANDLING ---
    def set_image_background(self, image_path):
        """Load and display background image on canvas"""
        try:
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()

            full_path = os.path.join(self.script_dir, image_path)

            original_image = Image.open(full_path)
            resized_image = original_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

            # Overlay to make text visible
            overlay = Image.new('RGBA', resized_image.size, (255, 255, 255, 200))
            self.bg_image_pil = Image.blend(resized_image.convert('RGBA'), overlay, 0.2)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_pil)

            self.bg_canvas = tk.Canvas(self.master, width=screen_width, height=screen_height, highlightthickness=0)
            self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")

        except FileNotFoundError:
            print(f"File Not Found Error for: {full_path}")
            self.master.configure(bg=self.BG_DARK)
        except Exception as e:
            print(f"General Image Loading Error: {e}")
            self.master.configure(bg=self.BG_DARK)

    # --- CORE GAME LOGIC ---
    def random_int(self, difficulty_level):
        if difficulty_level == 1:
            return 1, 9
        elif difficulty_level == 2:
            return 10, 99
        elif difficulty_level == 3:
            return 1000, 9999
        return 1, 9

    def decide_operation(self):
        return random.choice(['+', '-'])

    def is_correct(self, user_answer):
        try:
            return int(user_answer) == self.current_problem['answer']
        except ValueError:
            return False

    def generate_problem(self):
        min_val, max_val = self.random_int(self.difficulty)
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)
        op = self.decide_operation()
        if op == '-' and num1 < num2:
            num1, num2 = num2, num1
        answer = num1 + num2 if op == '+' else num1 - num2
        self.current_problem = {'num1': num1, 'num2': num2, 'op': op, 'answer': answer}

    # --- GUI FRAME MANAGEMENT ---
    def switch_frame(self, new_frame_func):
        if self.current_frame:
            self.current_frame.destroy()
        new_frame_func()

    def reset_game(self):
        self.difficulty = 0
        self.score = 0
        self.question_count = 0
        self.current_problem = {}
        self.attempts = 0

    def quit_game(self):
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit? Your score will be lost."):
            self.master.unbind('<Return>')
            self.switch_frame(self.display_menu)

    # --- DISPLAY MENU ---
    def display_menu(self):
        self.reset_game()
        menu_frame = tk.Frame(self.master, padx=40, pady=30, bg=self.BG_LIGHT,
                              relief=tk.RIDGE, borderwidth=0, highlightthickness=2,
                              highlightbackground=self.ACCENT_YELLOW)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = menu_frame
        menu_frame.lift()

        tk.Label(menu_frame, text="🎯 MATH MASTER", font=self.header_font,
                 bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=(0, 10))
        tk.Label(menu_frame, text="Select Difficulty Level",
                 font=("Segoe UI", 14), bg=self.BG_LIGHT, fg=self.TEXT_COLOR).pack(pady=(0, 20))

        options = [("EASY", 1), ("MODERATE", 2), ("ADVANCED", 3)]

        for text, level in options:
            btn = tk.Button(menu_frame, text=text, font=self.font_style,
                            bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                            activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                            command=lambda l=level: self.start_quiz(l),
                            width=20, height=2, bd=0, relief=tk.FLAT, cursor="hand2")
            btn.pack(pady=8)

            def on_enter(e, button=btn):
                button['bg'] = self.ACCENT_YELLOW
                button['fg'] = self.BG_DARK

            def on_leave(e, button=btn):
                button['bg'] = self.ACCENT_BLACK
                button['fg'] = self.BG_LIGHT

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    # --- START QUIZ ---
    def start_quiz(self, level):
        self.difficulty = level
        self.question_count = 0
        self.score = 0
        self.play_background_music()
        self.switch_frame(self.display_problem)

    # --- DISPLAY PROBLEM ---
    def display_problem(self):
        self.question_count += 1
        self.attempts = 0

        if self.question_count > 10:
            self.switch_frame(self.display_results)
            return

        self.generate_problem()

        quiz_frame = tk.Frame(self.master, padx=20, pady=20, bg=self.BG_LIGHT,
                              relief=tk.RIDGE, borderwidth=0, highlightthickness=2,
                              highlightbackground=self.ACCENT_YELLOW)
        quiz_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = quiz_frame
        quiz_frame.lift()

        header_text = f"Question {self.question_count} of 10  |  Score: {self.score}"
        tk.Label(quiz_frame, text=header_text,
                 font=("Segoe UI", 12, "bold"), bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=(0, 20))

        problem_text = f"{self.current_problem['num1']} {self.current_problem['op']} {self.current_problem['num2']} = ?"
        tk.Label(quiz_frame, text=problem_text, font=self.problem_font,
                 bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=10)

        self.answer_entry = tk.Entry(quiz_frame, font=self.header_font, justify='center',
                                     width=12, bd=2, bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                                     insertbackground=self.ACCENT_YELLOW, relief=tk.FLAT,
                                     highlightthickness=2, highlightcolor=self.ACCENT_YELLOW,
                                     highlightbackground=self.ACCENT_BLACK)
        self.answer_entry.pack(pady=20)
        self.answer_entry.focus_set()

        self.feedback_label = tk.Label(quiz_frame, text="", font=self.font_style,
                                       bg=self.BG_LIGHT, fg=self.ACCENT_BLACK)
        self.feedback_label.pack(pady=5)

        button_container = tk.Frame(quiz_frame, bg=self.BG_LIGHT)
        button_container.pack(pady=10)

        submit_btn = tk.Button(button_container, text="SUBMIT", font=self.font_style,
                               bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                               activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                               command=self.check_answer, width=12, height=1, bd=0, relief=tk.FLAT,
                               cursor="hand2")
        submit_btn.pack(side=tk.LEFT, padx=15)

        quit_btn = tk.Button(button_container, text="QUIT", font=self.font_style,
                             bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                             activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                             command=self.quit_game, width=12, height=1, bd=0, relief=tk.FLAT,
                             cursor="hand2")
        quit_btn.pack(side=tk.RIGHT, padx=15)

        def on_enter_submit(e): submit_btn['bg'], submit_btn['fg'] = self.ACCENT_YELLOW, self.BG_DARK
        def on_leave_submit(e): submit_btn['bg'], submit_btn['fg'] = self.ACCENT_BLACK, self.BG_LIGHT
        def on_enter_quit(e): quit_btn['bg'], quit_btn['fg'] = self.ACCENT_YELLOW, self.BG_DARK
        def on_leave_quit(e): quit_btn['bg'], quit_btn['fg'] = self.ACCENT_BLACK, self.BG_LIGHT

        submit_btn.bind("<Enter>", on_enter_submit)
        submit_btn.bind("<Leave>", on_leave_submit)
        quit_btn.bind("<Enter>", on_enter_quit)
        quit_btn.bind("<Leave>", on_leave_quit)

        self.master.bind('<Return>', lambda event: self.check_answer())

    # --- CHECK ANSWER ---
    def check_answer(self):
        """Handles the submission and scoring of the user's answer."""
        self.master.unbind('<Return>')

        user_answer = self.answer_entry.get().strip()

        if self.is_correct(user_answer):
            points = 10 if self.attempts == 0 else 5
            self.score += points

            success_window = tk.Toplevel(self.master)
            success_window.title("Correct!")
            success_window.geometry("300x150")
            success_window.configure(bg=self.BG_LIGHT)
            success_window.resizable(False, False)
            success_window.transient(self.master)
            success_window.grab_set()
            success_window.geometry("+%d+%d" % (
                self.master.winfo_rootx() + self.master.winfo_width() // 2 - 150,
                self.master.winfo_rooty() + self.master.winfo_height() // 2 - 75
            ))

            tk.Label(success_window, text="✅ CORRECT!", font=("Segoe UI", 16, "bold"),
                     bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=10)

            tk.Label(success_window, text=f"+{points} points!", font=("Segoe UI", 14),
                     bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=5)

            tk.Button(success_window, text="CONTINUE", font=self.font_style,
                      bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                      activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                      command=lambda: [success_window.destroy(), self.switch_frame(self.display_problem)],
                      width=10, bd=0, relief=tk.FLAT).pack(pady=10)

        else:
            self.attempts += 1
            if self.attempts < 2:
                self.feedback_label.config(text="Incorrect. Try again!")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus_set()
                self.master.bind('<Return>', lambda event: self.check_answer())
            else:
                messagebox.showerror("Incorrect", f"The correct answer was {self.current_problem['answer']}.")
                self.switch_frame(self.display_problem)

    # --- GRADING ---
    def get_grade(self, final_score):
        if final_score > 90: return "A+ (Math Master!)"
        elif final_score >= 80: return "A (Excellent!)"
        elif final_score >= 70: return "B (Great Job!)"
        elif final_score >= 60: return "C (Good Work)"
        else: return "D (Keep Practicing)"

    # --- RESULTS SCREEN ---
    def display_results(self):
        max_score = 100
        grade = self.get_grade(self.score)

        results_frame = tk.Frame(self.master, padx=40, pady=30, bg=self.BG_LIGHT,
                                 relief=tk.RIDGE, borderwidth=0, highlightthickness=2,
                                 highlightbackground=self.ACCENT_YELLOW)
        results_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = results_frame
        results_frame.lift()

        tk.Label(results_frame, text="🏆 QUIZ COMPLETE!",
                 font=self.header_font, bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=15)

        summary = f"Final Score: {self.score} / {max_score}"
        tk.Label(results_frame, text=summary, font=("Segoe UI", 18, "bold"),
                 bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=10)

        rank = f"Grade: {grade}"
        tk.Label(results_frame, text=rank, font=("Segoe UI", 14),
                 bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=5)

        tk.Label(results_frame, text="Play again?",
                 font=("Segoe UI", 12), bg=self.BG_LIGHT, fg=self.TEXT_COLOR).pack(pady=20)

        replay_btn = tk.Button(results_frame, text="PLAY AGAIN", font=self.font_style,
                               bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                               activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                               command=lambda: self.switch_frame(self.display_menu),
                               width=15, height=1, bd=0, relief=tk.FLAT,
                               cursor="hand2")
        replay_btn.pack(pady=10)

        def on_enter(e): replay_btn['bg'], replay_btn['fg'] = self.ACCENT_YELLOW, self.BG_DARK
        def on_leave(e): replay_btn['bg'], replay_btn['fg'] = self.ACCENT_BLACK, self.BG_LIGHT

        replay_btn.bind("<Enter>", on_enter)
        replay_btn.bind("<Leave>", on_leave)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
