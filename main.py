import random
from datetime import datetime

from practice4.help_functions import (check_choice, authorize, get_password, get_ids)
from practice4.sql import Users_db, Orders_db, Customers_db, Workers_db, Cars_db

user = Users_db("carsRepairing.sql")
order = Orders_db("carsRepairing.sql")
customer = Customers_db("carsRepairing.sql")
worker = Workers_db("carsRepairing.sql")
cars = Cars_db("carsRepairing.sql")


def repair_main(user_id):
    print("Уточните информацию: ")
    cars.set_car()
    cars.insert_into(cars, {"car_model": cars.model, "car_num": cars.number})
    customers = customer.select_from()
    choices = list()
    print("Выберите какой сервис Вам удобен:")
    query = ""
    for id, custom in enumerate(customers):
        query += f"\n[{id + 1}]"
        for item in custom:
            query += f" - {item}"
        choices.append(id + 1)
    query += "\nВаш выбор: "
    custom_id = check_choice(int, query, choices)
    maker = worker.select_from(worker, ['id'])
    car = cars.select_from(cars, ["id"], {"car_model": cars.model, "car_num": cars.number})
    car = car[-1][0]
    maker = maker[-1][0]
    date = datetime.now().strftime("%d/%m/%y")
    try:
        order.insert_into(order, {"car_id": car,
                                  "worker_id": maker,
                                  "customer_id": custom_id,
                                  "user_id": user_id,
                                  "order_date": date})
        print("Вы успешно записаны к нам в ФИТ-СЕРВИС, ждём ВАС!")
    except Exception as e:
        pass


def create_all_tables():
    user_column = {"id": "integer primary key autoincrement",
                   "user_name": "text not null unique",
                   "user_role": "text not null",
                   "user_password": "text not null"}
    cars_column = {"id": 'integer primary key autoincrement',
                    "car_model": "text not null",
                    "car_num": "text not null unique"}
    workers_column = {"id": "integer primary key autoincrement",
               "worker_name": "text not null",
               "worker_prof": "text",
               "worker_code": "integer not null unique"
               }
    orders_column = {"id": "integer primary key autoincrement",
                     "car_id": "integer references Cars_db(id)",
                     "worker_id": "integer references Workers_db(id)",
                     "customer_id": "integer references Customers_db(id)",
                     "user_id": "integer references User_db(id)",
                     "order_date": "date"}
    customer_column = {"id": "integer primary key autoincrement",
                "customer_title": "text not null unique",
                "customer_address": "text not null unique"}
    all_columns = [user_column, customer_column, workers_column, cars_column, orders_column]
    all_classess = [user, customer, worker, cars, order]
    for id, any_class in enumerate(all_classess):
        any_class.create_table(any_class, all_columns[id])
    try:
        customer.insert_into(customer, {"customer_title": "ФИТ-СЕРВИС СПБ", "customer_address": "Санкт-Петербург, улица Фельдшера 6"})
        customer.insert_into(customer, {"customer_title": "ФИТ-СЕРВИС МСК", "customer_address": "Москва, улица Преображения 19"})
        worker.insert_into(worker, {"worker_name": "ГЕНИЙ", "worker_code": "1111", "worker_prof": "механик"})
    except Exception as e:
        pass

def get_all_orders():
    info = list()
    mess = f"Вы '{user.name}' записаны:"
    user_id = user.select_from(user, ['id'], {"user_name": user.name,
                                              "user_password": user.password})
    order_ids = order.select_from(order, ['id'], {"user_id": user_id[-1][0]})
    worker_id = order.select_from(order, ['worker_id'], {"user_id": user_id[-1][0]})
    car_id = order.select_from(order, ['car_id'], {"user_id": user_id[-1][0]})
    customer_id = order.select_from(order, ['customer_id'], {"user_id": user_id[-1][0]})
    order_date = order.select_from(order, ['order_date'], {"user_id": user_id[-1][0]})
    ids = get_ids([worker_id, car_id, customer_id, order_date])
    work_list = list()
    car_list = list()
    cust_list = list()
    order_id = list()
    for id in order_ids:
        order_id.append(id[0])
    info.append(order_id)
    for id in ids[0]:
        worker_name = worker.select_from(worker, ["worker_name"], {"id": id})
        work_list.append(worker_name[-1][0])
    info.append(work_list)
    for id in ids[1]:
        car_info = cars.select_from(cars, ["car_model", "car_num"],
                                    {"id": id})
        car_mess = ", ".join(f'{item}' for item in list(car_info[-1]))
        car_list.append(car_mess)
    info.append(car_list)
    for id in ids[2]:
        customer_info = customer.select_from()
        customer_mess = ", ".join(f'{item}' for item in list(customer_info[-1]))
        cust_list.append(customer_mess)
    info.append(cust_list)
    info.append(ids[-1])
    for i in range(0, len(info[-1])):
        ord_id = f"Номер записи - {info[0][i]}\n"
        work = f"К работнику - {info[1][i]}\n"
        car = f"Машина - {info[2][i]}\n"
        address = f"По адресу - {info[3][i]}\n"
        date = f"Дата записи - {info[4][i]}\n"
        mess += f"\n{ord_id}{work}{car}{address}{date}{'-' * 20}"
    print(mess)
    return info


def check_order(sender):
    choice = ("[1] - Новая запись\n"
              "[2] - Посмотреть все мои записи\n"
              "[3] - Удалить запись по номеру\n"
              "[4] - Выход из программы\n"
              "Ваш выбор: ")
    result = check_choice(int, choice, [1, 2, 3, 4])
    info= get_all_orders() if ((result == 2) or (result == 3)) else list()
    if result == 2:
        result = check_order(sender)
    if result == 3:
        del_choice = "Выберите номер записи для удаления: "
        result = check_choice(int, del_choice, info[0])
        order.delete_from(order, {'id': result})
        print(f'Запись под номером {result} успешна удалена')
        result = check_order(user)
    return result

def check_job(work, sender):
    choices = [1]
    query = f"[1] - Выход из программы\n"
    if work:
        job = worker.select_from(worker, ["worker_prof"],
                                  {"worker_code": worker.code})
        print(f'Вы работаете - {job[-1][0]}')
        query += "[2] - Уволиться\n"
        choices.append(2)
    else:
        query += f"[2] - Рассказать о своей проффесии\n"
        choices.append(2)
    query += f"Ваш выбор: "
    result = check_choice(int, query, choices)
    if result == 2 and work == False:
        job = check_choice(str, "Какова Ваша проффесия: ")
        jobs = ['механик', "механик-конструктор", "старший механик", 'помощник механика',
                "кладовщик", "уборщик"]
        if job in jobs:
            print(f"Вы успешно приняты на работу: - '{job}'")
            sender.update_table(job)
            check_job(True, sender)
        else:
            print("Извините, Вы нам не подходите(\n"
                  f"Мы нуждаемся в: {', '.join(jobs)}")
            check_job(False, sender)
    if result == 2 and work == True:
        sender.update_table()
        print("Вы уволились(")
        check_job(False, sender)


def start_programm():
    choice = ("Что Вы хотите в нашем сервисе?\n"
              "[1] Починить машину\n"
              "[2] Найти работу\n"
              "Ваш выбор: ")
    result = check_choice(int, choice, [1, 2])
    role = bool(result - 1)
    if role:
        role = "работник"
    else:
        role = "пользователь"
    return role



def main():
    create_all_tables()
    print("Добро пожаловать в ФИТ-СЕРВИС")
    while True:
        auth = authorize()
        if auth == 2:
            user.set_name(check_choice(str, "Введите Ваше имя: "))
            password = get_password()
            user.set_pass(password)
            new_user = user.select_from(user, ['user_role'], {"user_name": user.name,
                                                      "user_password": password})
            if len(new_user) == 0:
                print("Неверный логин или пароль")
            else:
                user.set_role(new_user[-1][0])
                if user.role == "работник":
                    worker.set_name(user.name)
                    code = worker.select_from(worker, ["worker_code"],
                                              {"worker_name": worker.name})
                    worker.set_code(code[-1][0])
                print("успешная авторизация")
                break
        elif auth == 1:
            user.check_name()
            password = get_password()
            user.set_role(start_programm())
            user.set_pass(password)
            user.insert_into(user, {"user_name": user.name,
                                    "user_role": user.role,
                                    "user_password": user.password})
            if user.role == "работник":
                worker.set_code(f"{worker.name}_{random.randint(0,10000)}")
                worker.insert_into(worker, {"worker_name": worker.name,
                                            "worker_code": worker.code})
            break
        else:
            print("Пока")
            return
    if user.role == "пользователь":
        user_id = user.select_from(user, ['id'], {"user_name": user.name})
        result = check_order(user)
        if result == 1:
            repair_main(user_id[-1][0])
            check_order(user)
        else:
            main()
    if user.role == 'работник':
        job = worker.select_from(worker, ["worker_prof"],
                                  {"worker_code": worker.code})
        work = True if len(job) > 0 else False
        check_job(work, worker)
        main()


if __name__ == "__main__":
    main()

