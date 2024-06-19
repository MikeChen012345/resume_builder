import os
import tkinter as tk
from tkinter import messagebox
from resume_builder import ResumeBuilder
from resume_improver import ResumeImprover
from resume_rater import ResumeRater

class ResumeBuilderGUI:
    def __init__(self, window):

        ## Header Section
        self.window = window
        self.window.title("Resume Builder")

        ## Sidebar Section
        self.sidebar = tk.Frame(window, width=200, bg='grey')
        self.sidebar.pack(expand=False, fill='both', side='left')

        # Button for filling in .env file: opens a new window with text boxes for the user to 
        # fill in the API URL and the API key
        self.fill_env_button = tk.Button(self.sidebar, text="Fill .env File", command=self.fill_env)
        self.fill_env_button.pack()

        # Button for loading/changing the resume PDF file: allows the user to select a new resume PDF file
        #self.load_resume_button = tk.Button(self.sidebar, text="Load Resume PDF", command=self.load_resume)
        #self.load_resume_button.pack()

        ## Main Section

        self.builder = ResumeBuilder()

        # Output filename
        self.filename_label = tk.Label(window, text="Output Filename:")
        self.filename_label.pack()
        self.filename_entry = tk.Entry(window)
        self.filename_entry.pack()

        # Preserve LaTeX file
        self.preserve_var = tk.BooleanVar()
        self.preserve_check = tk.Checkbutton(window, text="Preserve LaTeX file", variable=self.preserve_var)
        self.preserve_check.pack()

        # Generate button
        self.generate_button = tk.Button(window, text="Generate Resume", command=self.generate_resume)
        self.generate_button.pack()

        # Clean the output directory button
        self.clean_button = tk.Button(window, text="Clean Output Directory", command=self.clean_output_directory)
        self.clean_button.pack()

        # Resume improver and resume rater buttons, an input text box only for resume rater, 
        # and the feedback text box
        self.improve_button = tk.Button(window, text="Improve Resume", command=self.improve_resume)
        self.improve_button.pack()
        self.rate_button = tk.Button(window, text="Rate Resume", command=self.rate_resume)
        self.rate_button.pack()
        self.input_text_label = tk.Label(window, text="Input Text:")
        self.input_text_label.pack()
        self.input_text = tk.Text(window, height=10, width=50)
        self.input_text.pack()
        self.feedback_label = tk.Label(window, text="Feedback:")
        self.feedback_label.pack()
        self.feedback_text = tk.Text(window, height=10, width=50)
        self.feedback_text.pack()

    def fill_env(self):
        def save_env():
            with open('.env', 'w') as f:
                f.write(f"url={self.url_entry.get()}\n")
                f.write(f"auth_key={self.key_entry.get()}\n")
            messagebox.showinfo("Resume Builder", ".env file saved successfully! Please restart the application.")
            self.env_window.destroy()
        
        self.env_window = tk.Toplevel(self.window)
        self.env_window.title("Fill .env File")

        # API URL
        self.url_label = tk.Label(self.env_window, text="API URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.env_window)
        self.url_entry.pack()

        # API Key
        self.key_label = tk.Label(self.env_window, text="API Key:")
        self.key_label.pack()
        self.key_entry = tk.Entry(self.env_window)
        self.key_entry.pack()

        # Save button
        self.save_button = tk.Button(self.env_window, text="Save", command=save_env)
        self.save_button.pack()

    def generate_resume(self):
        output_filename = self.filename_entry.get()
        preserve_latex = self.preserve_var.get()

        # Load data from csv files
        self.builder.load_personal_info('data/personal_info.csv')
        self.builder.load_education('data/education.csv')
        self.builder.load_experience('data/experience.csv')
        self.builder.load_certifications('data/certifications.csv')
        self.builder.load_skills('data/skills.csv')

        # Generate the resume
        try:
            self.builder.generate_resume(output_filename, preserve_latex=preserve_latex)
            messagebox.showinfo("Resume Builder", "Resume generated successfully!")
        except Exception as e:
            messagebox.showerror("Resume Builder", f"Error: {e}")

    def clean_output_directory(self):
        self.builder.clean_output_directory()
        messagebox.showinfo("Resume Builder", "Output directory cleaned!")

    def improve_resume(self):
        content = self.builder.get_resume_content()
        if not self.builder.is_loaded:
            messagebox.showerror("Resume Builder", "Please generate a resume first!")
            return

        resume_improver = ResumeImprover()
        reply_text = resume_improver.get_advice(content)
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.insert(tk.END, reply_text)

        improve_resume_builder = ResumeBuilder()
        improve_resume_builder.load_resume_from_text(reply_text)
        improve_resume_builder.generate_resume("improved_resume", preserve_latex=False)

    def rate_resume(self):
        content = self.builder.get_resume_content()
        theme = self.input_text.get("1.0", tk.END)
        if not self.builder.is_loaded:
            messagebox.showerror("Resume Builder", "Please generate a resume first!")
            return

        if len(theme.strip()) == 0:
            messagebox.showerror("Resume Builder", "Please enter a theme in the input text box!")
            return

        resume_rater = ResumeRater()
        reply_text = resume_rater.get_advice(theme, content)
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.insert(tk.END, reply_text)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ResumeBuilderGUI(root)
    root.mainloop()