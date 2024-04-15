import json
from abc import ABC, abstractmethod
from typing import List, Tuple

import requests

API_URL = "https://api.hh.ru/vacancies"


class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, search_query: str, page: int) -> List[dict]:
        pass


class HhVacancyAPI(VacancyAPI):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_vacancies(self, search_query: str, page: int) -> List[dict]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"text": search_query, "page": page}
        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            raise Exception(f"Error getting vacancies: {response.status_code}")


class Vacancy:
    def __init__(self, title: str, url: str, salary: int, description: str):
        self.title = title
        self.url = url
        self.salary = salary or 0
        self.description = description

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def validate(self):
        if type(self.salary) not in [int, float]:
            raise ValueError("Salary must be a number")
        if not isinstance(self.title, str):
            raise ValueError("Title must be a string")
        if not isinstance(self.url, str):
            raise ValueError("URL must be a string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancies(self, vacancies: List[Vacancy]):
        pass

    @abstractmethod
    def get_vacancies(self, key: str, value: str) -> List[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancies(self, key: str, value: str):
        pass


class JsonVacancyStorage(VacancyStorage):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def add_vacancies(self, vacancies: List[Vacancy]):
        with open(self.file_name, "w") as f:
            json.dump([v.__dict__ for v in vacancies], f)

    def get_vacancies(self, key: str, value: str) -> List[Vacancy]:
        with open(self.file_name, "r") as f:
            vacancies = json.load(f)
        return [Vacancy(**v) for v in vacancies if v[key] == value]

    def delete_vacancies(self, key: str, value: str):
        with open(self.file_name, "r") as f:
            vacancies = json.load(f)
        vacancies = [v for v in vacancies if v[key] != value]
        with open(self.file_name, "w") as f:
            json.dump(vacancies, f)


def interact_with_user(vacancy_api: VacancyAPI, vacancy_storage: VacancyStorage):
    while True:
        print("\nWhat do you want to do?")
        print("1. Search for vacancies")
        print("2. Get top N vacancies by salary")
        print("3. Get vacancies with a keyword in the description")
        print("4. Exit")
        choice = input("> ")

        if choice == "1":
            search_query = input("Enter search query: ")
            vacancies = vacancy_api.get_vacancies(search_query, 0)
            print(f"Found {len(vacancies)} vacancies")
            vacancy_storage.add_vacancies(vacancies)

        elif choice == "2":
            top_n = int(input("Enter N: "))
            vacancies = vacancy_storage.get_vacancies("salary", "max")
            vacancies.sort(reverse=True)
            for i in range(min(top_n, len(vacancies))):
                print(f"{i + 1}. {vacancies[i].title} - {vacancies[i].salary}")

        elif choice == "3":
            keyword = input("Enter keyword: ")
            vacancies = vacancy_storage.get_vacancies("description", keyword)
            print(f"Found {len(vacancies)} vacancies with the keyword '{keyword}'")
            for v in vacancies:
                print(f"{v.title} - {v.url}")

        elif choice == "4":
            break

        else:
            print("Invalid choice")


def main():
    vacancy_api = HhVacancyAPI("YOUR_API_KEY")
    vacancy_storage = JsonVacancyStorage("vacancies.json")
    interact_with_user(vacancy_api, vacancy_storage)


if __name__ == "__main__":
    main()