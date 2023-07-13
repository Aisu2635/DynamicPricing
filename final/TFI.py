from tkinter import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import datetime

root = Tk()
root.wm_title("project")
root.geometry('1920x1080+0+0')
root.configure(bg='#EEAA00')
C = Canvas(root, height=3840, width=2160)


def Lr():
    def connect():
        E1 = int(Entry1.get())  # samosa
        E2 = int(Entry2.get())  # vadapav
        df = pd.read_csv('Sale_data.csv')

        df['Time'] = pd.to_datetime(df['Time']).dt.hour

        X = df[['Quantity', 'Time']]  # Using quantity & time as the feature
        y = df['Price']  # Price is the target variable

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        rf_model = RandomForestRegressor()
        rf_model.fit(X_train, y_train)

        rf_train_score = rf_model.score(X_train, y_train)
        rf_test_score = rf_model.score(X_test, y_test)
        print("Random Forest Training R-squared:", rf_train_score)
        print("Random Forest Testing R-squared:", rf_test_score)

        lr_train_score = lr_model.score(X_train, y_train)
        lr_test_score = lr_model.score(X_test, y_test)
        print("Linear Regression Training R-squared:", lr_train_score)
        print("Linear Regression Testing R-squared:", lr_test_score)

        base_price_vadapav = 10
        base_price_samosa = 8

        def calculate_dynamic_price(quantity_sold_vadapav, quantity_sold_samosa):
            current_time = datetime.datetime.now().hour
            lr_predicted_price_v = lr_model.predict([[quantity_sold_vadapav, current_time]])
            lr_predicted_price_s = lr_model.predict([[quantity_sold_samosa, current_time]])
            rf_predicted_price_v = rf_model.predict([[quantity_sold_vadapav, current_time]])
            rf_predicted_price_s = rf_model.predict([[quantity_sold_samosa, current_time]])
            if quantity_sold_vadapav >= quantity_sold_samosa:
                lr_dynamic_price_v = base_price_vadapav + 0.1 * lr_predicted_price_v[0]
                lr_dynamic_price_s = base_price_samosa - 0.1 * lr_predicted_price_s[0]
                rf_dynamic_price_v = base_price_vadapav + 0.1 * rf_predicted_price_v[0]
                rf_dynamic_price_s = base_price_samosa - 0.1 * rf_predicted_price_s[0]
            else:
                lr_dynamic_price_v = base_price_vadapav - 0.1 * lr_predicted_price_v[0]
                lr_dynamic_price_s = base_price_samosa + 0.1 * lr_predicted_price_s[0]
                rf_dynamic_price_v = base_price_vadapav - 0.1 * rf_predicted_price_v[0]
                rf_dynamic_price_s = base_price_samosa + 0.1 * rf_predicted_price_s[0]

            final_dynamic_price_v = (lr_dynamic_price_v + rf_dynamic_price_v) / 2
            final_dynamic_price_s = (lr_dynamic_price_s + rf_dynamic_price_s) / 2

            return final_dynamic_price_v, final_dynamic_price_s

        dynamic_price_vadapav, dynamic_price_samosa = calculate_dynamic_price(E2, E1)
        V_price.configure(text="Dynamic Price of Vadapav is: " + str(dynamic_price_vadapav))
        S_price.configure(text="Dynamic Price of Samosa is: " + str(dynamic_price_samosa))
        base_price_samosa = dynamic_price_samosa
        base_price_vadapav = dynamic_price_vadapav

    Window6 = Toplevel(root)
    Window6.geometry('1920x1080')
    Window6.state('zoomed')
    C7 = Canvas(Window6, height=3840, width=2160)
    img = PhotoImage(file="anime.gif")
    C7.create_image(960, 500, anchor=CENTER, image=img)
    C7.pack()
    Label1 = Label(Window6, text="The Food Index!!!", bg="#606060", font="Times 34", borderwidth=5, relief="raised")
    Label1.place(relx=0.5, rely=0.2, anchor=CENTER)
    baseV = Label(Window6, text="Base Price of Vadapav is: 10", bg="#c1976d", font="Times 20", borderwidth=5,
                  relief="raised")
    baseV.place(relx=0.7, rely=0.1)
    baseS = Label(Window6, text="Base Price of Samosa is: 8", bg="#c1976d", font="Times 20", borderwidth=5,
                  relief="raised")
    baseS.place(relx=0.7, rely=0.2)
    Label3 = Label(Window6, text="Please Enter your Details for the same:-", bg="#606060", font="Times 20",
                   borderwidth=5,
                   relief="raised")
    Label3.place(relx=0.1, rely=0.3)
    Label4 = Label(Window6, text="Enter amount of Samosa sold :-", bg="#c1976d", font="Times 20", borderwidth=5,
                   relief="raised")
    Label4.place(relx=0.1, rely=0.4)
    Entry1 = Entry(Window6, font="Times 15", bg="#dfdfdf", borderwidth=5, relief="raised")
    Entry1.place(relx=0.1, rely=0.49)
    Label4 = Label(Window6, text="Enter amount of Vadapav Sold:-", bg="#c1976d", font="Times 20", borderwidth=5,
                   relief="raised")
    Label4.place(relx=0.1, rely=0.6)
    Entry2 = Entry(Window6, font="Times 15", bg="#dfdfdf", borderwidth=5, relief="raised")
    Entry2.place(relx=0.1, rely=0.69)
    Button2 = Button(Window6, text="Purchase", font="Times 20", bg="#dfdfdf", borderwidth=5, relief="raised",
                     command=connect)
    Button2.place(relx=0.1, rely=0.79)

    V_price = Label(Window6, text="Dynamic Price for Vadapav:-", bg="#c1976d", font="Times 20", borderwidth=5,
                    relief="raised")
    V_price.place(relx=0.5, rely=0.6)

    S_price = Label(Window6, text="Dynamic Price for Samosa:-", bg="#c1976d", font="Times 20", borderwidth=5,
                    relief="raised")
    S_price.place(relx=0.5, rely=0.4)

    Window6.mainloop()


def mainscreen():
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='file', menu=filemenu)
    filemenu.add_command(label="New")
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Exit")

    img = PhotoImage(file="anime.gif")
    C.create_image(960, 500, anchor=CENTER, image=img)
    root.state('zoomed')

    Title = Label(C, relief="ridge", text="Food Pricing model mimicking share market ", bg="#c1976d", font="Times 45",
                  borderwidth=5)
    Title.place(relx=0.5, rely=0.1, anchor=CENTER)
    Welcome = Label(C, relief="groove", bg="#c1976d",
                    text="In this Machine Learning Final Project, we shall show different machine learning models",
                    font="Times 30", borderwidth=5)
    Welcome.place(relx=0.5, rely=0.2, anchor=CENTER)

    Button1 = Button(C, bg="#c1976d", text="Start!!", font="Times  25", relief="raised", command=Lr)
    Button1.place(relx=0.5, rely=0.55, anchor=CENTER)

    Button2 = Button(C, bg="#c1976d", text="Settings", font="Times 25", relief="raised")
    Button2.place(relx=0.5, rely=0.65, anchor=CENTER)

    acc = Label(C, relief="groove", bg="#c1976d", text="Made by:  COMP 18 Aditya Borkar | COMP 52 Om Hinge | "
                                                       "CSE 65 Omkar | ENTC 66 Arjun ", font="Times 15")
    acc.place(relx=0.5, rely=0.9, anchor=CENTER)

    C.pack()
    root.mainloop()


if __name__ == "__main__":
    mainscreen()
