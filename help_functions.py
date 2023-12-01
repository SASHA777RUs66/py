
def get_ids(from_what):
    info = list()
    for item in from_what:
        temp_list = list()
        for id in item:
            temp_list.append(id[0])
        info.append(temp_list)
    return info


def check_choice(type, query, choices=None):
    while True:
        choice = input(query).strip()
        if type == str:
            try:
                int(choice)
            except Exception:
                if len(choice) != 0:
                    return choice
        if type == int:
            try:
                result = int(choice)
                if choices:
                    if result in choices:
                        return result
                    else:
                        print(f"Ваш ответ должен быть: {' или '.join(f'{choice}' for choice in choices)}")
                        raise ValueError
            except ValueError:
                print("Попробуйте еще раз)")
        else:
            if len(choice) != 0:
                return choice


def authorize():
    query = "1 - зарегистрироваться\n2 - авторизоваться\n3 - полный выход\nВаш выбор: "
    result = check_choice(int, query, [1, 2, 3])
    return result


def get_password():
    password = check_choice("", "Введите пароль: ")
    return password
