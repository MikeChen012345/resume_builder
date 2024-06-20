<h1>Resume Builder</h1>

# Introduction

This is a resume builder that can help user facilitate their recruiting process. The builder takes user information as input and turns it into a formatted resume in PDF as output. The information will go through a Python script that converts the information into LaTex format via templates. Then the LaTex engine will be called to turn it into a PDF and return the file. We may provide a more user-friendly GUI version, but for simplicity, we may also do an easy-to-use command-line version that asks for information as CSV files and then outputs the PDF.

The project also includes an AI resume improver, which elaborates the wording and removes grammatical errors, and an AI resume rater, which rates the resume (currently only texts without format) and provides feedback on how to improve it. Both use GPT-3.5 as the model.


# Getting Started

To start using the resume builder, simply clone the repository to your local repository by using the following command in your terminal:

`git clone git@github.com:MikeChen012345/resume_builder.git`

Then, make sure that you have Python installed. If not, go to https://www.python.org/downloads/ to get the interpreter and follow the installation instructions. After this, go to your local repository and run the following command in your terminal to install all the required packages:

`pip install -r requirements.txt`

Then, if you have not, get LaTeX at https://miktex.org/download. Make sure that you get the version that corresponds to your system.

Now we can move on to build the resume! 

# Using the GUI

First, make sure that you have put your information correctly in all the CSV files in the `\data` folder.

Then, run the following command in your terminal to open the GUI:

`python gui.py`

_Note: during the generation, the software may be stuck due to waiting for responses from the url. Please wait patiently._

# Using the Commandline Interface

_Note: We recommend you to use the GUI if you can as the commandline can be troublesome if you don't have enough experience. Also, several features are only available via the GUI._

First, make sure that you have put your information correctly in all the CSV files in the `\data` folder. 

Then, run the following command in your terminal to generate the resume:

`python builder.py (<output_filename>) (<preserve LaTeX file=False>)`

The first parameter is the filename of the output PDF. The second parameter is whether to preserve the transitional LaTeX file. Note that if only one parameter exists, if the parameter is "True" or "False", then the parameter will be considered as the preserve_LaTeX_file flag. Otherwise, it will be considered as the output filename. If not specified, the default output filename will be "new_resume.pdf", and the default transitional LaTeX file will not be preserved after the generation of the PDF.

You might be asked to install some LaTeX dependencies for formatting. Just follow the instructions to install them all.

_Note: the commandline versions of resume improver and resume rater only provide basic support. To fully utilize them, please use the GUI version._

To use the `resume_improver.py` and `resume_rater.py`, you first need to create a file named `.env` under the local repository. Then, add the following lines inside:

`url = "<your openai API url>"`

`auth_key = <your openai API key>`

The url parameter is designed as such to allow 3rd-party openai API. For example, you can get a free openai API at https://github.com/chatanywhere/GPT_API_free.

Then, simply run the two programs using
`python resume_improver.py` and `python resume_rater.py`. You will be asked to provide your resume and a job description of the job that you are applying for. You can also fill in the your resume in the variable `content` and your job description in the variable `theme` (only for `resume_rater.py`).

_Note: during the generation, the software may be stuck due to waiting for responses from the url. Please wait patiently._

# Trouble Shooting

## I am using MacOS and the `python` commands do not work for me

For MacOS, try changing `python` into `python3` and leaving the other parts the same.

## The resume improver fails to create new resume. What should I do?

The current resume improver can be unstable because sometimes GPT changes the format, causing the resume improver to fail to recognize the response. You can retry and it should be working within a few tries.

## Other issues/bugs

Please open an issue :) I will get back ASAP