from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
import paramiko, os

scripts_file = []
for file in os.listdir():
    if file[-5:] == '.shsp':
        scripts_file.append(file)
scripts_file.append('Выбрать пустой')

global client
remember = True

def chk():
    global remember
    remember = False

def connect():
    global client
    #Поддягиваю переменные из форм если их нет в конфигурации
    with open('config.txt', 'r') as file:
        par = file.read()
        if par != '':
            host, user, password, port = par.split()
            port = int(port)
        else:
            host = f'{txt.get()}'
            user = f'{txt1.get()}'
            password = f'{txt2.get()}'
            port = txt3.get()
    #Подключаюсь к серверу
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=password, port=port)
        if remember:
            with open('config.txt', 'w') as file:
                file.write(f'{host} {user} {password} {port}')
        else:
            with open('config.txt', 'w') as file:
                file.write('')
        screen.title("SSH Scripts Panel 0.1 (Подключено)")
        print('Подключение установлено!')
    except:
       print('Ошибка подключения!')

def script_view(event):
    global combobox, text
    if combobox.get() != '':
        try:
            with open(f'{combobox.get()}', 'r', encoding='utf8') as file:
                scripts = (file.read())
                text.delete('1.0', END)
                text.insert(1.0, scripts)
        except:
            print('Ошибка отобржения скрипта!')

def script():
    global client, text
    try:
        scripts = (str(text.get(1.0, END)).split('\n'))
        for command in scripts:
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())
        print('Скрипт выполнен успешно!')
    except:
        print('Ошибка выполнения! Возможно отсутствует подключение...')

def script_save():
    global text
    try:
        file_name = fd.asksaveasfilename(
        filetypes=(("Scripts files", "*.shsp"), ("All files", "*.*")))
        f = open(file_name, 'w')
        s = text.get(1.0, END)
        f.write(s)
        f.close()
    except:
        print('Ошибка сохранения!...')


def script_file():
    global client, combobox
    if combobox.get() == '':
        print("Выберите скрипт!")
        return
    try:
        with open(f'{combobox.get()}') as file:
            scripts = (file.read()).split('\n')
        for command in scripts:
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())
        print('Скрипт выполнен успешно!')
    except:
        print('Ошибка выполнения скрипта! Возможно отсутствует подключение...')

#Настройки экрана
screen = Tk()  
screen.title("SSH Scripts Panel 0.1 (Неподключено)")  
screen.geometry('690x440')

#Форма ввода данных для подключения
lbl = Label(screen, text="Хост:")  
lbl.place(x=0, y=5)  
txt = Entry(screen, width=10)  
txt.place(x=35, y=5)

lbl1 = Label(screen, text="Имя:")  
lbl1.place(x=105, y=5)  
txt1 = Entry(screen, width=10)  
txt1.place(x=140, y=5)

lbl2 = Label(screen, text="Пароль:")  
lbl2.place(x=210, y=5)  
txt2 = Entry(screen, width=10)  
txt2.place(x=265, y=5)

lbl3 = Label(screen, text="Порт:")  
lbl3.place(x=335, y=5)  
txt3 = Entry(screen, width=10)  
txt3.place(x=380, y=5)

btn = Button(screen, text="Подключиться", command=connect) 
btn.place(x=450, y=0)

chk_state = BooleanVar()  
chk_state.set(True) 
chk = Checkbutton(screen, text='Запомнить меня', var=chk_state, command=chk)  
chk.place(x=550, y=0) 

scroll = Scrollbar(screen, orient='horizontal')
scroll.pack(side=BOTTOM, fill='x')
text = Text(width=60, height=20, bg="white", fg='black', wrap=NONE, xscrollcommand=scroll.set)
text.pack()
text.place(x=200, y=100)
scroll.config(command=text.xview)

btn1 = Button(screen, text="Выполнить код", command=script) 
btn1.place(x=580, y=390)

lbl3 = Label(screen, text="Выберете\nсохраннёный скрипт")  
lbl3.place(x=40, y=55) 
combobox = ttk.Combobox(values=scripts_file)
combobox.pack(anchor=NW, padx=6, pady=6)
combobox.place(x=30, y=100)
combobox.bind("<<ComboboxSelected>>", script_view)

btn1 = Button(screen, text="Выполнить", command=script_file) 
btn1.place(x=65, y=130)

btn2 = Button(screen, text="Сохранить", command=script_save) 
btn2.place(x=500, y=390)

#Завершение работы
screen.mainloop()
client.close()