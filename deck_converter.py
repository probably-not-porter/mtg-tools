from tkinter import *
from tkinter import filedialog
  
def browseFiles():
    filenames = filedialog.askopenfilenames(initialdir = "/", title = "Select a File", filetypes = (("Text files","*.txt*"),("all files","*.*")))
    num_files = len(filenames)
    label_file_explorer.configure(text="Opened: "+ str(num_files) + " file(s)")
    for item in filenames:
        print(item)
        label_file_names.insert(END, str(item) + "\n")

def browseFolders():
    folder_selected = filedialog.askdirectory(initialdir = "/", title = "Select an Save Directory")
    label_folder_explorer.configure(text="Export to: "+folder_selected)

def convDCK():
    print("CONVERT TO DCK")

window = Tk()
window.title('MTG Bulk File Converter')

# FILE EXPLORER BUTTON
label_file_explorer = Label(window, text = "Open a deck file...",width = 50, height = 4, fg = "blue")
button_explore_files = Button(window, text = "Browse Files",command = browseFiles) 
label_file_explorer.grid(column = 1, row = 0, columnspan = 3)
button_explore_files.grid(column = 0, row = 0)

# FOLDER EXPLORER BUTTON
label_folder_explorer = Label(window, text = "Select a Save Directory",width = 50, height = 4, fg = "blue")
button_explore_folders = Button(window, text = "Browse Folders",command = browseFolders) 
label_folder_explorer.grid(column = 1, row = 1, columnspan = 3)
button_explore_folders.grid(column = 0, row = 1)

# CONVERT BUTTONS
button_dck = Button(window, text = "Convert to .dck",command = convDCK) 
button_dck.grid(column = 0, row = 2)

button_dec = Button(window, text = "Convert to .dec",command = convDCK) 
button_dec.grid(column = 1, row = 2)

button_dek = Button(window, text = "Convert to .dek",command = convDCK) 
button_dek.grid(column = 2, row = 2)

button_mtga = Button(window, text = "Convert to .mtga",command = convDCK) 
button_mtga.grid(column = 3, row = 2)

button_cod = Button(window, text = "Convert to .cod",command = convDCK) 
button_cod.grid(column = 4, row = 2)

label_file_names = Text(window,width=70, height=20, fg = "blue")
label_file_names.grid(column=0,row=3,columnspan = 5)

  
window.mainloop()