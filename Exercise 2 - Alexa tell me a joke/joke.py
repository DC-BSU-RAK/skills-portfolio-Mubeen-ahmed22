import tkinter as tk
from tkinter import messagebox
import random
from pathlib import Path
import pygame
import os

class ModernJokeTeller:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("1000x700")
        
        # Initialize pygame sound system for background music
        # (This part is a bit advanced because pygame handles audio separately.
        # I took help from Chatgpt to understand how to initialize the mixer correctly.)
        pygame.mixer.init()
        self.background_music = None
        
        # Color theme used throughout the interface
        self.colors = {
            'bg': '#FFD700',
            'card_bg': '#FFFFFF',
            'card_outer': '#FFED4E',
            'button_bg': '#000000',
            'button_hover': '#333333',
            'text_black': '#000000',
            'text_white': '#FFFFFF',
            'accent': '#B8860B',
            'stroke': '#000000'
        }
        
        # Fonts for different UI elements
        self.title_font = ('Arial', 32, 'bold')
        self.joke_font = ('Arial', 20)
        self.punchline_font = ('Arial', 19, 'bold')
        self.button_font = ('Arial', 14, 'bold')
        self.status_font = ('Arial', 12)
        
        # File paths for background image and music file
        self.bg_image_path = "background.png"
        self.music_path = "backgroundaudio.mp3"
        
        # Load jokes from file or use fallback list
        self.jokes = self.load_jokes()
        self.current_joke = None
        
        # Build the full UI layout
        self.create_modern_interface()
        
        # Start background music automatically
        self.start_background_music()
        
    def load_jokes(self):
        # Loads jokes from a text file if it exists, otherwise uses default jokes.
        # This part is slightly advanced because of Path() and folder navigation,
        #took help from chatgpt to make it work properly.
        try:
            current_dir = Path(__file__).parent
            resources_dir = current_dir.parent / "resources"
            file_path = resources_dir / "randomJokes.txt"
            
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as file:
                    jokes = [line.strip() for line in file if line.strip()]
                return jokes
            else:
                return [
                    "Why did the chicken cross the road?To get to the other side",
                    "What happens if you boil a clown?You get a laughing stock",
                    "Why don't scientists trust atoms?Because they make up everything",
                    "What do you call a fake noodle?An impasta",
                    "Why did the scarecrow win an award?Because he was outstanding in his field",
                    "How does a penguin build its house?Igloos it together",
                    "What do you call a bear with no teeth?A gummy bear",
                    "Why don't eggs tell jokes?They'd crack each other up",
                    "What do you call a sleeping bull?A bulldozer",
                    "Why did the math book look so sad?Because it had too many problems"
                ]
        except:
            return ["Why did the computer go to the doctor?Because it had a virus!"]
    
    def start_background_music(self):
        """Play background music in a loop with lower volume."""
        try:
            # Loading and looping background music
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Could not load background music: {e}")
            print("Continuing without background music")
    
    def stop_background_music(self):
        """Stop playing the background music."""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def create_modern_interface(self):
        # Canvas used to place the background image
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.bg_canvas.pack(fill='both', expand=True)
        
        # Load the image onto the background canvas
        self.load_background_image()
        
        # Main outer black border
        main_stroke = tk.Frame(self.bg_canvas, bg=self.colors['stroke'], highlightthickness=0)
        main_stroke.place(relx=0.5, rely=0.5, anchor='center', width=920, height=670)
        
        # Main yellow area
        main_frame = tk.Frame(main_stroke, bg=self.colors['bg'], highlightthickness=0)
        main_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Header container
        header_stroke = tk.Frame(main_frame, bg=self.colors['stroke'], highlightthickness=0)
        header_stroke.pack(fill='x', pady=(15, 20), padx=60)
        
        header_frame = tk.Frame(header_stroke, bg=self.colors['bg'], highlightthickness=0)
        header_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Main title
        title_label = tk.Label(
            header_frame, 
            text="🎤 Joking Alexa",
            font=self.title_font,
            fg=self.colors['text_black'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=15)
        
        # Subtitle text
        subtitle_label = tk.Label(
            header_frame,
            text="Relax, Laugh a little.",
            font=('Arial', 16),
            fg=self.colors['text_black'],
            bg=self.colors['bg']
        )
        subtitle_label.pack(pady=5)
        
        # Emoji icon
        alexa_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        alexa_frame.pack(pady=15)
        
        alexa_icon = tk.Label(
            alexa_frame,
            text="😂",
            font=('Arial', 48),
            fg=self.colors['text_black'],
            bg=self.colors['bg']
        )
        alexa_icon.pack()
        
        # Centered white card area
        stroke_box = tk.Frame(main_frame, bg=self.colors['stroke'], relief='flat', bd=0)
        stroke_box.pack(fill='both', expand=True, pady=10, padx=60)
        
        outer_box = tk.Frame(stroke_box, bg=self.colors['card_outer'], relief='flat', bd=0)
        outer_box.pack(fill='both', expand=True, padx=3, pady=3)
        
        inner_box = tk.Frame(outer_box, bg=self.colors['card_bg'], relief='flat', bd=0)
        inner_box.pack(fill='both', expand=True, padx=12, pady=12)
        
        # Content (joke text) container
        joke_content = tk.Frame(inner_box, bg=self.colors['card_bg'])
        joke_content.pack(fill='both', expand=True, padx=30, pady=40)
        
        # Setup text (initially showing intro text)
        self.setup_label = tk.Label(
            joke_content,
            text="Ready to brighten your day? Click Tell Joke to begin! ✨",
            font=self.joke_font,
            fg=self.colors['text_black'],
            bg=self.colors['card_bg'],
            wraplength=550,
            justify='center'
        )
        self.setup_label.place(relx=0.5, rely=0.3, anchor='center')
        
        # Punchline text (hidden until needed)
        self.punchline_label = tk.Label(
            joke_content,
            text="",
            font=self.punchline_font,
            fg=self.colors['accent'],
            bg=self.colors['card_bg'],
            wraplength=550,
            justify='center'
        )
        
        # Button row container
        button_stroke = tk.Frame(main_frame, bg=self.colors['stroke'], highlightthickness=0)
        button_stroke.pack(fill='x', pady=20, padx=60)
        
        button_container = tk.Frame(button_stroke, bg=self.colors['bg'], highlightthickness=0)
        button_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Buttons
        self.tell_btn = self.create_modern_button(button_container, "🎤 Tell Joke", self.tell_joke, 0, 0)
        self.punchline_btn = self.create_modern_button(button_container, "😂 Punchline", self.show_punchline, 0, 1)
        self.next_btn = self.create_modern_button(button_container, "🔄 Next", self.next_joke, 0, 2)
        self.quit_btn = self.create_modern_button(button_container, "🚪 Quit", self.quit_app, 0, 3)
        
        # Disable punchline/next buttons until a joke is shown
        self.punchline_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        
        # Status bar at bottom
        status_stroke = tk.Frame(main_frame, bg=self.colors['stroke'], highlightthickness=0)
        status_stroke.pack(fill='x', pady=10, padx=60)
        
        status_frame = tk.Frame(status_stroke, bg=self.colors['bg'], highlightthickness=0)
        status_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Label that shows instructions or info
        self.status_label = tk.Label(
            status_frame,
            text="Click Tell Joke to start the fun! 🎉",
            font=self.status_font,
            fg=self.colors['text_black'],
            bg=self.colors['bg']
        )
        self.status_label.pack(pady=8)
    
    def load_background_image(self):
        """Load the background image onto the canvas."""
        # This part is a bit tricky because Tkinter PhotoImage only supports PNG.
        # I took help from Chatgpt to understand how to place the image correctly.
        try:
            self.bg_image = tk.PhotoImage(file=self.bg_image_path)
            self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor='nw')
        except Exception as e:
            print(f"Background image not found: {e}")
            self.bg_canvas.configure(bg=self.colors['bg'])
    
    def create_modern_button(self, parent, text, command, row, col):
        # Create a styled button in the interface
        btn = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            bg=self.colors['button_bg'],
            fg=self.colors['text_white'],
            activebackground=self.colors['button_hover'],
            activeforeground=self.colors['text_white'],
            relief='flat',
            bd=0,
            width=15,
            height=2,
            cursor='hand2',
            command=command,
            anchor='w'
        )
        btn.grid(row=row, column=col, padx=10, pady=5)
        
        # Hover animation
        def on_enter(e):
            if btn['state'] != 'disabled':
                btn['bg'] = self.colors['button_hover']
        def on_leave(e):
            if btn['state'] != 'disabled':
                btn['bg'] = self.colors['button_bg']
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def tell_joke(self):
        # Pick a random joke and show only the setup part
        if not self.jokes:
            messagebox.showerror("Error", "No jokes available!")
            return
        
        joke_text = random.choice(self.jokes)
        
        # Split setup and punchline
        if '?' in joke_text:
            setup, punchline = joke_text.split('?', 1)
            setup += "?"
        else:
            setup = joke_text
            punchline = "No punchline available!"
        
        self.current_joke = (setup, punchline)
        
        # Update the text display
        self.setup_label.config(text=setup)
        self.punchline_label.place_forget()
        
        # Enable next steps
        self.tell_btn.config(state='disabled')
        self.punchline_btn.config(state='normal')
        self.next_btn.config(state='normal')
        
        self.status_label.config(text="Joke loaded! Click Punchline to continue. 🎯")
    
    def show_punchline(self):
        # Display the punchline on the card
        if not self.current_joke:
            return
        
        self.punchline_label.config(text=self.current_joke[1])
        self.punchline_label.place(relx=0.5, rely=0.85, anchor='center')
        
        self.punchline_btn.config(state='disabled')
        
        self.status_label.config(text="Hope that made you smile! 😄")
    
    def next_joke(self):
        # Reset the interface and prepare for another joke
        self.setup_label.config(text="Getting another joke ready... ✨")
        self.punchline_label.place_forget()
        
        self.tell_btn.config(state='normal')
        self.punchline_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        
        self.status_label.config(text="Ready for more laughter! 🌟")
    
    def quit_app(self):
        # Confirm before exiting the program
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.stop_background_music()
            self.root.quit()

def main():
    # Create the main window and start the program
    root = tk.Tk()
    app = ModernJokeTeller(root)
    root.mainloop()

if __name__ == "__main__":
    main()
