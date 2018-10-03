import tkinter as tk

import tools.tool_blog_amara
from amara.amara_env import amara_headers

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.blogIdLabel= tk.Label(self)
        self.blogIdLabel["text"] = "blogId"
        self.blogIdLabel.pack()

        self.blogIdEntryBox = tk.Entry(self)
        self.blogIdEntryBox.focus_set()
        self.blogIdEntryBox.pack()

        self.postIdLabel= tk.Label(self)
        self.postIdLabel["text"] = "postId"
        self.postIdLabel.pack()

        self.postIdEntryBox = tk.Entry(self)
        self.postIdEntryBox.focus_set()
        self.postIdEntryBox.pack()

        self.languageCodeLabel = tk.Label(self)
        self.languageCodeLabel["text"] = "languageCode"
        self.languageCodeLabel.pack()

        self.languageCodeBox = tk.Entry(self)
        self.languageCodeBox.focus_set()
        self.languageCodeBox.pack()

        self.executeButton = tk.Button(self)
        self.executeButton["text"] = "Create Amara entry\n"
        self.executeButton["command"] = self.do_import
        self.executeButton.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def do_import(self):
        tools.tool_blog_amara.subtitles_workflow(self.blogIdEntryBox.get(), self.postIdEntryBox.get(), self.languageCodeBox.get(), amara_headers)

root = tk.Tk()
app = Application(master=root)
app.mainloop()