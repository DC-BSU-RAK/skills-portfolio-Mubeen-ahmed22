import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw
import datetime

class Student:
    def __init__(self, student_id: int, name: str, coursework_marks: List[int], exam_mark: int):
        self.student_id = student_id
        self.name = name
        self.coursework_marks = coursework_marks
        self.exam_mark = exam_mark
    
    @property
    def total_coursework(self) -> int:
        return sum(self.coursework_marks)
    
    @property
    def total_marks(self) -> int:
        return self.total_coursework + self.exam_mark
    
    @property
    def percentage(self) -> float:
        return (self.total_marks / 160) * 100
    
    @property
    def grade(self) -> str:
        percentage = self.percentage
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def to_file_format(self) -> str:
        return f"{self.student_id},{self.name},{self.coursework_marks[0]},{self.coursework_marks[1]},{self.coursework_marks[2]},{self.exam_mark}"

class StudentManager:
    def __init__(self, filename: str = "studentMarks.txt"):
        self.filename = filename
        self.students: List[Student] = []
        self.script_dir = Path(__file__).resolve().parent
        self.load_data()
    
    def load_data(self):
        text_files = ["studentMarks.txt", "studentsMarks.txt"]
        loaded = False
        
        for text_filename in text_files:
            text_file_path = self.script_dir / text_filename
            try:
                if text_file_path.exists():
                    print(f"Loading student data from {text_file_path.name}")
                    with open(text_file_path, 'r') as file:
                        lines = file.readlines()
                    
                    self.students = []
                    
                    if not lines:
                        continue

                    try:
                        num_students = int(lines[0].strip())
                    except ValueError:
                        print(f"First line of {text_filename} should be the student count")
                        continue
                    
                    for i in range(1, len(lines)):
                        if i <= num_students and i < len(lines):
                            line = lines[i].strip()
                            if line:
                                data = line.split(',')
                                if len(data) >= 6:
                                    try:
                                        student_id = int(data[0])
                                        name = data[1]
                                        coursework_marks = [int(data[2]), int(data[3]), int(data[4])]
                                        exam_mark = int(data[5])
                                        
                                        if (1000 <= student_id <= 9999 and 
                                            len(name) > 0 and 
                                            all(0 <= mark <= 20 for mark in coursework_marks) and 
                                            0 <= exam_mark <= 100):
                                                
                                            self.students.append(Student(student_id, name, coursework_marks, exam_mark))
                                        else:
                                            print(f"Skipping invalid student record on line {i+1}")
                                    except ValueError as e:
                                        print(f"Error processing student data on line {i+1}: {e}")
                                        continue

                    print(f"Successfully loaded {len(self.students)} students")
                    self.filename = text_filename
                    loaded = True
                    break
                
            except Exception as e:
                print(f"Error loading {text_filename}: {e}")
                continue
        
        if not loaded:
            print("No student data file found, starting with empty database")
            self.students = []
    
    def save_data(self):
        try:
            text_file_path = self.script_dir / self.filename
            
            with open(text_file_path, 'w') as file:
                file.write(f"{len(self.students)}\n")
                
                for student in self.students:
                    file.write(student.to_file_format() + "\n")
            
            print(f"Saved {len(self.students)} students to {self.filename}")
            return True
        except Exception as e:
            print(f"Error saving student data: {e}")
            raise
    
    def add_student(self, student: Student):
        if any(s.student_id == student.student_id for s in self.students):
            raise ValueError(f"Student ID {student.student_id} already exists")
        
        self.students.append(student)
        self.save_data()
    
    def remove_student(self, student_id: int):
        initial_count = len(self.students)
        self.students = [s for s in self.students if s.student_id != student_id]
        if len(self.students) < initial_count:
            self.save_data()
            return True
        return False
    
    def update_student(self, student_id: int, updated_student: Student):
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                self.students[i] = updated_student
                self.save_data()
                return True
        return False
    
    def get_student(self, student_id: int) -> Student:
        for student in self.students:
            if student.student_id == student_id:
                return student
        raise ValueError(f"Student ID {student_id} not found")
    
    def get_all_students(self) -> List[Student]:
        return self.students.copy()
    
    def get_highest_scoring_student(self) -> Student:
        if not self.students:
            raise ValueError("No students available")
        return max(self.students, key=lambda s: s.percentage)
    
    def get_lowest_scoring_student(self) -> Student:
        if not self.students:
            raise ValueError("No students available")
        return min(self.students, key=lambda s: s.percentage)
    
    def get_average_percentage(self) -> float:
        if not self.students:
            return 0.0
        return sum(student.percentage for student in self.students) / len(self.students)
    
    def get_grade_distribution(self) -> Dict[str, int]:
        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for student in self.students:
            distribution[student.grade] += 1
        return distribution
    
    def search_students(self, query: str) -> List[Student]:
        query = query.lower()
        results = []
        for student in self.students:
            if (query in student.name.lower() or 
                query in str(student.student_id)):
                results.append(student)
        return results

class ModernLoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        self.harvard_crimson = '#A41034'
        self.harvard_crimson_dark = '#8A0D2C'
        self.harvard_gray = '#8C8C8C'
        self.harvard_light_gray = '#F5F5F5'
        self.harvard_dark_gray = '#4A4A4A'
        self.harvard_gold = '#FFD700'
        
        self.primary_color = self.harvard_crimson
        self.primary_dark = self.harvard_crimson_dark
        self.secondary_color = self.harvard_gray
        self.background_gradient = [self.harvard_crimson, self.harvard_crimson_dark]
        self.card_bg = '#ffffff'
        self.text_primary = self.harvard_dark_gray
        self.text_secondary = self.harvard_gray
        self.shadow_color = '#E0E0E0'
        self.light_bg = self.harvard_light_gray
        
        self.images = {}
        self.load_images()
        
        self.setup_modern_login_page()
    
    def load_images(self):
        try:
            logo_path = Path(__file__).resolve().parent / "harvard logo.png"
            if logo_path.exists():
                original_logo = Image.open(logo_path)
                resized_logo = original_logo.resize((180, 180), Image.Resampling.LANCZOS)
                
                mask = Image.new('L', (180, 180), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 180, 180), fill=255)
                
                circular_logo = Image.new('RGBA', (180, 180), (0, 0, 0, 0))
                circular_logo.paste(resized_logo, (0, 0), mask)
                self.images['logo_circular'] = ImageTk.PhotoImage(circular_logo)
            else:
                self.images['logo_circular'] = None
                
            background_path = Path(__file__).resolve().parent / "background.png"
            if background_path.exists():
                original_bg = Image.open(background_path)
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                resized_bg = original_bg.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
                self.images['background'] = ImageTk.PhotoImage(resized_bg)
            else:
                self.images['background'] = None
                
        except Exception as e:
            print(f"Could not load images: {e}")
            self.images['logo_circular'] = None
            self.images['background'] = None
    
    def create_gradient_bg(self, width, height, colors):
        base = Image.new('RGB', (width, height), colors[0])
        top = Image.new('RGB', (width, height), colors[1])
        mask = Image.new('L', (width, height))
        mask_data = []
        for y in range(height):
            for x in range(width):
                mask_data.append(int(255 * (x / width)))
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return ImageTk.PhotoImage(base)
    
    def setup_modern_login_page(self):
        self.root.title("Harvard University - Student Management System")
        self.root.geometry("1200x800")
        
        if self.images['background']:
            bg_label = tk.Label(self.root, image=self.images['background'])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = self.images['background']
        else:
            self.root.configure(bg=self.primary_color)
            gradient_bg = self.create_gradient_bg(1200, 800, self.background_gradient)
            bg_label = tk.Label(self.root, image=gradient_bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = gradient_bg
        
        main_container = tk.Frame(self.root, bg='white', relief='flat', bd=0)
        main_container.place(relx=0.5, rely=0.5, anchor='center', width=900, height=600)
        
        shadow_frame = tk.Frame(main_container, bg=self.shadow_color, relief='flat')
        shadow_frame.place(x=5, y=5, relwidth=1, relheight=1)
        
        content_frame = tk.Frame(main_container, bg=self.card_bg, relief='flat')
        content_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        left_frame = tk.Frame(content_frame, bg=self.primary_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = tk.Frame(content_frame, bg=self.card_bg)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        left_content = tk.Frame(left_frame, bg=self.primary_color)
        left_content.place(relx=0.5, rely=0.5, anchor='center')
        
        if self.images['logo_circular']:
            logo_label = tk.Label(left_content, image=self.images['logo_circular'], bg=self.primary_color)
            logo_label.pack(pady=(0, 20))
        else:
            modern_icon = tk.Label(left_content, text="🎓", font=('Arial', 72), 
                                     bg=self.primary_color, fg='white')
            modern_icon.pack(pady=(0, 20))
        
        title_label = tk.Label(left_content, 
                              text="HARVARD", 
                              font=('Times New Roman', 32, 'bold'),
                              fg='white',
                              bg=self.primary_color)
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(left_content,
                                 text="Student Management",
                                 font=('Times New Roman', 18, 'normal'),
                                 fg='white',
                                 bg=self.primary_color)
        subtitle_label.pack()
        
        form_container = tk.Frame(right_frame, bg=self.card_bg)
        form_container.pack(expand=True, fill=tk.BOTH)
        
        welcome_label = tk.Label(form_container,
                                 text="Welcome Back",
                                 font=('Times New Roman', 28, 'bold'),
                                 fg=self.text_primary,
                                 bg=self.card_bg)
        welcome_label.pack(pady=(0, 10))
        
        instruction_label = tk.Label(form_container,
                                     text="Enter your access code to continue",
                                     font=('Times New Roman', 12),
                                     fg=self.text_secondary,
                                     bg=self.card_bg)
        instruction_label.pack(pady=(0, 40))
        
        input_frame = tk.Frame(form_container, bg=self.card_bg)
        input_frame.pack(pady=20)
        
        code_label = tk.Label(input_frame,
                              text="ACCESS CODE",
                              font=('Times New Roman', 10, 'bold'),
                              fg=self.text_secondary,
                              bg=self.card_bg)
        code_label.pack(anchor='w', pady=(0, 8))
        
        self.access_code = tk.StringVar()
        code_entry = tk.Entry(input_frame,
                              textvariable=self.access_code,
                              font=('Times New Roman', 14),
                              width=25,
                              justify='left',
                              relief='flat',
                              bd=0,
                              bg=self.light_bg,
                              fg=self.text_primary)
        code_entry.pack(fill=tk.X, pady=(0, 10), ipady=12)
        
        underline = tk.Frame(input_frame, bg=self.primary_color, height=2)
        underline.pack(fill=tk.X)
        
        hint_label = tk.Label(input_frame,
                              text="💡 Hint: Enter 'VERITAS' to access the system",
                              font=('Times New Roman', 9),
                              fg=self.text_secondary,
                              bg=self.card_bg)
        hint_label.pack(anchor='w', pady=(10, 0))
        
        login_btn = tk.Button(form_container,
                              text="🔓 ACCESS SYSTEM",
                              command=self.verify_access,
                              font=('Times New Roman', 12, 'bold'),
                              bg=self.primary_color,
                              fg='white',
                              activebackground=self.primary_dark,
                              activeforeground='white',
                              relief='flat',
                              bd=0,
                              cursor='hand2',
                              padx=30,
                              pady=15)
        login_btn.pack(pady=30)
        
        def on_enter(e):
            login_btn.config(bg=self.primary_dark)
        def on_leave(e):
            login_btn.config(bg=self.primary_color)
        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)
        
        footer_label = tk.Label(form_container,
                                 text="Harvard University • Established 1636 • Veritas",
                                 font=('Times New Roman', 9),
                                 fg=self.text_secondary,
                                 bg=self.card_bg)
        footer_label.pack(side=tk.BOTTOM, pady=20)
        
        code_entry.bind('<Return>', lambda e: self.verify_access())
        code_entry.focus()
    
    def verify_access(self):
        access_code = self.access_code.get().strip().upper()
        
        if access_code == "VERITAS":
            self.animate_success()
            self.root.after(1500, self.on_login_success)
        else:
            messagebox.showerror("Access Denied",
                                 "❌ Invalid access code\n\n"
                                 "Please enter 'VERITAS' to continue")
            self.access_code.set("")
            self.shake_login()
    
    def animate_success(self):
        success_window = tk.Toplevel(self.root)
        success_window.overrideredirect(True)
        success_window.geometry("300x200")
        success_window.configure(bg='white', relief='flat')
        
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        success_window.geometry(f"300x200+{x}+{y}")
        
        content = tk.Frame(success_window, bg='white')
        content.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        check_label = tk.Label(content, text="✅", font=('Arial', 48), bg='white')
        check_label.pack(pady=20)
        
        success_label = tk.Label(content, 
                                 text="Access Granted!",
                                 font=('Times New Roman', 16, 'bold'),
                                 fg=self.primary_color,
                                 bg='white')
        success_label.pack()
        
        loading_label = tk.Label(content,
                                 text="Loading system...",
                                 font=('Times New Roman', 10),
                                 fg=self.text_secondary,
                                 bg='white')
        loading_label.pack(pady=10)
        
        success_window.after(1200, success_window.destroy)
    
    def shake_login(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        
        for i in range(0, 5):
            for dx in [8, -8, 8, -8, 0]:
                self.root.geometry(f"+{x+dx}+{y}")
                self.root.update()
                self.root.after(30)

class ModernStudentManagerApp:
    def __init__(self, root):
        self.root = root
        
        self.harvard_crimson = '#A41034'
        self.harvard_crimson_dark = '#8A0D2C'
        self.harvard_gray = '#8C8C8C'
        self.harvard_light_gray = '#F5F5F5'
        self.harvard_dark_gray = '#4A4A4A'
        self.harvard_gold = '#FFD700'
        
        self.primary_color = self.harvard_crimson
        self.primary_dark = self.harvard_crimson_dark
        self.secondary_color = self.harvard_gray
        self.sidebar_color = '#2C3E50'
        self.sidebar_accent = '#34495E'
        self.card_bg = '#ffffff'
        self.background_color = self.harvard_light_gray
        self.text_primary = self.harvard_dark_gray
        self.text_secondary = self.harvard_gray
        self.success_color = '#27AE60'
        self.warning_color = '#E67E22'
        self.error_color = '#E74C3C'
        
        self.grade_colors = {
            'A': '#2E8B57',
            'B': '#4169E1',
            'C': '#FF8C00',
            'D': '#DA70D6',
            'F': '#DC143C'
        }
        
        self.root.title("🎓 Harvard University - Student Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.background_color)
        
        self.manager = StudentManager()
        
        self.images = {}
        self.load_images()
        
        self.show_modern_login_page()
    
    def set_dialog_icon(self, dialog: tk.Toplevel):
        if self.images.get('logo'):
            try:
                dialog.iconphoto(False, self.images['logo'])
            except tk.TclError as e:
                pass

    def show_modern_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.login_page = ModernLoginPage(self.root, self.on_login_success)
    
    def on_login_success(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.setup_modern_ui()
        self.view_all_students()
    
    def load_images(self):
        try:
            logo_path = self.manager.script_dir / "harvard logo.png"
            if logo_path.exists():
                original_logo = Image.open(logo_path)
                resized_logo = original_logo.resize((60, 60), Image.Resampling.LANCZOS)
                self.images['logo'] = ImageTk.PhotoImage(resized_logo)
                self.root.iconphoto(False, self.images['logo'])
            else:
                self.images['logo'] = None
        except Exception as e:
            print(f"Could not load logo image: {e}")
            self.images['logo'] = None
    
    def setup_modern_ui(self):
        main_container = tk.Frame(self.root, bg=self.background_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.setup_modern_header(main_container)
        
        content_frame = tk.Frame(main_container, bg=self.background_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.setup_modern_sidebar(content_frame)
        
        self.setup_modern_main_content(content_frame)
    
    def setup_modern_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 0))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=self.primary_color)
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        title_frame = tk.Frame(header_content, bg=self.primary_color)
        title_frame.pack(side=tk.LEFT)
        
        if self.images['logo']:
            logo_label = tk.Label(title_frame, image=self.images['logo'], bg=self.primary_color)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        text_stack_frame = tk.Frame(title_frame, bg=self.primary_color)
        text_stack_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        harvard_label = tk.Label(text_stack_frame,
                                 text="Harvard University",
                                 font=('Times New Roman', 20, 'bold'),
                                 fg='white',
                                 bg=self.primary_color,
                                 anchor='w')
        harvard_label.pack(fill=tk.X, anchor='w')
        
        system_label = tk.Label(text_stack_frame,
                                 text="Student Management System",
                                 font=('Times New Roman', 12),
                                 fg='white',
                                 bg=self.primary_color,
                                 anchor='w')
        system_label.pack(fill=tk.X, anchor='w')
        
        stats_frame = tk.Frame(header_content, bg=self.primary_color)
        stats_frame.pack(side=tk.RIGHT)
        
        self.stats_label = tk.Label(stats_frame,
                                      text="",
                                      font=('Times New Roman', 10, 'bold'),
                                      fg='white',
                                      bg=self.primary_color,
                                      justify=tk.RIGHT)
        self.stats_label.pack()
        self.update_stats()
    
    def setup_modern_sidebar(self, parent):
        sidebar_frame = tk.Frame(parent, bg=self.sidebar_color, width=280, relief='flat')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 0))
        sidebar_frame.pack_propagate(False)
        
        sidebar_header = tk.Frame(sidebar_frame, bg=self.sidebar_color, height=100)
        sidebar_header.pack(fill=tk.X, pady=(0, 10))
        sidebar_header.pack_propagate(False)
        
        sidebar_title_frame = tk.Frame(sidebar_header, bg=self.sidebar_color)
        sidebar_title_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        sidebar_title = tk.Label(sidebar_title_frame,
                                 text="NAVIGATION",
                                 font=('Times New Roman', 16, 'bold'),
                                 fg=self.harvard_gold,
                                 bg=self.sidebar_color)
        sidebar_title.pack()
        
        nav_container = tk.Frame(sidebar_frame, bg=self.sidebar_color)
        nav_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        nav_buttons = [
            ("📊 Dashboard", self.view_all_students),
            ("🔍 Search Students", self.search_students_dialog),
            ("👤 Student Profile", self.view_individual_student),
            ("🏆 Top Performers", self.show_highest_student),
            ("📈 Analytics", self.show_statistics),
            ("🎓 Grade Distribution", self.show_grade_distribution),
            ("➕ Add Student", self.add_student_dialog),
            ("✏️ Edit Student", self.update_student_dialog),
            ("🗑️ Remove Student", self.remove_student_dialog),
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn_frame = tk.Frame(nav_container, bg=self.sidebar_color)
            btn_frame.pack(fill=tk.X, padx=5, pady=2)
            
            btn_bg = self.sidebar_accent if i % 2 == 0 else self.sidebar_color
            
            btn = tk.Button(btn_frame, 
                          text=text, 
                          command=command,
                          font=('Times New Roman', 11, 'bold'),
                          bg=btn_bg,
                          fg='white',
                          activebackground=self.primary_color,
                          activeforeground='white',
                          relief='flat',
                          anchor='w',
                          padx=15,
                          pady=10,
                          cursor='hand2')
            btn.pack(fill=tk.X)
            
            def make_hover_effect(button, normal_bg):
                def on_enter(e):
                    button.config(bg=self.primary_color)
                def on_leave(e):
                    button.config(bg=normal_bg)
                return on_enter, on_leave
            
            on_enter, on_leave = make_hover_effect(btn, btn_bg)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        bottom_frame = tk.Frame(sidebar_frame, bg=self.sidebar_color)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        red_color = '#DC143C'
        red_dark = '#B22222'
        
        actions = [
            ("💾 Export Data", self.export_data),
            ("🔄 Refresh Data", self.refresh_data),
        ]
        
        for text, command in actions:
            action_frame = tk.Frame(bottom_frame, bg=self.sidebar_color)
            action_frame.pack(fill=tk.X, padx=10, pady=3)
            
            btn_color = red_color
            hover_color = red_dark
            
            action_btn = tk.Button(action_frame,
                                 text=text,
                                 command=command,
                                 font=('Times New Roman', 11, 'bold'),
                                 bg=btn_color,
                                 fg='white',
                                 activebackground=hover_color,
                                 relief='flat',
                                 pady=10,
                                 cursor='hand2')
            action_btn.pack(fill=tk.X)
            
            def make_action_hover(button, normal, hover):
                def on_enter(e):
                    button.config(bg=hover)
                def on_leave(e):
                    button.config(bg=normal)
                return on_enter, on_leave
            
            on_enter, on_leave = make_action_hover(action_btn, btn_color, hover_color)
            action_btn.bind("<Enter>", on_enter)
            action_btn.bind("<Leave>", on_leave)
    
    def setup_modern_main_content(self, parent):
        main_content = tk.Frame(parent, bg=self.background_color)
        main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content_header = tk.Frame(main_content, bg=self.card_bg, height=60, relief='flat')
        content_header.pack(fill=tk.X, pady=(0, 20))
        content_header.pack_propagate(False)
        
        self.content_title = tk.Label(content_header,
                                      text="Student Dashboard",
                                      font=('Times New Roman', 18, 'bold'),
                                      fg=self.primary_color,
                                      bg=self.card_bg)
        self.content_title.pack(expand=True)
        
        text_container = tk.Frame(main_content, bg=self.card_bg, relief='flat')
        text_container.pack(fill=tk.BOTH, expand=True)
        
        self.text_display = tk.Text(text_container,
                                     wrap=tk.WORD,
                                     font=('Consolas', 11),
                                     bg=self.card_bg,
                                     fg=self.text_primary,
                                     padx=25,
                                     pady=25,
                                     relief='flat',
                                     bd=0)
        
        scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.text_display.yview)
        self.text_display.configure(yscrollcommand=scrollbar.set)
        
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_display.config(state=tk.DISABLED)
    
    def update_stats(self):
        students = self.manager.get_all_students()
        if students:
            try:
                avg_percentage = self.manager.get_average_percentage()
                highest = self.manager.get_highest_scoring_student()
                stats_text = f"👥 {len(students)} Students | 📊 Avg: {avg_percentage:.1f}% | 🏆 Best: {highest.percentage:.1f}%"
            except ValueError:
                stats_text = f"👥 {len(students)} Students | 📊 Analyzing..."
        else:
            stats_text = "👥 No students in database"
        self.stats_label.config(text=stats_text)
    
    def display_text(self, text: str, title: str = "Dashboard"):
        self.content_title.config(text=title)
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        
        formatted_text = self.apply_modern_formatting(text)
        self.text_display.insert(1.0, formatted_text)
        
        self.text_display.config(state=tk.DISABLED)
        self.update_stats()
    
    def apply_modern_formatting(self, text: str) -> str:
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if any(keyword in line for keyword in ['ALL STUDENT RECORDS', 'CLASS SUMMARY', 'TOP PERFORMERS', 'CLASS STATISTICS', 'GRADE DISTRIBUTION']):
                line = f"🎓 {line}"
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def format_student_info(self, student: Student) -> str:
        grade_emoji = {
            'A': '🟢', 'B': '🔵', 'C': '🟡', 'D': '🟠', 'F': '🔴'
        }
        
        return f"""👤 {student.name}
#️⃣ ID: {student.student_id}
📝 Coursework: {student.coursework_marks} (Total: {student.total_coursework}/60)
✏️ Exam: {student.exam_mark}/100
📈 Overall: {student.percentage:.2f}% ({student.total_marks}/160)
{grade_emoji.get(student.grade, '⚪')} Grade: {student.grade}
{'─' * 50}
"""
    
    def view_all_students(self):
        students = self.manager.get_all_students()
        
        if not students:
            self.display_text("⭐ No students found in the database. Add some students to get started! ⭐", "Dashboard")
            return
        
        output = "🎓 ALL STUDENT RECORDS\n"
        output += "════════════════════════════════════════════════════════════════════════════════\n\n"
        
        students_sorted = sorted(students, key=lambda s: s.percentage, reverse=True)
        
        for i, student in enumerate(students_sorted, 1):
            rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i:2d}."
            output += f"{rank_icon} {self.format_student_info(student)}"
        
        output += f"\n🎓 CLASS SUMMARY\n"
        output += "════════════════════════════════════════════════════════════════\n"
        output += f"👥 Total Students: {len(students)}\n"
        output += f"📈 Average Percentage: {self.manager.get_average_percentage():.2f}%\n"
        
        try:
            highest = self.manager.get_highest_scoring_student()
            lowest = self.manager.get_lowest_scoring_student()
            output += f"🥇 Highest Score: {highest.percentage:.2f}% ({highest.name})\n"
            output += f"📉 Lowest Score: {lowest.percentage:.2f}% ({lowest.name})\n"
        except ValueError:
            output += f"🥇 Highest Score: N/A\n"
            output += f"📉 Lowest Score: N/A\n"
        
        self.display_text(output, "Student Dashboard")
    
    def search_students_dialog(self):
        students = self.manager.get_all_students()
        
        if not students:
            messagebox.showwarning("No Students", "No students found in the database.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Search Students")
        self.set_dialog_icon(dialog)
        dialog.geometry("400x300")
        dialog.configure(bg=self.background_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        content_frame = tk.Frame(dialog, bg=self.card_bg, relief='flat', padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(content_frame,
                              text="🔍 Search Students",
                              font=('Times New Roman', 16, 'bold'),
                              fg=self.primary_color,
                              bg=self.card_bg)
        title_label.pack(pady=(0, 20))
        
        instruction_label = tk.Label(content_frame,
                                     text="Enter student name or ID:",
                                     font=('Times New Roman', 11),
                                     fg=self.text_secondary,
                                     bg=self.card_bg)
        instruction_label.pack(anchor='w', pady=(0, 8))
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(content_frame,
                                textvariable=search_var,
                                font=('Times New Roman', 12),
                                relief='flat',
                                bg=self.background_color,
                                fg=self.text_primary)
        search_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        underline = tk.Frame(content_frame, bg=self.primary_color, height=2)
        underline.pack(fill=tk.X, pady=(0, 20))
        
        def perform_search():
            query = search_var.get().strip()
            if not query:
                messagebox.showwarning("Empty Search", "Please enter a search term.")
                return
            
            results = self.manager.search_students(query)
            dialog.destroy()
            
            if results:
                output = f"🎓 SEARCH RESULTS FOR: '{query}'\n"
                output += "════════════════════════════════════════════════════════════════\n\n"
                for student in results:
                    output += self.format_student_info(student)
                self.display_text(output, f"Search Results ({len(results)} found)")
            else:
                messagebox.showinfo("No Results", f"No students found matching '{query}'")
        
        search_btn_frame = tk.Frame(content_frame, bg=self.card_bg)
        search_btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        search_btn = tk.Button(search_btn_frame,
                              text="🔍 SEARCH",
                              command=perform_search,
                              font=('Times New Roman', 12, 'bold'),
                              bg=self.primary_color,
                              fg='white',
                              relief='flat',
                              pady=12)
        search_btn.pack(fill=tk.X, pady=10)
        
        search_entry.bind('<Return>', lambda e: perform_search())
        search_entry.focus()
    
    def view_individual_student(self):
        students = self.manager.get_all_students()
        
        if not students:
            messagebox.showwarning("No Students", "No students found in the database.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("View Student Profile")
        self.set_dialog_icon(dialog)
        dialog.geometry("400x300")
        dialog.configure(bg=self.background_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        content_frame = tk.Frame(dialog, bg=self.card_bg, relief='flat', padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(content_frame,
                              text="👤 View Student Profile",
                              font=('Times New Roman', 16, 'bold'),
                              fg=self.primary_color,
                              bg=self.card_bg)
        title_label.pack(pady=(0, 20))
        
        instruction_label = tk.Label(content_frame,
                                     text="Enter Student ID:",
                                     font=('Times New Roman', 11),
                                     fg=self.text_secondary,
                                     bg=self.card_bg)
        instruction_label.pack(anchor='w', pady=(0, 8))
        
        id_var = tk.StringVar()
        id_entry = tk.Entry(content_frame,
                            textvariable=id_var,
                            font=('Times New Roman', 12),
                            relief='flat',
                            bg=self.background_color,
                            fg=self.text_primary)
        id_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        underline = tk.Frame(content_frame, bg=self.primary_color, height=2)
        underline.pack(fill=tk.X, pady=(0, 20))
        
        def view_student():
            try:
                student_id = int(id_var.get().strip())
                student = self.manager.get_student(student_id)
                dialog.destroy()
                
                output = f"🎓 STUDENT PROFILE\n"
                output += "════════════════════════════════════════════════════════════════\n\n"
                output += self.format_student_info(student)
                output += f"\n🎓 DETAILED BREAKDOWN\n"
                output += "────────────────────────────────────────────────\n"
                output += f"Assignment 1: {student.coursework_marks[0]}/20\n"
                output += f"Assignment 2: {student.coursework_marks[1]}/20\n"
                output += f"Assignment 3: {student.coursework_marks[2]}/20\n"
                output += f"Coursework Total: {student.total_coursework}/60\n"
                output += f"Exam: {student.exam_mark}/100\n"
                output += f"Overall: {student.total_marks}/160\n"
                
                self.display_text(output, f"Student: {student.name}")
                
            except ValueError:
                messagebox.showerror("Invalid ID", "Please enter a valid numeric Student ID")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        view_btn_frame = tk.Frame(content_frame, bg=self.card_bg)
        view_btn_frame.pack(fill=tk.X, pady=(40, 0))
        
        view_btn = tk.Button(view_btn_frame,
                              text="👤 VIEW PROFILE",
                              command=view_student,
                              font=('Times New Roman', 12, 'bold'),
                              bg=self.primary_color,
                              fg='white',
                              relief='flat',
                              pady=12)
        view_btn.pack(fill=tk.X, pady=10)
        
        id_entry.bind('<Return>', lambda e: view_student())
        id_entry.focus()
    
    def show_highest_student(self):
        try:
            highest = self.manager.get_highest_scoring_student()
            lowest = self.manager.get_lowest_scoring_student()
            
            output = f"🎓 TOP PERFORMERS\n"
            output += "════════════════════════════════════════════════════════════════\n\n"
            
            output += f"🎓 HIGHEST SCORING STUDENT\n"
            output += "────────────────────────────────────────────────\n"
            output += self.format_student_info(highest)
            
            output += f"\n🎓 LOWEST SCORING STUDENT\n"
            output += "────────────────────────────────────────────────\n"
            output += self.format_student_info(lowest)
            
            output += f"\n🎓 PERFORMANCE GAP\n"
            output += "────────────────────────────────────────────────\n"
            gap = highest.percentage - lowest.percentage
            output += f"Difference: {gap:.2f}%\n"
            
            self.display_text(output, "Top Performers")
            
        except ValueError as e:
            messagebox.showwarning("No Data", str(e))
    
    def show_statistics(self):
        students = self.manager.get_all_students()
        
        if not students:
            messagebox.showwarning("No Students", "No students found in the database.")
            return
        
        avg_percentage = self.manager.get_average_percentage()
        
        output = f"🎓 CLASS STATISTICS\n"
        output += "════════════════════════════════════════════════════════════════\n\n"
        
        output += f"🎓 OVERVIEW\n"
        output += "────────────────────────────────────────────────\n"
        output += f"👥 Total Students: {len(students)}\n"
        output += f"📈 Average Percentage: {avg_percentage:.2f}%\n\n"
        
        try:
            highest = self.manager.get_highest_scoring_student()
            lowest = self.manager.get_lowest_scoring_student()
            
            output += f"🎓 PERFORMANCE RANGE\n"
            output += "────────────────────────────────────────────────\n"
            output += f"🥇 Highest: {highest.percentage:.2f}% ({highest.name})\n"
            output += f"📉 Lowest: {lowest.percentage:.2f}% ({lowest.name})\n"
            output += f"📏 Range: {highest.percentage - lowest.percentage:.2f}%\n\n"
        except ValueError:
            output += f"Performance data not available\n\n"
        
        distribution = self.manager.get_grade_distribution()
        output += f"🎓 GRADE DISTRIBUTION\n"
        output += "────────────────────────────────────────────────\n"
        for grade, count in distribution.items():
            percentage = (count / len(students)) * 100 if students else 0
            output += f"{grade}: {count} students ({percentage:.1f}%)\n"
        
        self.display_text(output, "Class Statistics")
    
    def show_grade_distribution(self):
        students = self.manager.get_all_students()
        
        if not students:
            messagebox.showwarning("No Students", "No students found in the database.")
            return
        
        distribution = self.manager.get_grade_distribution()
        
        output = f"🎓 GRADE DISTRIBUTION\n"
        output += "════════════════════════════════════════════════════════════════\n\n"
        
        total_students = len(students)
        
        for grade, count in distribution.items():
            percentage = (count / total_students) * 100
            bar = "█" * int((count / total_students) * 30)
            output += f"{grade}: {bar} {count} ({percentage:.1f}%)\n"
        
        output += f"\n🎓 SUMMARY\n"
        output += "────────────────────────────────────────────────\n"
        output += f"Total Students: {total_students}\n"
        
        most_common = max(distribution.items(), key=lambda x: x[1])
        output += f"Most Common Grade: {most_common[0]} ({most_common[1]} students)\n"
        
        self.display_text(output, "Grade Distribution")
    
    def add_student_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        self.set_dialog_icon(dialog)
        dialog.geometry("500x650")
        dialog.configure(bg=self.background_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = tk.Frame(dialog, bg=self.background_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content_frame = tk.Frame(main_frame, bg=self.card_bg, relief='flat', padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(content_frame,
                              text="➕ Add New Student",
                              font=('Times New Roman', 18, 'bold'),
                              fg=self.primary_color,
                              bg=self.card_bg)
        title_label.pack(pady=(0, 20))
        
        canvas = tk.Canvas(content_frame, bg=self.card_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.card_bg)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        fields = [
            ("🎓 Student ID (1000-9999)", "id"),
            ("👤 Full Name", "name"),
            ("📝 Task 1 Mark (0-20)", "task1"),
            ("📝 Task 2 Mark (0-20)", "task2"), 
            ("📝 Task 3 Mark (0-20)", "task3"),
            ("✏️ Exam Mark (0-100)", "exam")
        ]
        
        entries = {}
        
        for label_text, field_name in fields:
            frame = tk.Frame(scrollable_frame, bg=self.card_bg)
            frame.pack(fill=tk.X, pady=12)
            
            label = tk.Label(frame,
                             text=label_text,
                             font=('Times New Roman', 11, 'bold'),
                             fg=self.text_primary,
                             bg=self.card_bg,
                             anchor='w')
            label.pack(fill=tk.X, pady=(0, 8))
            
            var = tk.StringVar()
            entry = tk.Entry(frame,
                             textvariable=var,
                             font=('Times New Roman', 12),
                             relief='flat',
                             bg=self.background_color,
                             fg=self.text_primary,
                             justify='left')
            entry.pack(fill=tk.X, pady=(0, 8), ipady=10)
            
            underline = tk.Frame(frame, bg=self.primary_color, height=2)
            underline.pack(fill=tk.X)
            
            entries[field_name] = var
        
        button_container = tk.Frame(scrollable_frame, bg=self.card_bg)
        button_container.pack(fill=tk.X, pady=(30, 20))
        
        add_btn = tk.Button(button_container,
                            text="➕ ADD STUDENT",
                            command=lambda: self.add_student_action(entries, dialog),
                            font=('Times New Roman', 14, 'bold'),
                            bg=self.success_color,
                            fg='white',
                            relief='flat',
                            pady=15,
                            cursor='hand2')
        add_btn.pack(fill=tk.X, pady=10)
        
        def on_enter(e):
            add_btn.config(bg='#228B22')
        def on_leave(e):
            add_btn.config(bg=self.success_color)
        add_btn.bind("<Enter>", on_enter)
        add_btn.bind("<Leave>", on_leave)
        
        def update_scrollregion():
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        dialog.after(100, update_scrollregion)
        
        dialog.bind('<Return>', lambda e: self.add_student_action(entries, dialog))
        
        entries['id'].set("")
        for widget in scrollable_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Entry):
                        child.focus_set()
                        return
    
    def add_student_action(self, entries, dialog):
        try:
            student_id = int(entries['id'].get().strip())
            name = entries['name'].get().strip()
            task1 = int(entries['task1'].get().strip())
            task2 = int(entries['task2'].get().strip())
            task3 = int(entries['task3'].get().strip())
            exam = int(entries['exam'].get().strip())
            
            if not (1000 <= student_id <= 9999):
                raise ValueError("Student ID must be between 1000 and 9999")
            if not name:
                raise ValueError("Name cannot be empty")
            if not all(0 <= mark <= 20 for mark in [task1, task2, task3]):
                raise ValueError("Task marks must be between 0 and 20")
            if not (0 <= exam <= 100):
                raise ValueError("Exam mark must be between 0 and 100")
            
            student = Student(student_id, name, [task1, task2, task3], exam)
            self.manager.add_student(student)
            
            dialog.destroy()
            messagebox.showinfo("Success", f"✅ Student {name} added successfully!")
            self.view_all_students()
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_student_dialog(self):
        students = self.manager.get_all_students()
        
        if not students:
            messagebox.showwarning("No Students", "No students found in the database.")
            return
        
        id_dialog = tk.Toplevel(self.root)
        id_dialog.title("Update Student")
        self.set_dialog_icon(id_dialog)
        id_dialog.geometry("400x300")
        id_dialog.configure(bg=self.background_color)
        id_dialog.transient(self.root)
        id_dialog.grab_set()
        
        id_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        content_frame = tk.Frame(id_dialog, bg=self.card_bg, relief='flat', padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(content_frame,
                              text="✏️ Update Student",
                              font=('Times New Roman', 16, 'bold'),
                              fg=self.primary_color,
                              bg=self.card_bg)
        title_label.pack(pady=(0, 20))
        
        instruction_label = tk.Label(content_frame,
                                     text="Enter Student ID to update:",
                                     font=('Times New Roman', 11),
                                     fg=self.text_secondary,
                                     bg=self.card_bg)
        instruction_label.pack(anchor='w', pady=(0, 8))
        
        id_var = tk.StringVar()
        id_entry = tk.Entry(content_frame,
                            textvariable=id_var,
                            font=('Times New Roman', 12),
                            relief='flat',
                            bg=self.background_color,
                            fg=self.text_primary)
        id_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        underline = tk.Frame(content_frame, bg=self.primary_color, height=2)
        underline.pack(fill=tk.X, pady=(0, 20))
        
        def find_student():
            try:
                student_id = int(id_var.get().strip())
                student = self.manager.get_student(student_id)
                id_dialog.destroy()
                self.show_update_form(student)
            except ValueError:
                messagebox.showerror("Invalid ID", "Please enter a valid numeric Student ID")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        find_btn_frame = tk.Frame(content_frame, bg=self.card_bg)
        find_btn_frame.pack(fill=tk.X, pady=(40, 0))
        
        find_btn = tk.Button(find_btn_frame,
                              text="🔍 FIND STUDENT",
                              command=find_student,
                              font=('Times New Roman', 12, 'bold'),
                              bg=self.primary_color,
                              fg='white',
                              relief='flat',
                              pady=12)
        find_btn.pack(fill=tk.X, pady=10)
        
        id_entry.bind('<Return>', lambda e: find_student())
        id_entry.focus()
    
    def show_update_form(self, student):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update {student.name}")
        self.set_dialog_icon(dialog)
        dialog.geometry("500x600")
        dialog.configure(bg=self.background_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        content_frame = tk.Frame(dialog, bg=self.card_bg, relief='flat', padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(content_frame,
                              text=f"✏️ Update {student.name}",
                              font=('Times New Roman', 18, 'bold'),
                              fg=self.primary_color,
                              bg=self.card_bg)
        title_label.pack(pady=(0, 30))
        
        current_info = tk.Label(content_frame,
                                 text=f"Current marks - Task 1: {student.coursework_marks[0]}, Task 2: {student.coursework_marks[1]}, Task 3: {student.coursework_marks[2]}, Exam: {student.exam_mark}",
                                 font=('Times New Roman', 10, 'bold'),
                                 fg=self.text_primary,
                                 bg=self.card_bg)
        current_info.pack(pady=(0, 20))
        
        fields = [
            ("📝 Task 1 Mark (0-20)", "task1", student.coursework_marks[0]),
            ("📝 Task 2 Mark (0-20)", "task2", student.coursework_marks[1]),
            ("📝 Task 3 Mark (0-20)", "task3", student.coursework_marks[2]),
            ("✏️ Exam Mark (0-100)", "exam", student.exam_mark)
        ]
        
        entries = {}
        
        for label_text, field_name, current_value in fields:
            frame = tk.Frame(content_frame, bg=self.card_bg)
            frame.pack(fill=tk.X, pady=8)
            
            label = tk.Label(frame,
                             text=label_text,
                             font=('Times New Roman', 10, 'bold'),
                             fg=self.text_primary,
                             bg=self.card_bg,
                             anchor='w')
            label.pack(fill=tk.X)
            
            var = tk.StringVar(value=str(current_value))
            entry = tk.Entry(frame,
                             textvariable=var,
                             font=('Times New Roman', 12, 'bold'),
                             relief='flat',
                             bg=self.background_color,
                             fg=self.text_primary)
            entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
            
            underline = tk.Frame(frame, bg=self.primary_color, height=2)
            underline.pack(fill=tk.X, pady=(5, 0))
            
            entries[field_name] = var
        
        def update_student():
            try:
                task1 = int(entries['task1'].get().strip())
                task2 = int(entries['task2'].get().strip())
                task3 = int(entries['task3'].get().strip())
                exam = int(entries['exam'].get().strip())
                
                if not all(0 <= mark <= 20 for mark in [task1, task2, task3]):
                    raise ValueError("Task marks must be between 0 and 20")
                if not (0 <= exam <= 100):
                    raise ValueError("Exam mark must be between 0 and 100")
                
                updated_student = Student(student.student_id, student.name, [task1, task2, task3], exam)
                self.manager.update_student(student.student_id, updated_student)
                
                dialog.destroy()
                messagebox.showinfo("Success", f"✅ Student {student.name} updated successfully!")
                self.view_all_students()
                
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        update_btn_frame = tk.Frame(content_frame, bg=self.card_bg)
        update_btn_frame.pack(fill=tk.X, pady=(40, 0))
        
        update_btn = tk.Button(update_btn_frame,
                              text="💾 UPDATE STUDENT",
                              command=update_student,
                              font=('Times New Roman', 12, 'bold'),
                              bg=self.warning_color,
                              fg='white',
                              relief='flat',
                              pady=12)
        update_btn.pack(fill=tk.X, pady=10)
    
    def remove_student_dialog(self):
        students = self.manager.get_all_students()
        
        if not students:
            messagebox.showwarning("No Students", "No students found in the database.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Student")
        self.set_dialog_icon(dialog)
        dialog.geometry("400x300")
        dialog.configure(bg=self.background_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        content_frame = tk.Frame(dialog, bg=self.card_bg, relief='flat', padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(content_frame,
                              text="🗑️ Remove Student",
                              font=('Times New Roman', 16, 'bold'),
                              fg=self.primary_color,
                              bg=self.card_bg)
        title_label.pack(pady=(0, 20))
        
        instruction_label = tk.Label(content_frame,
                                     text="Enter Student ID to remove:",
                                     font=('Times New Roman', 11),
                                     fg=self.text_secondary,
                                     bg=self.card_bg)
        instruction_label.pack(anchor='w', pady=(0, 8))
        
        id_var = tk.StringVar()
        id_entry = tk.Entry(content_frame,
                            textvariable=id_var,
                            font=('Times New Roman', 12),
                            relief='flat',
                            bg=self.background_color,
                            fg=self.text_primary)
        id_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        underline = tk.Frame(content_frame, bg=self.primary_color, height=2)
        underline.pack(fill=tk.X, pady=(0, 20))
        
        def remove_student():
            try:
                student_id = int(id_var.get().strip())
                student = self.manager.get_student(student_id)
                
                confirm = messagebox.askyesno(
                    "Confirm Removal",
                    f"Are you sure you want to remove {student.name} (ID: {student_id})?\n\nThis action cannot be undone."
                )
                
                if confirm:
                    if self.manager.remove_student(student_id):
                        dialog.destroy()
                        messagebox.showinfo("Success", f"✅ Student {student.name} removed successfully!")
                        self.view_all_students()
                    else:
                        messagebox.showerror("Error", "Failed to remove student")
                
            except ValueError:
                messagebox.showerror("Invalid ID", "Please enter a valid numeric Student ID")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        remove_btn_frame = tk.Frame(content_frame, bg=self.card_bg)
        remove_btn_frame.pack(fill=tk.X, pady=(40, 0))
        
        remove_btn = tk.Button(remove_btn_frame,
                              text="🗑️ REMOVE STUDENT",
                              command=remove_student,
                              font=('Times New Roman', 12, 'bold'),
                              bg=self.error_color,
                              fg='white',
                              relief='flat',
                              pady=12)
        remove_btn.pack(fill=tk.X, pady=10)
        
        id_entry.bind('<Return>', lambda e: remove_student())
        id_entry.focus()
    
    def export_data(self):
        students = self.manager.get_all_students()
        
        if not students:
            messagebox.showwarning("No Data", "No student data to export.")
            return
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            export_filename = f"student_export_{timestamp}.txt"
            export_path = self.manager.script_dir / export_filename
            
            with open(export_path, 'w') as file:
                file.write("🎓 Harvard University - Student Data Export\n")
                file.write("════════════════════════════════════════════════════════════════\n")
                file.write(f"Exported on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("════════════════════════════════════════════════════════════════\n\n")
                
                for student in students:
                    file.write(f"🎓 STUDENT PROFILE\n")
                    file.write(f"────────────────────────────────────────────────\n")
                    file.write(f"Student ID: {student.student_id}\n")
                    file.write(f"Name: {student.name}\n")
                    file.write(f"Task Marks: {student.coursework_marks}\n")
                    file.write(f"Exam Mark: {student.exam_mark}\n")
                    file.write(f"Total Marks: {student.total_marks}/160\n")
                    file.write(f"Percentage: {student.percentage:.2f}%\n")
                    file.write(f"Grade: {student.grade}\n")
                    file.write("────────────────────────────────────────────────\n\n")
            
            messagebox.showinfo("Export Successful", f"Student data exported to:\n{export_path}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export data: {str(e)}")
    
    def refresh_data(self):
        self.manager.load_data()
        self.view_all_students()
        messagebox.showinfo("Refreshed", "Student data has been refreshed from file.")

def main():
    root = tk.Tk()
    app = ModernStudentManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()