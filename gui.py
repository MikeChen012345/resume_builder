import tkinter

class ResumeBuilder:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Resume Builder")
        self.window.geometry("800x600")
        self.window.mainloop()

if __name__ == "__main__":
    ResumeBuilder()