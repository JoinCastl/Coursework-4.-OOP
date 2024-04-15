from src.utils import user_choice_hh, user_choice_sj, user_choice_both


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print('Здравствуйте! \n'
          'Эта программа поможет Вам в поиске вакансий на сайтах: HeadHunter и SuperJob. \n'
          'Введите цифру от 1 до 4: \n'
          '1 - HeadHunter \n'
          '2 - SuperJob \n'
          '3 - HeadHunter и SuperJob \n'
          '4 - Закрыть программу. \n')

    while True:
        user_choice_platform = input()
        if user_choice_platform == '1':
            print('HeadHunter')
            user_choice_hh()
            break

        elif user_choice_platform == '2':
            print('SuperJob')
            user_choice_sj()
            break

        elif user_choice_platform == '3':
            print('HeadHunter + SuperJob')
            user_choice_both()
            break

        elif user_choice_platform == '4':
            print('До свидания')
            break
        else:
            print('Неверный запрос')
            break


if __name__ == '__main__':
    user_interaction()