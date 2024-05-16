from typing import Self

from pydantic import BaseModel, RootModel, AnyHttpUrl, PositiveInt


class Vacancy(BaseModel):
    """
    Класс контейнер Вакансии. Требуемые ИМЕНОВАННЫЕ параметры:\n
    - id: PositiveInt
    - name: str
    - alternate_url: AnyHttpUrl
    - salary: dict | None = {}
    - area: dict | None = {}
    - schedule: dict | None = {}
    """
    id: PositiveInt
    name: str
    alternate_url: AnyHttpUrl
    salary: dict | None = {}
    area: dict | None = {}
    schedule: dict | None = {}

    def __str__(self):
        return (f"{30 * '*'}\n"
                f"id: {self.id}\n"
                f"Вакансия: {self.name}\n"
                f"URL: {self.alternate_url}\n"
                f"Зарплата: {self.__salary_str()}\n"
                f"Регион: {self.__area_str()}\n"
                f"График: {self.__schedule_str()}\n")

    def __salary_str(self):
        if not self.salary:
            return "Не указана"
        else:
            from_str = f"от {self.salary['from']} {self.salary['currency']} " if self.salary['from'] else ""
            to_str = f"до {self.salary['to']} {self.salary['currency']} " if self.salary['to'] else ""
            gross = "до вычета налогов" if self.salary['to'] else "на руки"
            return (from_str + to_str + gross).strip().capitalize()

    def __area_str(self):
        if not self.area:
            return "Не указан"
        else:
            return self.area['name']

    def __schedule_str(self):
        if not self.schedule:
            return "Не указан"
        else:
            return self.schedule['name']

    def __gt__(self, other: Self):
        self.__vacancy_type_validate(other)
        if self.salary and other.salary:
            # Если оба объекты, то сравниваем from и to
            # Вычет налога игнорируем
            if int(self.salary.get("from", 0) or 0) == int(other.salary.get("from", 0) or 0):
                return int(self.salary.get("to", 0) or 0) > int(other.salary.get("to", 0) or 0)
            else:
                return int(self.salary.get("from", 0) or 0) > int(other.salary.get("from", 0) or 0)
        else:
            return self.salary is not None

    def __ge__(self, other: Self):
        self.__vacancy_type_validate(other)
        return self > other or self == other

    def __eq__(self, other: Self):
        self.__vacancy_type_validate(other)
        if self.salary and other.salary:
            # Если оба объекты, то сравниваем from и to
            # Вычет налога игнорируем
            if int(self.salary.get("from", 0) or 0) == int(other.salary.get("from", 0) or 0):
                return int(self.salary.get("to", 0) or 0) == int(other.salary.get("to", 0) or 0)
            else:
                return False
        else:
            # Если оба None значит равны
            # Если что-то None, а что-то объект, значит не равны
            return self.salary == other.salary

    @staticmethod
    def __vacancy_type_validate(instance):
        if not isinstance(instance, Vacancy):
            raise TypeError("Сравнивать можно только с типом Vacancy")


class VacanciesList(RootModel):
    """
    Класс контейнер списка вакансий. Требуемые параметры:\n
    - list[Vacancy] = None
    """
    root: list[Vacancy] = []

    def append(self, vacancy: Vacancy):
        """
        Добавляет объект типа Vacancy, описывающий вакансию в список вакансий
        :param vacancy: Вакансия
        :return: None
        """
        self.root.append(vacancy)

    def remove_vacancies_by_ids(self, vacancies_id: list[int]):
        """
        Удаляет вакансии с заданными id
        :param vacancies_id: список id
        :return: None
        """
        new_root = [vac for vac in self.root if vac.id not in vacancies_id]
        if new_root:
            self.root = new_root

    def filter_vacancies_by_ids(self, vacancies_id: list[int] | None = None):
        """
        Фильтрует (оставляет) вакансии с заданными id
        :param vacancies_id: список id
        :return: None
        """
        if vacancies_id:
            new_root = [vac for vac in self.root if vac.id in vacancies_id]
            if new_root:
                self.root = new_root

    def filter_vacancies_by_keyword(self, keywords: list[str]):
        """
        Фильтрует (оставляет) вакансии по заданными ключевым словам
        :param keywords: список ключевых слов
        :return: None
        """
        new_root = [vac for vac in self.root if any([key.lower() in vac.name.lower() for key in keywords])]
        if new_root:
            self.root = new_root

    def __str__(self):
        return "Нет данных!" if not self.root else "\n".join(map(str, self.root))
