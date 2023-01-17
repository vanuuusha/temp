import tkinter as tk
from configure import host, user, password, db_name, CONSOLETEXT
import psycopg2
from help_elements import create_button, create_entry, create_label, create_combo_box
from datetime import datetime


def make_number(string: str):
    answer = ''
    for i in string:
        if i.isdigit():
            answer += i
        if i == ',':
            return int(answer)


class CustomerForm:
    def __init__(self):
        self.db = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        self.cursor = self.db.cursor()
        self.x = 225
        self.window = tk.Tk()
        self.create_console()
        self.window.geometry('1400x875')
        self.active_elements = {}
        self.show_main_screen()
        self.window.mainloop()
        self.window.title("Ресторан")

    def create_console(self, text=""):
        try:
            self.console.destroy()
        except AttributeError:
            pass
        create_label(
            font_color='#000000',
            text=CONSOLETEXT,
            position=[550, 175],
            font="Sedan 14",
            background="#30d3f9"
        )

        self.console = tk.Text(font=f"Sedan 14",
                               foreground='#000000',
                               background='#ffffff',
                               width=70,
                               height=18)
        self.console.insert(tk.END, text)
        self.console.place(x=560, y=225)

    def show_main_screen(self):
        self.destroy_all()
        self.active_elements['add'] = create_button(font_color='#ffffff', text="Добавить",
                                                    command=self.show_add_menu, position=[240, 425],
                                                    background='#2998E9', width='25', height='3',
                                                    font="Sedan 12")
        self.active_elements['show'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                     command=self.show_show_menu, position=[240, 325],
                                                     background='#2998E9', width='25', height='3',
                                                     font="Sedan 12")
        self.active_elements['make_purchase'] = create_button(font_color='#ffffff', text="Сделать покупку",
                                                              command=self.make_purchase, position=[240, 525],
                                                              background='#2998E9', width='25', height='3',
                                                              font="Sedan 12")
        self.active_elements['add_balance'] = create_button(font_color='#ffffff', text="Пополнить баланс",
                                                            command=self.show_add_balance, position=[240, 525],
                                                            background='#2998E9', width='25', height='3',
                                                            font="Sedan 12")
        self.active_elements['kill_all'] = create_button(font_color='#ffffff', text="Выход",
                                                         command=self.kill_all, position=[1000, 700],
                                                         background='#2998E9', width='25', height='3',
                                                         font="Sedan 12")

    def make_purchase(self):
        self.destroy_all()
        self.create_console('Вы хотите сделать покупку')
        self.active_elements['customer_name'] = create_label(font_color="#000000",
                                                             text="Выберите покупателя", position=[self.x, 275],
                                                             background="#b5effb",
                                                             font="Sedan 14")
        self.cursor.execute('SELECT id FROM "Customer"')
        customers_id = self.cursor.fetchall()
        self.active_elements['customer_info'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                              command=self.show_customer_info, position=[50, 325],
                                                              background='#2998E9', width=12, height='3',
                                                              font="Sedan 12")
        self.active_elements['customer_combo'] = create_combo_box(width=12, font_color="#000000",
                                                                  position=[self.x, 325], values=customers_id,
                                                                  font="Sedan 14", default=0)
        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 700], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")
        self.active_elements['complete'] = create_button(font_color='#ffffff', text="Выполнить",
                                                         command=self.user_make_purchase, position=[325, 675],
                                                         background='#2998E9', width=12, height='3',
                                                         font="Sedan 12")

    def user_make_purchase(self):
        customer = int(self.active_elements['customer_combo'].get())
        if self.has_open_purchase(customer):
            purchase_id = self.get_purchase_id(customer)
            self.cursor.execute('SELECT current_price FROM "Purchase" WHERE id=%s', (purchase_id,))
            current_price = make_number(self.cursor.fetchone()[0])
            self.cursor.execute('SELECT balance FROM "Customer" WHERE id=%s', (customer,))
            balance = make_number(self.cursor.fetchone()[0])
            if current_price > balance:
                self.create_console('На балансе данного пользователя недостаточно средств')
            else:
                self.cursor.execute('UPDATE "Purchase" SET complete=True, time_bought=%s WHERE id=%s',
                                    (datetime.now(), purchase_id,))
                self.cursor.execute('UPDATE "Customer" SET balance = balance - CAST(%s AS MONEY) WHERE id=%s',
                                    (current_price, customer))
                self.create_console('Покупка успешно завершена')
        else:
            self.create_console('У пользователя нет открытой покупки')
        self.show_main_screen()

    def kill_all(self):
        self.db.commit()
        self.db.close()
        self.window.destroy()

    def show_show_menu(self):
        self.destroy_all()
        self.create_console('Просмотреть информацию о')
        self.active_elements['show_customer'] = create_button(font_color='#ffffff', text="Информация о покупателях",
                                                              command=self.show_customer_info, position=[240, 225],
                                                              background='#2998E9', width='25', height='3',
                                                              font="Sedan 12")
        self.active_elements['show_list_shops'] = create_button(font_color='#ffffff', text="Список ресторанов",
                                                                command=self.show_list_shops, position=[240, 325],
                                                                background='#2998E9', width='25', height='3',
                                                                font="Sedan 12")
        self.active_elements['show_list_dishes'] = create_button(font_color='#ffffff', text="Список блюд",
                                                                 command=self.show_list_dishes, position=[240, 425],
                                                                 background='#2998E9', width='25', height='3',
                                                                 font="Sedan 12")
        self.active_elements['show_list_providers'] = create_button(font_color='#ffffff', text="Список поставщиков",
                                                                    command=self.show_list_providers,
                                                                    position=[240, 525],
                                                                    background='#2998E9', width='25', height='3',
                                                                    font="Sedan 12")

        self.active_elements['show_list_ingridients'] = create_button(font_color='#ffffff', text="Список ингредиентов",
                                                                      command=self.show_list_ingridients,
                                                                      position=[240, 625],
                                                                      background='#2998E9', width='25', height='3',
                                                                      font="Sedan 12")
        self.active_elements['show_list_purchase'] = create_button(font_color='#ffffff', text="Список покупок",
                                                                   command=self.show_list_purchase,
                                                                   position=[240, 725],
                                                                   background='#2998E9', width='25', height='3',
                                                                   font="Sedan 12")
        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 700], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")

    def show_answer(self, text=''):
        answer = text
        for i in self.cursor.fetchall():
            for j in i:
                if isinstance(j, str):
                    j = j.strip()
                answer += f'{j} '
            answer += '\n'
        self.create_console(answer)

    def show_customer_info(self):
        self.cursor.execute('SELECT * FROM "Customer" LIMIT 10;')
        self.show_answer("Список покупателей\nname, id, surname, balance, date_born, sex, username\n")

    def show_list_shops(self):
        self.cursor.execute('SELECT * FROM "Restaurants" LIMIT 10;')
        self.show_answer("Список магазинов\nid, name, description\n")

    def show_list_dishes(self):
        self.cursor.execute('SELECT * FROM "Dishes" LIMIT 10;')
        self.show_answer("Список блюд\nid, dish_name, dish_cost, dish_description, dish_type_id, restaraun_id\n")

    def show_list_providers(self):
        self.cursor.execute('SELECT * FROM "Providers" LIMIT 10;')
        self.show_answer("Список поставщиков\nid, name, description\n")

    def show_list_ingridients(self):
        self.cursor.execute('SELECT * FROM "Ingridient" LIMIT 10;')
        self.show_answer("Список ингредиентов\nid, name, price, description\n")

    def show_list_purchase(self):
        self.cursor.execute('SELECT * FROM "Purchase" LIMIT 10;')
        self.show_answer("Список покупок\ncustomer_id, time_bought, id, complete, current_price\n")

    def show_add_menu(self):
        self.destroy_all()
        self.create_console('Переход на страницу добавления')
        self.active_elements['add_ingridient'] = create_button(font_color='#ffffff', text="Добавить ингредиент",
                                                               command=self.show_add_ingridient, position=[240, 225],
                                                               background='#2998E9', width='25', height='3',
                                                               font="Sedan 12")
        self.active_elements['add_customer'] = create_button(font_color='#ffffff', text="Добавить покупателя",
                                                             command=self.show_add_customer, position=[240, 425],
                                                             background='#2998E9', width='25', height='3',
                                                             font="Sedan 12")
        self.active_elements['add_good'] = create_button(font_color='#ffffff', text="Добавить товар в покупку",
                                                         command=self.show_add_good, position=[240, 325],
                                                         background='#2998E9', width='25', height='3',
                                                         font="Sedan 12")
        self.active_elements['add_dish'] = create_button(font_color='#ffffff', text="Добавить блюдо",
                                                         command=self.show_add_dish, position=[240, 525],
                                                         background='#2998E9', width='25', height='3',
                                                         font="Sedan 12")
        self.active_elements['add_restaraun'] = create_button(font_color='#ffffff', text="Добавить ресторан",
                                                              command=self.show_add_restaraun, position=[240, 625],
                                                              background='#2998E9', width='25', height='3',
                                                              font="Sedan 12")
        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 725], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")

    def show_add_ingridient(self):
        self.destroy_all()
        self.create_console('Переход на страницу добавления ингридиента')
        self.active_elements['ingridient_name'] = create_label(font_color="#000000",
                                                               text="Название блюда", position=[self.x, 275],
                                                               background="#b5effb",
                                                               font="Sedan 14")
        self.active_elements['ingridient_name_entry'] = create_entry(width=25, font="Sedan 14",
                                                                     position=[self.x, 325], font_color="#000000")
        self.active_elements['ingridient_description'] = create_label(font_color="#000000",
                                                                      text="Описание блюда", position=[self.x, 375],
                                                                      background="#b5effb",
                                                                      font="Sedan 14")
        self.active_elements['ingridient_description_entry'] = create_entry(width=25, font="Sedan 14",
                                                                            position=[self.x, 425],
                                                                            font_color="#000000")
        self.active_elements['ingridient_cost'] = create_label(font_color="#000000",
                                                               text="Цена блюда", position=[self.x, 475],
                                                               background="#b5effb",
                                                               font="Sedan 14")
        self.active_elements['ingridient_cost_entry'] = create_entry(width=25, font="Sedan 14",
                                                                     position=[self.x, 525], font_color="#000000")
        self.active_elements['complete'] = create_button(font_color='#ffffff', text="Выполнить",
                                                         command=self.add_ingridient, position=[425, 625],
                                                         background='#2998E9', width=12, height='3',
                                                         font="Sedan 12")
        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 725], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")

    def add_ingridient(self):
        name = self.active_elements['ingridient_name_entry'].get()
        description = self.active_elements['ingridient_description_entry'].get()
        try:
            cost = float(self.active_elements['ingridient_cost_entry'].get())
        except Exception:
            self.create_console('Что-то пошло не так')
        else:
            self.cursor.execute('INSERT INTO "Ingridient" (name, description, cost) VALUES (%s, %s, CAST(%s AS MONEY))',
                                (name, description, cost))
            self.show_main_screen()
            self.create_console('Ингриент успешно добавлен')

    def show_add_dish(self):
        self.destroy_all()
        self.create_console("Страница добавления блюда")
        self.active_elements['dish_name'] = create_label(font_color="#000000",
                                                         text="Название блюда", position=[self.x, 275],
                                                         background="#b5effb",
                                                         font="Sedan 14")
        self.active_elements['dish_name_entry'] = create_entry(width=25, font="Sedan 14",
                                                               position=[self.x, 325], font_color="#000000")
        self.active_elements['dish_description'] = create_label(font_color="#000000",
                                                                text="Описание блюда", position=[self.x, 375],
                                                                background="#b5effb",
                                                                font="Sedan 14")
        self.active_elements['dish_description_entry'] = create_entry(width=25, font="Sedan 14",
                                                                      position=[self.x, 425], font_color="#000000")
        self.active_elements['dish_cost'] = create_label(font_color="#000000",
                                                         text="Цена блюда", position=[self.x, 475],
                                                         background="#b5effb",
                                                         font="Sedan 14")
        self.active_elements['dish_cost_entry'] = create_entry(width=25, font="Sedan 14",
                                                               position=[self.x, 525], font_color="#000000")
        self.cursor.execute('SELECT id FROM "Restaurants"')
        restaraun_id = self.cursor.fetchall()
        self.active_elements['restaraun_label'] = create_label(font_color="#000000",
                                                               text="Ресторан", position=[self.x, 575],
                                                               background="#b5effb",
                                                               font="Sedan 14")
        self.active_elements['restaraun_info'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                               command=self.show_list_shops, position=[50, 625],
                                                               background='#2998E9', width=12, height='3',
                                                               font="Sedan 12")
        self.active_elements['restarun_combo'] = create_combo_box(width=12, font_color="#000000",
                                                                  position=[self.x, 625], values=restaraun_id,
                                                                  font="Sedan 14", default=0)
        self.cursor.execute('SELECT id FROM "Dish_types"')
        dish_id = self.cursor.fetchall()
        self.active_elements['dish_label'] = create_label(font_color="#000000",
                                                          text="Тип блюда", position=[self.x, 675],
                                                          background="#b5effb",
                                                          font="Sedan 14")
        self.active_elements['dish_info'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                          command=self.show_list_dishes, position=[50, 725],
                                                          background='#2998E9', width=12, height='3',
                                                          font="Sedan 12")
        self.active_elements['dish_combo'] = create_combo_box(width=12, font_color="#000000",
                                                              position=[self.x, 725], values=dish_id,
                                                              font="Sedan 14", default=0)
        self.active_elements['complete'] = create_button(font_color='#ffffff', text="Выполнить",
                                                         command=self.add_dish, position=[425, 775],
                                                         background='#2998E9', width=12, height='3',
                                                         font="Sedan 12")
        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 725], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")

    def add_dish(self):
        name = self.active_elements['dish_name_entry'].get()
        description = self.active_elements['dish_description_entry'].get()
        try:
            cost = float(self.active_elements['dish_cost_entry'].get())
        except Exception:
            self.create_console('Что-то пошло не так')
        else:
            dish_type = self.active_elements['dish_combo'].get()
            restaraun = self.active_elements['restarun_combo'].get()
            self.cursor.execute(
                'INSERT INTO "Dishes" (dish_name, dish_description, dish_cost, dish_type_id, restaraun_id) VALUES ('
                '%s, %s, CAST(%s AS MONEY), %s, %s)',
                (name, description, cost, dish_type, restaraun))
            self.return_to_main_screen()
            self.create_console('Блюдо успешно добавлено')

    def show_add_restaraun(self):
        self.destroy_all()
        self.create_console("Страница добавления ресторана")
        self.active_elements['rest_name'] = create_label(font_color="#000000",
                                                         text="Название ресторана", position=[self.x, 375],
                                                         background="#b5effb",
                                                         font="Sedan 14")
        self.active_elements['rest_name_entry'] = create_entry(width=25, font="Sedan 14",
                                                               position=[self.x, 425], font_color="#000000")
        self.active_elements['rest_description'] = create_label(font_color="#000000",
                                                                text="Описание ресторана", position=[self.x, 475],
                                                                background="#b5effb",
                                                                font="Sedan 14")
        self.active_elements['rest_description_entry'] = create_entry(width=25, font="Sedan 14",
                                                                      position=[self.x, 525], font_color="#000000")
        self.active_elements['complete'] = create_button(font_color='#ffffff', text="Выполнить",
                                                         command=self.add_restaraun, position=[325, 675],
                                                         background='#2998E9', width=12, height='3',
                                                         font="Sedan 12")
        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 700], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")

    def add_restaraun(self):
        name = self.active_elements['rest_name_entry'].get()
        description = self.active_elements['rest_description_entry'].get()
        try:
            self.cursor.execute('INSERT INTO "Restaurants" (name, description) VALUES (%s, %s)', (name, description))
        except Exception:
            self.create_console("Ресторан не был добавлен")
        else:
            self.return_to_main_screen()
            self.create_console('Ресторан успешно добавлен')

    def show_add_balance(self):
        self.destroy_all()
        self.create_console('Переход на страницу добавления баланса')
        self.active_elements['customer_name'] = create_label(font_color="#000000",
                                                             text="Выберите покупателя", position=[self.x, 275],
                                                             background="#b5effb",
                                                             font="Sedan 14")
        self.cursor.execute('SELECT id FROM "Customer"')
        customers_id = self.cursor.fetchall()
        self.active_elements['customer_info'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                              command=self.show_customer_info, position=[50, 325],
                                                              background='#2998E9', width=12, height='3',
                                                              font="Sedan 12")
        self.active_elements['customer_combo'] = create_combo_box(width=12, font_color="#000000",
                                                                  position=[self.x, 325], values=customers_id,
                                                                  font="Sedan 14", default=0)
        self.active_elements['customer_balance'] = create_label(font_color="#000000",
                                                                text="Сколько денег добавляем", position=[self.x, 375],
                                                                background="#b5effb",
                                                                font="Sedan 14")
        self.active_elements['customer_balance_entry'] = create_entry(width=25, font="Sedan 14",
                                                                      position=[self.x, 425], font_color="#000000")
        self.active_elements['complete'] = create_button(font_color='#ffffff', text="Выполнить",
                                                         command=self.add_balance, position=[325, 675],
                                                         background='#2998E9', width=12, height='3',
                                                         font="Sedan 12")

        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 700], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")

    def add_balance(self):
        customer = int(self.active_elements['customer_combo'].get())
        try:
            balance = float(self.active_elements['customer_balance_entry'].get())
        except Exception:
            self.create_console('Баланс введен неверно')
        else:
            self.cursor.execute('UPDATE "Customer" SET balance=balance+CAST(%s AS MONEY) WHERE id=%s',
                                (balance, customer))
            self.create_console("Баланс успешно пополнен")
            self.return_to_main_screen()

    def destroy_all(self):
        for elem in self.active_elements:
            self.active_elements[elem].destroy()
        self.active_elements.clear()

    def show_add_good(self):
        self.destroy_all()
        self.create_console('Переход на страницу добавления товара')
        self.active_elements['label'] = create_label(font_color="#0C8EEC",
                                                     text="Страница добавления товара",
                                                     position=[400, 40], background="#b5effb",
                                                     font="Sedan 14")
        self.active_elements['customer_name'] = create_label(font_color="#000000",
                                                             text="Выберите покупателя", position=[self.x, 275],
                                                             background="#b5effb",
                                                             font="Sedan 14")
        self.cursor.execute('SELECT id FROM "Customer"')
        customers_id = self.cursor.fetchall()
        self.active_elements['customer_info'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                              command=self.show_customer_info, position=[50, 325],
                                                              background='#2998E9', width=12, height='3',
                                                              font="Sedan 12")
        self.active_elements['customer_combo'] = create_combo_box(width=12, font_color="#000000",
                                                                  position=[self.x, 325], values=customers_id,
                                                                  font="Sedan 14")
        self.active_elements['customer_good'] = create_label(font_color="#000000",
                                                             text="Выберите блюдо", position=[self.x, 375],
                                                             background="#b5effb",
                                                             font="Sedan 14")
        self.cursor.execute('SELECT id FROM "Dishes"')
        dishes_id = self.cursor.fetchall()
        self.active_elements['good_info'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                          command=self.show_list_dishes, position=[50, 425],
                                                          background='#2998E9', width=12, height='3',
                                                          font="Sedan 12")
        self.active_elements['dishes_info'] = create_button(font_color='#ffffff', text="Просмотреть",
                                                            command=self.show_list_dishes, position=[50, 425],
                                                            background='#2998E9', width=12, height='3',
                                                            font="Sedan 12")
        self.active_elements['customer_combo_good'] = create_combo_box(width=12, font_color="#000000",
                                                                       position=[self.x, 425], values=dishes_id,
                                                                       font="Sedan 14")

        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 700], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")
        self.active_elements['complete'] = create_button(font_color='#ffffff', text="Выполнить",
                                                         command=self.add_new_purchase, position=[325, 675],
                                                         background='#2998E9', width=12, height='3',
                                                         font="Sedan 12")

    def show_add_customer(self):
        self.destroy_all()
        self.create_console('Переход на страницу добавления покупателя')
        self.active_elements['label'] = create_label(font_color="#0C8EEC",
                                                     text="Страница добавления покупателя",
                                                     position=[400, 40], background="#b5effb",
                                                     font="Sedan 14")
        self.active_elements['customer_name'] = create_label(font_color="#000000",
                                                             text="Имя покупателя", position=[self.x, 275],
                                                             background="#b5effb",
                                                             font="Sedan 14")
        self.active_elements['customer_name_entry'] = create_entry(width=25, font="Sedan 14",
                                                                   position=[self.x, 325], font_color="#000000")
        self.active_elements['customer_surname'] = create_label(font_color="#000000",
                                                                text="Фамилия покупателя", position=[self.x, 175],
                                                                background="#b5effb",
                                                                font="Sedan 14")
        self.active_elements['customer_surname_entry'] = create_entry(width=25, font="Sedan 14",
                                                                      position=[self.x, 225], font_color="#000000")
        self.active_elements['balance'] = create_label(font_color="#000000",
                                                       text="Баланс покупателя",
                                                       position=[self.x, 375],
                                                       background="#b5effb",
                                                       font="Sedan 14")
        self.active_elements['balance_entry'] = create_entry(width=25, font="Sedan 14",
                                                             position=[self.x, 425],
                                                             font_color="#000000")
        self.active_elements['date_born'] = create_label(font_color="#000000",
                                                         text="Дата рождения покупателя",
                                                         position=[self.x, 475],
                                                         background="#b5effb",
                                                         font="Sedan 14")
        self.active_elements['date_born_entry'] = create_entry(width=25, font="Sedan 14",
                                                               position=[self.x, 525],
                                                               font_color="#000000")
        self.active_elements['username'] = create_label(font_color="#000000",
                                                        text="Имя пользователя покупателя",
                                                        position=[self.x, 575],
                                                        background="#b5effb",
                                                        font="Sedan 14")
        self.active_elements['username_entry'] = create_entry(width=25, font="Sedan 14",
                                                              position=[self.x, 625],
                                                              font_color="#000000")

        self.active_elements['customer_sex'] = create_label(font_color="#000000",
                                                            text="Выберите пол покупателя", position=[self.x, 675],
                                                            background="#b5effb",
                                                            font="Sedan 14")
        self.active_elements['customer_sex_combo'] = create_combo_box(width=12, font_color="#000000",
                                                                      position=[self.x, 725],
                                                                      values=['мужской', 'женский'],
                                                                      font="Sedan 14")

        self.active_elements['go_back'] = create_button(font_color='#ffffff', text="Назад",
                                                        command=self.return_to_main_screen,
                                                        position=[1000, 700], background='#2998E9', width='25',
                                                        height='3', font="Sedan 12")
        self.active_elements['complete'] = create_button(font_color='#ffffff', text="Выполнить",
                                                         command=self.add_new_customer, position=[325, 775],
                                                         background='#2998E9', width=12, height='3',
                                                         font="Sedan 12")

    def add_new_customer(self):
        name = self.active_elements['customer_name_entry'].get()
        surname = self.active_elements['customer_surname_entry'].get()
        date_born = self.active_elements['date_born_entry'].get()
        balance = self.active_elements['balance_entry'].get()
        username = self.active_elements['username_entry'].get()
        sex = self.active_elements['customer_sex_combo'].get()
        if sex == 'мужской':
            sex = True
        else:
            sex = False
        try:
            self.cursor.execute(
                'INSERT INTO "Customer" (name, surname, date_born, balance, username, sex) VALUES (%s, %s, %s, %s, '
                '%s, %s)',
                (name, surname, date_born, balance, username, sex))
        except Exception:
            self.create_console('Ошибка при вводе данных, пользователь не был добавлен')
        else:
            self.create_console('Пользователь успешно добавлен')
        self.show_main_screen()

    def add_new_purchase(self):
        customer = int(self.active_elements['customer_combo'].get())
        good = int(self.active_elements['customer_combo_good'].get())
        if not self.has_open_purchase(customer):
            self.add_new_purchase_for_customer(customer)
        purchase_id = self.get_purchase_id(customer)
        self.cursor.execute('SELECT * FROM "Purchase2Dishes" WHERE purchase_id = %s AND dishes_id = %s',
                            (purchase_id, good))
        if self.cursor.fetchone():
            self.create_console("Запись уже существует")
        else:
            self.cursor.execute('INSERT INTO "Purchase2Dishes" (purchase_id, dishes_id) VALUES (%s, %s)',
                                (purchase_id, good))
            self.cursor.execute('SELECT dish_cost FROM "Dishes" WHERE id=%s', (good,))
            answer = self.cursor.fetchone()[0]
            self.cursor.execute('UPDATE "Purchase" SET current_price = current_price + %s WHERE id = %s',
                                (answer, purchase_id))
            self.create_console('Покупка успешно добавлена')
            self.show_main_screen()

    def get_purchase_id(self, customer):
        self.cursor.execute('SELECT id FROM "Purchase" WHERE customer_id = %s AND complete = False', (customer,))
        return self.cursor.fetchone()[0]

    def add_new_purchase_for_customer(self, customer):
        self.cursor.execute('INSERT INTO "Purchase" (customer_id, complete, current_price) VALUES (%s, %s, %s)',
                            (customer, False, 0))

    def has_open_purchase(self, customer):
        self.cursor.execute('SELECT * FROM "Purchase" WHERE customer_id = %s AND complete = False', (customer,))
        if self.cursor.fetchone():
            return True
        return False

    def return_to_main_screen(self):
        self.create_console('Возврат на основной экран')
        self.destroy_all()
        self.show_main_screen()


if __name__ == '__main__':
    a = CustomerForm()
