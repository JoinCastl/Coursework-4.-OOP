from src.hh_api import HeadHunterAPI
from src.sj_api import SuperJobAPI
from src.jsonsaver import JSONSaver


def user_choice_hh():
    keyword = input('Напишите название профессии: \n')
    hh_api = HeadHunterAPI()
    print('Сколько вывести страниц? \n')
    pages = int(input())
    from_hh = hh_api.get_vacancies(keyword, pages)
    print('Список вакансий с сайта "HeadHuter": \n')
    for i in from_hh:
        print(i)
    print('Записать, отсортированные по зарплате данные в JSON файл? \n')
    user_answer = input('Да\Нет \n').lower()
    if user_answer not in ['да']:
        print('Спасибо за использование программы!')
    else:
        jsonfile_hh = JSONSaver()
        jsonfile_hh.add_vacancies(from_hh)
        jsonfile_hh.sort_vacancies_by_salary()
        jsonfile_hh.file_writer()
        return jsonfile_hh


def user_choice_sj():
    keyword = input('Напишите название профессии: \n')
    superjob_api = SuperJobAPI()
    print('Сколько вывести страниц? \n')
    pages = int(input())
    from_sj = superjob_api.get_vacancies(keyword, pages)
    print('Список вакансий с сайта "SuperJob": \n')
    for i in from_sj:
        print(i)
    print('Записать, отсортированные по зарплате данные в JSON файл? \n')
    user_answer = input('Да\Нет \n').lower()
    if user_answer not in ['да']:
        print('Спасибо за использование программы!')
    else:
        jsonfile_sj = JSONSaver()
        jsonfile_sj.add_vacancies(from_sj)
        jsonfile_sj.sort_vacancies_by_salary()
        jsonfile_sj.file_writer()
        return jsonfile_sj


def user_choice_both():
    keyword = input('Напишите название профессии: \n')
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    print('Сколько вывести страниц? \n')
    pages = int(input())
    from_hh = hh_api.get_vacancies(keyword, pages)
    from_sj = superjob_api.get_vacancies(keyword, pages)
    print('Список вакансий с сайта "HeadHuter":\n')
    for i in from_hh:
        print(i)
    print('Список вакансий с сайта "SuperJob":\n')
    for i in from_sj:
        print(i)
    print('Записать, отсортированные по зарплате данные в JSON файл? \n')
    user_answer = input('Да\Нет \n').lower()
    if user_answer not in ['да']:
        print('Спасибо за использование программы!')
    else:
        jsonfile_all = JSONSaver()
        jsonfile_all.add_vacancies(from_hh)
        jsonfile_all.add_vacancies(from_sj)
        jsonfile_all.sort_vacancies_by_salary()
        jsonfile_all.file_writer()
        return jsonfile_all