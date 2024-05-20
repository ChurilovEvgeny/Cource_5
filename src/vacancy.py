from pydantic import BaseModel, RootModel, AnyHttpUrl, PositiveInt, validator


class Schema:
    pass


class Vacancy(BaseModel):
    """
    Класс контейнер Вакансии. Требуемые ИМЕНОВАННЫЕ параметры:\n
    - id: PositiveInt
    - employer_id: PositiveInt
    - name: str
    - alternate_url: AnyHttpUrl
    - salary: dict | None = {}
    - area: dict | None = {}
    """
    id: PositiveInt
    employer: int
    name: str
    alternate_url: AnyHttpUrl
    salary: dict | None = {}
    area: str | None

    @validator('area', always=True, pre=True)
    def validate_area(cls, v):
        if v is None:
            return None
        elif not isinstance(v, dict):
            raise TypeError('"area" type must be dict')
        if 'name' not in v:
            return "НЕ УКАЗАНО"
        return v['name']

    @validator('salary', always=True, pre=True)
    def validate_salary(cls, v):
        if v is None:
            return {'from': None, 'to': None, 'currency': "", 'gross': False}
        elif not isinstance(v, dict):
            raise TypeError('"salary" type must be dict')
        return v

    @validator('employer', always=True, pre=True)
    def validate_employer(cls, v):
        if not isinstance(v, dict):
            raise TypeError('"employer" type must be dict')
        if 'id' not in v:
            raise TypeError('"employer" must be have id')
        return v['id']

    def __str__(self):
        return (f"{30 * '*'}\n"
                f"id: {self.id}\n"
                f"id Работодателя: {self.employer}\n"
                f"Вакансия: {self.name}\n"
                f"URL: {self.alternate_url}\n"
                f"Зарплата: {self.__salary_str()}\n"
                f"Регион: {self.__area_str()}\n")

    def __salary_str(self):
        if not self.salary:
            return "Не указана"
        else:
            from_str = f"от {self.salary['from']} {self.salary['currency']} " if self.salary['from'] else ""
            to_str = f"до {self.salary['to']} {self.salary['currency']} " if self.salary['to'] else ""
            gross = "до вычета налогов" if self.salary['gross'] else "на руки"
            return (from_str + to_str + gross).strip().capitalize()

    def __area_str(self):
        if not self.area:
            return "Не указан"
        else:
            return self.area

    def to_tuple(self):
        return ((self.id, self.employer, self.name, str(self.alternate_url), self.area),
                (self.id, self.salary['from'], self.salary['to'], self.salary['currency'], self.salary['gross']))


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

    def to_list(self):
        return [v.to_tuple() for v in self.root]

    def __str__(self):
        return "Нет данных!" if not self.root else "\n".join(map(str, self.root))
