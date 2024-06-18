"""
Resume Builder - Command Line Interface

This is a resume builder that takes in a user's information and generates a resume in PDF format.
The user is prompted to enter their personal information, education, work experience, skills, and interests
in csv format. The resume is then generated using the data provided by the user through LaTeX templates.

Files required:
- builder.py (this file)
- resume_config.cls
- data/
    - personal_info.csv
    - education.csv
    - experience.csv
    - certifications.csv
    - skills.csv

Command line usage: python resume_builder.py (<output_filename>) (<preserve LaTeX file=False>)

Note: The user needs to provide the required information in the csv files before running the script.
        Currently, up to 5 experience explanations are supported.
"""

import os
import csv
import time
import sys

class ResumeBuilder:
    def __init__(self):
        self.personal_info = {}
        self.education = []
        self.experience = []
        self.certifications = []
        self.skills = []

    def load_personal_info(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.personal_info = next(reader)
        return self.personal_info

    def load_experience(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.experience = [row for row in reader]
        return self.experience
    
    def load_education(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.education = [row for row in reader]
        return self.education

    def load_certifications(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.certifications = [row for row in reader]
        return self.certifications
    
    def load_skills(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.skills = [row for row in reader]
        return self.skills

    def generate_resume(self, filename="new_resume", preserve_latex=False):
        """
        Generate resume using the provided data.

        Args:
            filename (str): Name of the output file.
            preserve_latex (bool): Flag to preserve the LaTeX file after generating the PDF.
        """
        # Generate and compile the LaTeX resume
        with open("temp_resume.tex", 'w') as file:
            # Start of the LaTeX document
            file.write("\documentclass[letterpaper]{resume_config}\n\n")
            file.write(r"\begin{document}")
            file.write("\n\n")
            
            # Personal information
            file.write("\Header\n    {" + self.personal_info['name'] + "}\n    {"
                       + self.personal_info['city'] + ", " + self.personal_info['province'] + "}\n    {"
                       + self.personal_info['phone number'] + "}\n    {"
                       + self.personal_info['email'] + "}\n    {"
                       + self.personal_info['linkedin link (https://linkedin.com/in/_______)'] + "}")
            file.write("\n\n")

            # Experience
            file.write("\section{Experience}\n\n")
            
            for exp in self.experience: 
                exp_string = "\WorkExperience\n    {" + exp['job title'] + "}\n    {"\
                + exp['company name'] + "}\n    {"\
                + exp['beginning and end of employment. If currently employed write " - Present"'] + "}\n    {"\
                + exp['city'] + ", " + exp['country of employment'] + "}\n    {\n"
                for i in range(1, 6): # Support up to 5 experience explanations
                    if 'explanation' + str(i) not in exp or not exp['explanation' + str(i)]:
                        # No more experience entries
                        break
                    exp_string += "        \item " + exp['explanation' + str(i)] + "\n"
                exp_string += "}"
                file.write(exp_string)
                file.write("\n\n")
            file.write("\n\n")

            # Education
            file.write("\section{Education}\n\n")

            for edu in self.education:
                edu_string = "\EducationExperience\n    {" + edu['school name'] + "}\n    {"\
                + edu['credential name'] + "}\n    {"\
                + edu['date of graduation'] + "}\n    {"\
                + edu['city'] + ", " + edu['country of school'] + "}\n"
                file.write(edu_string)
                file.write("\n\n")
            file.write("\n\n")

            # Certifications
            file.write("\section{Certifications}\n\n")
            for cert in self.certifications:
                cert_string = "\Certification\n    {" + cert['credential name'] + "}\n    {"\
                + cert['school name'] + "}\n    {"\
                + cert['date of completion'] + "}\n"
                file.write(cert_string)
                file.write("\n\n")
            file.write("\n\n")

            # Skills
            file.write("\section{Skills}\n\n")
            file.write(r"\begin{SkillsList}")
            for skill in self.skills:
                file.write("\n    \item " + skill['name'])
            file.write("\n\end{SkillsList}")
            file.write("\n\n")


            # End of the LaTeX document
            file.write("\end{document}")
        
        try:
            # Compile the LaTeX file to generate the PDF
            print("Outputing resume pdf...")
            os.system(f"xelatex temp_resume.tex -output-directory=output -interaction=nonstopmode")

            # Check if the PDF file was generated successfully and rename it
            if os.path.exists("output/temp_resume.pdf"):
                os.rename("output/temp_resume.pdf", f"output/{filename}.pdf")

            print("\nResume generated successfully!")

        finally:
            # Clean up temporary files
            time.sleep(1)
            if os.path.exists("output/temp_resume.pdf"):
                os.remove("output/temp_resume.pdf")
            if not preserve_latex:
                os.remove("temp_resume.tex")
                #os.remove("temp_resume.fdb_latexmk")
                #os.remove("temp_resume.fls")
            else:
                os.rename("temp_resume.tex", f"output/{filename}.tex")
            os.remove("output/temp_resume.aux")
            os.remove("output/temp_resume.log")
            os.remove("output/temp_resume.out")


if __name__ == '__main__':
    # Read the arguments
    if len(sys.argv) == 1: # Default output filename
        output_filename = "new_resume"
    elif len(sys.argv) == 2: # Custom output filename or preserve LaTeX file flag
        if sys.argv[1].lower() == "true":
            preserve_latex = True
            output_filename = "new_resume"
        elif sys.argv[1].lower() == "false":
            preserve_latex = False
            output_filename = "new_resume"
        else:
            output_filename = sys.argv[1]
            preserve_latex = False
    elif len(sys.argv) == 3: # Custom output filename and preserve LaTeX file flag
        output_filename = sys.argv[1]
        preserve_latex = sys.argv[2].lower() == "true"
    else:
        print("Usage: python resume_builder.py (<output_filename>) (<preserve LaTeX file=False>)")
        sys.exit(1)
    

    # Initialize the resume builder
    builder = ResumeBuilder()

    # Load data from csv files
    builder.load_personal_info('data/personal_info.csv')
    builder.load_education('data/education.csv')
    builder.load_experience('data/experience.csv')
    builder.load_certifications('data/certifications.csv')
    builder.load_skills('data/skills.csv')

    # Generate the resume
    if not os.path.exists('output'):
        os.makedirs('output')
    builder.generate_resume(output_filename, preserve_latex=preserve_latex)
