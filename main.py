import tkinter as tk
from ui.password_manager_gui import PasswordManagerGUI
if __name__=='__main__':
    root=tk.Tk()
    app=PasswordManagerGUI(root)
    root.mainloop()