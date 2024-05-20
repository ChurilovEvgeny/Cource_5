from pydantic import BaseModel, PositiveInt, AnyHttpUrl, RootModel


class Employer(BaseModel):
    """
    Класс контейнер Работодателя. Требуемые ИМЕНОВАННЫЕ параметры:\n
    - id: PositiveInt
    - name: str
    - alternate_url: AnyHttpUrl
    """
    id: PositiveInt
    name: str
    alternate_url: AnyHttpUrl

    def __str__(self):
        return (f"{30 * '*'}\n"
                f"id: {self.id}\n"
                f"Работодатель: {self.name}\n"
                f"URL: {self.alternate_url}\n")


class EmployersList(RootModel):
    """
    Класс контейнер списка работодателей. Требуемые параметры:\n
    - list[Vacancy] = None
    """
    root: list[Employer] = []

    def append(self, employer: Employer):
        """
        Добавляет объект типа Employer, описывающий работодателя в списке работодателей
        :param employer: Работодатель
        :return: None
        """
        self.root.append(employer)
