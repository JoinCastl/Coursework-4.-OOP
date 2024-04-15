import os
import requests
from src.vacancy import Vacancy
from src.abstracted_classes import GetVacancies

SUPERJOB_API_KEY = os.environ.get('SUPERJOBAPI')


class SuperJobAPI(GetVacancies):
    """Класс для подключения к сайту SJ.ru"""
    def get_vacancies(self, name_job, pages):
        sj_list = []
        head = {'Host': 'api.superjob.ru',
                'X-Api-App-Id': SUPERJOB_API_KEY
                }

        for i in range(pages):
            params = {
                'keyword': name_job,
                'count': 5,
                'page': i
            }

            response = requests.get('https://api.superjob.ru/2.0/vacancies/', params=params, headers=head)
            response_json = response.json()

            for j in response_json['objects']:
                sj_title = j['profession']
                if j['address'] is None:
                    sj_town = None
                else:
                    sj_town = j['town']['title']
                if not ((j['payment_from'] is None) or (j['payment_to'] is None)):
                    sj_salary_from = j['payment_from']
                    sj_salary_to = j['payment_to']
                else:
                    sj_salary_from = 0
                    sj_salary_to = 0
                sj_employment = j['type_of_work']['title']
                sj_url = j['link']

                sj_vacancy = Vacancy(sj_title, sj_town, sj_salary_from, sj_salary_to, sj_employment, sj_url)
                sj_list.append(sj_vacancy)

        return sj_list