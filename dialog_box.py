import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog

def ask_msg(msg: str):
	return tkinter.messagebox.askyesno(title = "freebird", message = msg)
	
def ask_more_msg(msg: str):
	return tkinter.messagebox.askyesnocancel(title = "freebird", message = msg)

def waring_msg(msg: str):
	return tkinter.messagebox.showwarning(title = "warning", message = msg)
	
def error_msg(msg: str):
	return tkinter.messagebox.showerror(title = "error", message = msg)
	
def info_msg(msg: str):
	return tkinter.messagebox.showinfo(title = "freebird", message = msg)

def get_msg(msg: str):
	return tkinter.simpledialog.askstring(title = "freebird", prompt = msg)
	
def film_msg():
	return tkinter.filedialog.askopenfilenames()

def save_msg():
	return tkinter.filedialog.asksaveasfile(mode='w')
	