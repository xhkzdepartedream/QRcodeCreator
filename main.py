import qrcode
import random
import os
import tkinter as tk
import validators
import datetime
from tkinter import filedialog,ttk,messagebox
from PIL import Image, ImageDraw, ImageFont
import textwrap

def show_creator():
    messagebox.showinfo("关于","开发者：xhkzdepartedream")

top = tk.Tk()
top.title('二维码生成器')
top.geometry('600x500')
termin = tk.Menu(top)
termin.add_command(label="关于",command=show_creator)
top.config(menu=termin)

website_text = tk.Text(master=top, cursor='xterm', width=50, height=10,relief='flat')
filename_entry=ttk.Entry(master=top, cursor='xterm',width=50)
label1 = tk.Label(master=top, text='网址')
label2 = tk.Label(master=top, text='生成的二维码图片的文件名')
label3 = tk.Label(master=top, text='注意：如果不指定文件名，程序将会随机生成文件名，\n但可能不便于确认二维码的内容。',fg='red',font=1)
label4 = tk.Label(master=top, text='保存文件路径：NULL')

warning_label = tk.Label(master=top, text="", fg='red',pady=10)
folder_path="NULL"
warning=1

def is_valid_filename(filename):
     # 对于 Windows，文件名不能包含以下字符
    invalid_chars = r'<>:"/\|?*'  # Windows 的非法字符
    if any(char in filename for char in invalid_chars):
        return False

    # 文件名不能包含两个以上的连续句点或空格等
    if filename.endswith(' ') or filename.endswith('.'):
        return False
    # 文件名长度检查
    if len(filename) > 255:  # Windows 文件名最长 255 个字符
        return False

    # 检查是否为保留字 (Windows)
    reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                      'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    if filename.upper() in reserved_names:
        return False

    # 如果在 Linux 或 macOS 下，检查路径是否有效
    try:
        # 需要给出一个路径，可以是当前路径或者其他路径，确保操作系统支持
        os.path.join('.', filename)
    except ValueError:
        return False
    return True

def check():
    data = website_text.get(1.0,"end-1c")
    if validators.url(data):
        return True
    else:
        return False

def make_qrcode():
    data = website_text.get(1.0,"end-1c")
    global warning
    if check():
        img = qrcode.make(data)
        date = str(datetime.date.today()) + '-'
        if folder_path=='NULL':
            if warning==1:
                ret=messagebox.askokcancel("警告","未指定文件保存路径，生成的图片将保存在程序当前工作目录，确定要继续吗？\n本提示不再重复。")
                warning=0
                if not ret:
                    return
            img.save(date+str(random.randint(100000, 999999))+'.png')
        else:
            name=folder_path+'/'+date+filename_entry.get()+'.png'
            if is_valid_filename(filename_entry.get()):
                img.save(name)
                warning_label.config(text='处理成功', fg='black')
            else:
                warning_label.config(text="输入的文件名不合法", fg='red')
                return
    else:
        warning_label.config(text="输入的网址不合法", fg='red')

    website_text.delete(1.0, 'end')
    filename_entry.delete(0, 'end')

def choose_dict():
    global folder_path
    folder_path = filedialog.askdirectory(title="选择保存文件的文件夹")
    if folder_path=="":
        folder_path = 'NULL'
    label4.config(text='保存文件路径：'+folder_path)
    
def clear():
    website_text.delete(1.0, 'end')
    filename_entry.delete(0, 'end')
    warning_label.config(text="", fg='red',pady=10)

conf_but = ttk.Button(master=top, text='确认开始生成', command=make_qrcode,takefocus=False,width=15)
dict_but=ttk.Button(master=top,text='指定保存文件路径...', command=choose_dict,takefocus=False,width=15)
clear_but=ttk.Button(master=top,text='清空所有文本', command=clear,takefocus=False,width=15)
label1.pack()
website_text.pack()
warning_label.pack()
label2.pack()
filename_entry.pack()
clear_but.pack(pady=10)
label3.pack()
dict_but.pack(pady=10)
label4.pack()
conf_but.pack(pady=10)
top.mainloop()