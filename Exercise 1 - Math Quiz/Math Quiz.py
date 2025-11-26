import tkinter as tk
import random
from PIL import Image, ImageTk
import pygame
import os

class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("➕ MATH MASTER: The Ultimate Quiz")

        # --- FIX 1: MAIN WINDOW ICON REMOVAL ---
        try:
            master.attributes('-toolwindow', True)
        except tk.TclError:
            pass 

        # FULL-SCREEN IMPLEMENTATION
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.end_fullscreen)

        # SCRIPT DIRECTORY
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # COLOR PALETTE
        self.BG_DARK = "#000000"
        self.BG_LIGHT = "#FFFFFF"
        self.ACCENT_YELLOW = "#FFD700" 
        self.ACCENT_BLACK = "#2C2C2C"   
        self.TEXT_COLOR = "#000000"
        self.HIGHLIGHT = "#FFD700"
        self.QUIT_COLOR = "#FF6B6B"     

        master.configure(bg=self.BG_DARK)

        # AUDIO SETUP
        self.setup_audio()

        # BACKGROUND IMAGE
        self.set_image_background("math.jpg")

        # FONT STYLES
        self.font_style = ("Segoe UI", 11)
        self.header_font = ("Segoe UI", 22, "bold")
        self.problem_font = ("Segoe UI", 34, "bold")

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
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Audio setup failed: {e}")

    def play_background_music(self, music_file="chill.mp3"):
        try:
            full_path = os.path.join(self.script_dir, music_file)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Could not play music: {e}.")

    # --- FULL SCREEN EXIT ---
    def end_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>', lambda e: self.master.destroy())

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    # --- IMAGE HANDLING ---
    def set_image_background(self, image_path):
        try:
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            full_path = os.path.join(self.script_dir, image_path)
            original_image = Image.open(full_path)
            resized_image = original_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            overlay = Image.new('RGBA', resized_image.size, (255, 255, 255, 200))
            self.bg_image_pil = Image.blend(resized_image.convert('RGBA'), overlay, 0.2)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_pil)
            self.bg_canvas = tk.Canvas(self.master, width=screen_width, height=screen_height, highlightthickness=0)
            self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        except Exception as e:
            print(f"Image Error: {e}")
            self.master.configure(bg=self.BG_DARK)

    # --- CORE GAME LOGIC ---
    def random_int(self, difficulty_level):
        if difficulty_level == 1: return 1, 9
        elif difficulty_level == 2: return 10, 99
        elif difficulty_level == 3: return 1000, 9999
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

    # --- HELPER: CREATE CUSTOM POPUP ---
    def create_custom_popup(self, title, width=300, height=150):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.configure(bg=self.BG_LIGHT)
        
        # --- FIX 2: POPUP ICON REMOVAL ---
        try:
            popup.attributes('-toolwindow', True)
        except tk.TclError:
            pass

        # Center the popup
        x = self.master.winfo_rootx() + self.master.winfo_width() // 2 - (width // 2)
        y = self.master.winfo_rooty() + self.master.winfo_height() // 2 - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.resizable(False, False)
        popup.transient(self.master)
        popup.grab_set() # Make modal
        return popup

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

    # --- CUSTOM QUIT POPUP (Replaces messagebox.askyesno) ---
    def quit_game(self):
        popup = self.create_custom_popup("Quit Game", width=350)
        
        tk.Label(popup, text="Quit Game?", font=("Segoe UI", 16, "bold"), 
                 bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=(15, 5))
        tk.Label(popup, text="Are you sure? Your score will be lost.", 
                 font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.TEXT_COLOR).pack(pady=5)
        
        btn_frame = tk.Frame(popup, bg=self.BG_LIGHT)
        btn_frame.pack(pady=15)
        
        def confirm():
            popup.destroy()
            self.master.unbind('<Return>')
            self.switch_frame(self.display_menu)
            
        # Custom styled buttons
        tk.Button(btn_frame, text="YES", command=confirm, 
                  bg=self.QUIT_COLOR, fg=self.BG_LIGHT, activebackground="#FF5252", activeforeground=self.BG_LIGHT,
                  relief=tk.FLAT, width=10, cursor="hand2").pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="NO", command=popup.destroy, 
                  bg=self.ACCENT_BLACK, fg=self.BG_LIGHT, activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                  relief=tk.FLAT, width=10, cursor="hand2").pack(side=tk.LEFT, padx=10)

    # --- DISPLAY MENU ---
    def display_menu(self):
        self.reset_game()
        menu_frame = tk.Frame(self.master, padx=40, pady=30, bg=self.BG_LIGHT,
                              relief=tk.RIDGE, borderwidth=0, highlightthickness=2,
                              highlightbackground=self.ACCENT_YELLOW)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = menu_frame

        # Bubbles background
        bubble_canvas = tk.Canvas(menu_frame, bg=self.BG_LIGHT, highlightthickness=0)
        bubble_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        bubbles = []
        symbols = ['+', '-', '×', '÷', '=', 'π', '∞', '∑']
        
        for _ in range(6):
            x = random.randint(20, 380)
            y = random.randint(20, 380)
            size = random.randint(30, 60)
            symbol = random.choice(symbols)
            speed = random.uniform(0.3, 1.5)
            
            bubble = bubble_canvas.create_oval(x, y, x+size, y+size, 
                                        fill=self.BG_LIGHT, outline=self.ACCENT_YELLOW, width=2)
            text = bubble_canvas.create_text(x+size/2, y+size/2, text=symbol, 
                                    font=("Segoe UI", size//3), fill=self.ACCENT_BLACK)
            bubbles.append({'bubble': bubble, 'text': text, 'x': x, 'y': y, 'dx': random.choice([-1, 1])*speed, 'dy': random.choice([-1, 1])*speed, 'size': size})
        
        def animate_bubbles():
            for bubble_data in bubbles:
                bubble_canvas.move(bubble_data['bubble'], bubble_data['dx'], bubble_data['dy'])
                bubble_canvas.move(bubble_data['text'], bubble_data['dx'], bubble_data['dy'])
                bubble_data['x'] += bubble_data['dx']
                bubble_data['y'] += bubble_data['dy']
                if bubble_data['x'] <= 0 or bubble_data['x'] >= 400 - bubble_data['size']: bubble_data['dx'] *= -1
                if bubble_data['y'] <= 0 or bubble_data['y'] >= 400 - bubble_data['size']: bubble_data['dy'] *= -1
            menu_frame.after(50, animate_bubbles)
        animate_bubbles()

        tk.Label(menu_frame, text="➕ MATH MASTER", font=self.header_font, bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=(0, 10))
        tk.Label(menu_frame, text="Select Difficulty Level", font=("Segoe UI", 14), bg=self.BG_LIGHT, fg=self.TEXT_COLOR).pack(pady=(0, 20))

        options = [("EASY", 1), ("MODERATE", 2), ("ADVANCED", 3)]
        for text, level in options:
            btn = tk.Button(menu_frame, text=text, font=self.font_style, bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                            activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                            command=lambda l=level: self.start_quiz(l), width=18, height=1, bd=0, relief=tk.FLAT, cursor="hand2")
            btn.pack(pady=6)
            btn.bind("<Enter>", lambda e, b=btn: [b.config(bg=self.ACCENT_YELLOW, fg=self.BG_DARK)])
            btn.bind("<Leave>", lambda e, b=btn: [b.config(bg=self.ACCENT_BLACK, fg=self.BG_LIGHT)])

        quit_btn = tk.Button(menu_frame, text="QUIT GAME", font=("Segoe UI", 10), bg=self.QUIT_COLOR, fg=self.BG_LIGHT,
                            activebackground="#FF5252", activeforeground=self.BG_LIGHT,
                            command=self.master.quit, width=12, height=1, bd=0, relief=tk.FLAT, cursor="hand2")
        quit_btn.pack(pady=8)
        quit_btn.bind("<Enter>", lambda e: quit_btn.config(bg="#FF5252"))
        quit_btn.bind("<Leave>", lambda e: quit_btn.config(bg=self.QUIT_COLOR))

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

        quiz_frame = tk.Frame(self.master, padx=30, pady=25, bg=self.BG_LIGHT,
                              relief=tk.RIDGE, borderwidth=0, highlightthickness=2,
                              highlightbackground=self.ACCENT_YELLOW)
        quiz_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current_frame = quiz_frame

        tk.Label(quiz_frame, text=f"Question {self.question_count} of 10  |  Score: {self.score}",
                 font=("Segoe UI", 12, "bold"), bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=(0, 20))

        tk.Label(quiz_frame, text=f"{self.current_problem['num1']} {self.current_problem['op']} {self.current_problem['num2']} = ?", 
                 font=self.problem_font, bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=10)

        self.answer_entry = tk.Entry(quiz_frame, font=self.header_font, justify='center', width=12, bd=2, 
                                     bg=self.ACCENT_BLACK, fg=self.BG_LIGHT, insertbackground=self.ACCENT_YELLOW, 
                                     relief=tk.FLAT, highlightthickness=2, highlightcolor=self.ACCENT_YELLOW, highlightbackground=self.ACCENT_BLACK)
        self.answer_entry.pack(pady=20)
        self.answer_entry.focus_set()

        self.feedback_label = tk.Label(quiz_frame, text="", font=self.font_style, bg=self.BG_LIGHT, fg=self.ACCENT_BLACK)
        self.feedback_label.pack(pady=5)

        btn_container = tk.Frame(quiz_frame, bg=self.BG_LIGHT)
        btn_container.pack(pady=10)

        submit_btn = tk.Button(btn_container, text="SUBMIT", font=self.font_style, bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                               activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                               command=self.check_answer, width=10, height=1, bd=0, relief=tk.FLAT, cursor="hand2")
        submit_btn.pack(side=tk.LEFT, padx=15)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg=self.ACCENT_YELLOW, fg=self.BG_DARK))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg=self.ACCENT_BLACK, fg=self.BG_LIGHT))

        quit_btn = tk.Button(btn_container, text="QUIT", font=("Segoe UI", 10), bg=self.QUIT_COLOR, fg=self.BG_LIGHT,
                             activebackground="#FF5252", activeforeground=self.BG_LIGHT,
                             command=self.quit_game, width=8, height=1, bd=0, relief=tk.FLAT, cursor="hand2")
        quit_btn.pack(side=tk.RIGHT, padx=15)
        quit_btn.bind("<Enter>", lambda e: quit_btn.config(bg="#FF5252"))
        quit_btn.bind("<Leave>", lambda e: quit_btn.config(bg=self.QUIT_COLOR))

        self.master.bind('<Return>', lambda event: self.check_answer())

    # --- CHECK ANSWER ---
    def check_answer(self):
        self.master.unbind('<Return>')
        user_answer = self.answer_entry.get().strip()

        if self.is_correct(user_answer):
            points = 10 if self.attempts == 0 else 5
            self.score += points

            # Custom Success Popup (No Feather)
            popup = self.create_custom_popup("➕ Correct!")
            
            tk.Label(popup, text="✅ CORRECT!", font=("Segoe UI", 16, "bold"), bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=10)
            tk.Label(popup, text=f"+{points} points!", font=("Segoe UI", 14), bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=5)
            
            tk.Button(popup, text="CONTINUE", font=self.font_style, bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                      activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                      command=lambda: [popup.destroy(), self.switch_frame(self.display_problem)],
                      width=10, bd=0, relief=tk.FLAT, cursor="hand2").pack(pady=10)

        else:
            self.attempts += 1
            if self.attempts < 2:
                self.feedback_label.config(text="Incorrect. Try again!")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus_set()
                self.master.bind('<Return>', lambda event: self.check_answer())
            else:
                # Custom Incorrect Popup (No Feather)
                # Replaces messagebox.showerror
                popup = self.create_custom_popup("Incorrect")
                
                tk.Label(popup, text="❌ Incorrect", font=("Segoe UI", 16, "bold"), bg=self.BG_LIGHT, fg="#FF6B6B").pack(pady=10)
                tk.Label(popup, text=f"The correct answer was {self.current_problem['answer']}.", font=("Segoe UI", 11), bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=5)
                
                tk.Button(popup, text="OK", font=self.font_style, bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                          activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                          command=lambda: [popup.destroy(), self.switch_frame(self.display_problem)],
                          width=10, bd=0, relief=tk.FLAT, cursor="hand2").pack(pady=15)
                
                # Ensure closing via X works too
                popup.protocol("WM_DELETE_WINDOW", lambda: [popup.destroy(), self.switch_frame(self.display_problem)])

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

        # Bubbles background
        bubble_canvas = tk.Canvas(results_frame, bg=self.BG_LIGHT, highlightthickness=0)
        bubble_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        bubbles = []
        symbols = ['+', '-', '×', '÷', '=', 'π', '∞', '∑']
        
        for _ in range(6):
            x = random.randint(20, 380)
            y = random.randint(20, 380)
            size = random.randint(30, 60)
            symbol = random.choice(symbols)
            speed = random.uniform(0.3, 1.5)
            
            bubble = bubble_canvas.create_oval(x, y, x+size, y+size, 
                                        fill=self.BG_LIGHT, outline=self.ACCENT_YELLOW, width=2)
            text = bubble_canvas.create_text(x+size/2, y+size/2, text=symbol, 
                                    font=("Segoe UI", size//3), fill=self.ACCENT_BLACK)
            bubbles.append({'bubble': bubble, 'text': text, 'x': x, 'y': y, 'dx': random.choice([-1, 1])*speed, 'dy': random.choice([-1, 1])*speed, 'size': size})
        
        def animate_bubbles():
            for bubble_data in bubbles:
                bubble_canvas.move(bubble_data['bubble'], bubble_data['dx'], bubble_data['dy'])
                bubble_canvas.move(bubble_data['text'], bubble_data['dx'], bubble_data['dy'])
                bubble_data['x'] += bubble_data['dx']
                bubble_data['y'] += bubble_data['dy']
                if bubble_data['x'] <= 0 or bubble_data['x'] >= 400 - bubble_data['size']: bubble_data['dx'] *= -1
                if bubble_data['y'] <= 0 or bubble_data['y'] >= 400 - bubble_data['size']: bubble_data['dy'] *= -1
            results_frame.after(50, animate_bubbles)
        animate_bubbles()

        tk.Label(results_frame, text="🏆 QUIZ COMPLETE!", font=self.header_font, bg=self.BG_LIGHT, fg=self.ACCENT_YELLOW).pack(pady=15)
        tk.Label(results_frame, text=f"Final Score: {self.score} / {max_score}", font=("Segoe UI", 18, "bold"), bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=10)
        tk.Label(results_frame, text=f"Grade: {grade}", font=("Segoe UI", 14), bg=self.BG_LIGHT, fg=self.ACCENT_BLACK).pack(pady=5)
        tk.Label(results_frame, text="Play again?", font=("Segoe UI", 12), bg=self.BG_LIGHT, fg=self.TEXT_COLOR).pack(pady=20)

        btn_container = tk.Frame(results_frame, bg=self.BG_LIGHT)
        btn_container.pack(pady=10)

        replay_btn = tk.Button(btn_container, text="PLAY AGAIN", font=self.font_style, bg=self.ACCENT_BLACK, fg=self.BG_LIGHT,
                               activebackground=self.ACCENT_YELLOW, activeforeground=self.BG_DARK,
                               command=lambda: self.switch_frame(self.display_menu), width=12, height=1, bd=0, relief=tk.FLAT, cursor="hand2")
        replay_btn.pack(side=tk.LEFT, padx=10)
        replay_btn.bind("<Enter>", lambda e: replay_btn.config(bg=self.ACCENT_YELLOW, fg=self.BG_DARK))
        replay_btn.bind("<Leave>", lambda e: replay_btn.config(bg=self.ACCENT_BLACK, fg=self.BG_LIGHT))

        quit_btn = tk.Button(btn_container, text="QUIT GAME", font=("Segoe UI", 10), bg=self.QUIT_COLOR, fg=self.BG_LIGHT,
                             activebackground="#FF5252", activeforeground=self.BG_LIGHT,
                             command=self.master.quit, width=10, height=1, bd=0, relief=tk.FLAT, cursor="hand2")
        quit_btn.pack(side=tk.RIGHT, padx=10)
        quit_btn.bind("<Enter>", lambda e: quit_btn.config(bg="#FF5252"))
        quit_btn.bind("<Leave>", lambda e: quit_btn.config(bg=self.QUIT_COLOR))

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()