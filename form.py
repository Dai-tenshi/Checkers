from tkinter import *
from tkinter import messagebox
import json
import rsaCipher


# главное окно приложения
window = Tk()
# заголовок окна
window.title('Авторизация')
# размер окна
window.geometry('800x600')
# можно ли изменять размер окна - нет
window.resizable(False, False)
is_loginned = False

window["bg"]='white'
#загрузка списка пользователей
users_list={}
try:
    with open('users/users.json') as json_file:
        users_list=json.load(json_file)
except Exception:
    with open('users/users.json','w') as out_file:
        users_list={"users":[]}
        json.dump(users_list,out_file)


img=PhotoImage(file='images/fon.png')
Label(window,image=img,bg='white',height='500',width='250').place(x=50,y=50)


username=""
password=""




main_label = Label(window, text='Авторизация',bg='white')
# помещаем виджет в окно по принципу один виджет под другим
main_label.pack()

# метка для поля ввода имени
username_label = Label(window, text='Имя пользователя')
username_label.pack()

# поле ввода имени
username_entry = Entry(window, bg='#fff', fg='#444')
username_entry.pack()

# метка для поля ввода пароля
password_label = Label(window, text='Пароль' )
password_label.pack()

# поле ввода пароля
password_entry = Entry(window, bg='#fff', fg='#444')
password_entry.pack()
def sign_in_clicked():

    # получаем имя пользователя и пароль

    print(username,password)
    sign_in()
# кнопка отправки формы
sign_in_Button = Button(window, text="Войти",border=0,bg='white',cursor='hand2',fg='blue', command=sign_in_clicked)
sign_in_Button.place(x=380,y=115)


label=Label(window,text="У вас нет аккаунта?",fg='black',bg='white')
label.place(x=315,y=150)
def sign_up():
    username = username_entry.get()
    password = password_entry.get()

    if len(username) > 0 and len(password) > 0:
        if password.isdigit()==False:
            messagebox.showinfo("Пароль должен состоять только из цифр")
            return
        user_create(username, password)
sign_up_Button=Button(window, text="Регистрация",border=0,bg='white',cursor='hand2',fg='blue', command=sign_up)
sign_up_Button.place(x=425,y=150)
# обработчик нажатия на клавишу 'Войти'

def sign_in():
    username = username_entry.get()
    password = password_entry.get()
    if len(username)>0 and len(password)>0:
        isUserExist = False
        need_pasword = ""
        for i in range(len(users_list["users"])):
            if users_list["users"][i]["username"] == username:
                isUserExist = True
                rsaCipher.encrypte = users_list["users"][i]["enc"]
                need_pasword = rsaCipher.rsa_decrypt(users_list["users"][i]["password"])
                break

        if isUserExist == False or password != need_pasword:
            messagebox.showinfo('Ошибка','Имя пользователи или пароль введены неправильно')
            window.destroy()
        elif isUserExist == True and password == need_pasword:
            username_set(username)
            if sign_in_Button:
                window.destroy()
            return #успешный вход в лич.каб
    else:
        messagebox.showinfo('Ошибка',"Пустые поля")



def user_create(u, p):
    global users_list
    users_list = users_list
    isUserexist = False
    if len(users_list["users"]) > 0:
        for i in range(len(users_list["users"])):
            if users_list["users"][i]["username"] == u:
                messagebox.showinfo("Ошибка","Пользователь уже существует")
                isUserexist = True
                break
    else:
        messagebox.showinfo('Ошибка',"Поле пустое")
    if not isUserexist:
        cryptpass = rsaCipher.rsa_encrypt(p)
        users_list["users"].append({"username":u,"password":cryptpass, "enc":rsaCipher.encrypte})

        with open('users/users.json', 'w') as out_file:
            json.dump(users_list, out_file)
            messagebox.showinfo("Регистрация", "Pегистрация успешна")
            username_set(username)

def username_set(u):
    global username
    global is_loginned
    username=u
    username=username
    is_loginned = True



window.mainloop()
