import tkinter as tk
from tkinter import messagebox,simpledialog
from core.password_manager import PasswordManager

class PasswordManagerGUI:
    def __init__(self,root):
        self.manager=PasswordManager()
        self.root=root
        self.root.title('Password Manager')

        self.add_button=tk.Button(root,text='Add Password',command=self.add_password)
        self.add_button.pack(pady=5)

        self.get_button=tk.Button(root,text='Get Password',command=self.get_password)
        self.get_button.pack(pady=5)

        self.generate_button=tk.Button(root,text='Generate Password',command=self.generate_password)
        self.generate_button.pack(pady=5)

    def add_password(self):
        account=simpledialog.askstring('Add Password','Enter account name:')
        password=simpledialog.askstring('Add Password','Enter password:',show='*')
        if account and password:   
            self.manager.save_password(account,password)
            messagebox.showinfo('Success','Password added successfully')
        else:
            messagebox.showerror('Error','Please enter both account and password')
    
    def get_password(self):
        account=simpledialog.askstring('Get Password','Enter account name:')
        if account:
            password=self.manager.get_password(account)
            if password:
                messagebox.showinfo('Password',f'Password for {account}:{password}')
            else:
                messagebox.showwarning('Warning','Password not found')
    
    def generate_password(self):
        password=self.manager.generate_password()
        messagebox.showinfo('Generated Password',f'Generated Password:{password}')


