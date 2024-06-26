import os
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from resume_builder import ResumeBuilder
from resume_improver import ResumeImprover
from resume_rater import ResumeRater
from resume_latex_generator import ResumeLatexGenerator

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
        self.fill_env_button = tk.Button(self.sidebar, text="Fill .env File", command=self.fill_env, width=20, height=2)
        self.fill_env_button.pack()

        # Button for saving the current resume builder to a file
        self.save_button = tk.Button(self.sidebar, text="Save Resume Builder", command=self.save_state, width=20, height=2)
        self.save_button.pack()

        # Button for loading a resume builder from a file
        self.load_button = tk.Button(self.sidebar, text="Load Resume Builder", command=self.load_state, width=20, height=2)
        self.load_button.pack()

        # Clean the output directory button
        self.clean_button = tk.Button(self.sidebar, text="Clean Output Directory", command=self.clean_output_directory, width=20, height=2)
        self.clean_button.pack()

        # Clean the saved directory button
        self.clean_button = tk.Button(self.sidebar, text="Clean Saved Directory", command=self.clean_saved_directory, width=20, height=2)
        self.clean_button.pack()

        # Compile a resume PDF from LaTeX button
        self.compile_button = tk.Button(self.sidebar, text="Compile Resume PDF", command=self.compile_resume_from_latex, width=20, height=2)
        self.compile_button.pack()

        # Generate a resume PDF from a LaTeX template button
        self.generate_button = tk.Button(self.sidebar, text="Generate from Template", command=self.generate_resume_from_template_latex, width=20, height=2)
        self.generate_button.pack()

        ## Main Section

        self.builder = ResumeBuilder()

        # Output filename
        self.filename_label = tk.Label(window, text="Output Filename:")
        self.filename_label.pack()
        self.filename_entry = tk.Entry(window)
        self.filename_entry.pack()

        # Preserve LaTeX file
        self.preserve_var = tk.BooleanVar()
        self.preserve_check = tk.Checkbutton(window, text="Preserve LaTeX File", variable=self.preserve_var)
        self.preserve_check.pack()

        # Generate button
        self.generate_button = tk.Button(window, text="Generate Resume", command=self.generate_resume, width=20, height=2)
        self.generate_button.pack()

        # Resume improver and resume rater buttons, an input text box only for resume rater, 
        # and the feedback text box
        self.improve_button = tk.Button(window, text="Improve Resume", command=self.improve_resume, width=20, height=2)
        self.improve_button.pack()
        self.rate_button = tk.Button(window, text="Rate Resume", command=self.rate_resume, width=20, height=2)
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

    def save_state(self):
        filename = self.filename_entry.get()
        if len(filename.strip()) == 0:
            messagebox.showerror("Resume Builder", "Please enter a filename!")
            return
        if not self.builder.is_loaded:
            messagebox.showerror("Resume Builder", "Empty resume builder! Please generate a resume first!")
            return
        self.builder.save_resume_builder_pkl(filename)
        messagebox.showinfo("Resume Builder", "Resume builder state saved successfully!")
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.insert(tk.END, "Resume builder state saved successfully!")

    def load_state(self):
        filepath = filedialog.askopenfilename(initialdir="saved", title="Select file", filetypes=((".pkl files", "*.pkl"),))
        if len(filepath.strip()) == 0: # the user closed the dialog and didn't select a file
            return
        self.builder.load_resume_builder_pkl(filepath)
        messagebox.showinfo("Resume Builder", "Resume builder state loaded successfully!")
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.insert(tk.END, "Resume builder state loaded successfully!")

    def generate_resume(self):
        output_filename = self.filename_entry.get()
        if len(output_filename.strip()) == 0:
            messagebox.showerror("Resume Builder", "Please enter a filename for the output PDF in the Output Filename field!")
            return
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

    def clean_output_directory(self) -> bool:
        """
        Clean the output directory by removing all the generated PDF files.

        Returns:
            bool: True if the output directory was cleaned successfully.
        """
        for file in os.listdir("output"):
            os.remove(os.path.join("output", file))
        print("Output directory cleaned!")
        messagebox.showinfo("Resume Builder", "Output directory cleaned!")
        return True

    def clean_saved_directory(self) -> bool:
        """
        Clean the saved directory by removing all the saved resume builder files.

        Returns:
            bool: True if the saved directory was cleaned successfully.
        """
        for file in os.listdir("saved"):
            os.remove(os.path.join("saved", file))
        print("Saved directory cleaned!")
        messagebox.showinfo("Resume Builder", "Saved directory cleaned!")
        return True

    def improve_resume(self):
        content = self.builder.get_resume_builder_json()
        print(content)
        if not self.builder.is_loaded:
            messagebox.showerror("Resume Builder", "Please generate a resume first!")
            return

        resume_improver = ResumeImprover()
        reply_text = resume_improver.get_advice(content, prompt="You are a resume writing tutor. Your job is to improve the quality of the user's resume and make the expression as professional and human-like as possible, while not distorting the truth. Please provide the improved version of the resume following the original JSON format. DO NOT change ANY of the keys.")
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.insert(tk.END, reply_text)

        if not isinstance(reply_text, Exception):
            improve_resume_builder = ResumeBuilder()
            improve_resume_builder.load_resume_builder_json(reply_text)
            improve_resume_builder.generate_resume("improved_resume_" + time.strftime("%Y-%m-%d-%H_%M_%S"), preserve_latex=False)
            messagebox.showinfo("Resume Builder", "Resume improved successfully!")
        else:
            messagebox.showerror("Resume Builder", f"Error: {reply_text}")

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

        if not isinstance(reply_text, Exception):
            messagebox.showinfo("Resume Builder", "Resume rated successfully!")
        else:
            messagebox.showerror("Resume Builder", f"Error: {reply_text}")

    def compile_resume_from_latex(self):
        filename = self.filename_entry.get()
        if len(filename.strip()) == 0:
            messagebox.showerror("Resume Compiler", "Please enter a filename for the output PDF in the Output Filename field!")
            return
        
        latex_filepath = filedialog.askopenfilename(initialdir="output", title="Select file", filetypes=((".tex files", "*.tex"),))
        if len(latex_filepath.strip()) == 0: # the user closed the dialog and didn't select a file
            return
        self.builder = ResumeBuilder()

        try:
            # Compile the LaTeX file to generate the PDF
            print("Outputing resume pdf...")
            os.system(f'xelatex "{latex_filepath}" -output-directory=output -interaction=nonstopmode')

            # Check if the PDF file was generated successfully and rename it
            latex_filename = latex_filepath.split("/")[-1].removesuffix(".tex")
            if os.path.exists(f"output/{latex_filename}.pdf"):
                os.rename(f"output/{latex_filename}.pdf", f"output/{filename}.pdf")

            self.builder.is_loaded = True
            print("\nResume generated successfully!")

            # Save the resume builder data to a file
            self.builder.save_resume_builder_pkl(filename)
            messagebox.showinfo("Resume Compiler", "Resume compiled successfully!")

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Resume Compiler", f"Error: {e}")
        
        finally:
            # Clean up temporary files
            time.sleep(1)
            if os.path.exists("output/temp_resume.pdf"):
                os.remove("output/temp_resume.pdf")

            # Remove auxiliary files
            try:
                os.remove("output/temp_resume.aux")
                os.remove("output/temp_resume.log")
                os.remove("output/temp_resume.out")
            except:
                pass

    def generate_resume_from_template_latex(self):
        filename = self.filename_entry.get()
        if len(filename.strip()) == 0:
            messagebox.showerror("Resume LaTeX Generator", "Please enter a filename for the output PDF in the Output Filename field!")
            return

        template_filepath = filedialog.askopenfilename(initialdir="templates", title="Select the LaTeX template file", filetypes=((".tex files", "*.tex"),))
        if len(template_filepath.strip()) == 0:
            return
        
        # Load data from csv files
        self.builder = ResumeBuilder()
        self.builder.load_personal_info('data/personal_info.csv')
        self.builder.load_education('data/education.csv')
        self.builder.load_experience('data/experience.csv')
        self.builder.load_certifications('data/certifications.csv')
        self.builder.load_skills('data/skills.csv')
        self.builder.is_loaded = True

        resume_latex_generator = ResumeLatexGenerator()
        data = self.builder.get_resume_content()
        with open(template_filepath, 'r', encoding="utf-8") as file:
            template = file.read()
        
        if len(data) == 0:
            messagebox.showerror("Resume LaTeX Generator", "Please provide the user's information!")
            return
        
        if len(template) == 0: 
            messagebox.showerror("Resume LaTeX Generator", "Please provide a non-empty LaTeX example file!")
            return

        try:
            # Generate the resume from the template LaTeX file
            reply_text = resume_latex_generator.get_latex(data, template)
            if isinstance(reply_text, Exception):
                messagebox.showerror("Resume LaTeX Generator", f"Error: {reply_text}")

            # Save the generated LaTeX file
            with open(f"output/{filename}.tex", 'w', encoding="utf-8") as file:
                file.write(reply_text)

            self.feedback_text.delete("1.0", tk.END)
            self.feedback_text.insert(tk.END, reply_text)

            # Compile the LaTeX file to generate the PDF
            print("Outputing resume pdf...")
            try:
                os.system(f'xelatex "output/{filename}.tex" -output-directory=output -interaction=nonstopmode')
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Resume LaTeX Generator", f"Error: {e}")

            # Save the resume builder data to a file
            self.builder.save_resume_builder_pkl(filename)
            messagebox.showinfo("Resume LaTeX Generator", "Resume generated successfully!")

        except Exception as e:
            messagebox.showerror("Resume LaTeX Generator", f"Error: {e}")

        finally:
            time.sleep(1)

            # Remove auxiliary files
            try:
                os.remove(f"output/{filename}.aux")
                os.remove(f"output/{filename}.log")
                os.remove(f"output/{filename}.out")
            except:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    gui = ResumeBuilderGUI(root)
    root.mainloop()