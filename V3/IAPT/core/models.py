from dataclasses import dataclass, field
from datetime import date


@dataclass
class Student:
    id: str
    firstname: str
    lastname: str
    classname: str
    account_found: bool = False

    bronze_previous: int = 0
    bronze_current: int = 0
    bronze_citizen_previous: int = 0
    bronze_citizen_current: int = 0
    bronze_worker_previous: int = 0
    bronze_worker_current: int = 0
    bronze_maker_previous: int = 0
    bronze_maker_current: int = 0
    bronze_entrepreneur_previous: int = 0
    bronze_entrepreneur_current: int = 0
    silver_previous: int = 0
    silver_current: int = 0

    badges: list[Badge] = field(default_factory=list)
    completed_homeworks: list[Homework] = field(default_factory=list)
    late_homeworks: list[Homework] = field(default_factory=list)
    missing_homeworks: list[Homework] = field(default_factory=list)
    points_from_homeworks: int = 0

    complete: int = 0
    late: int = 0
    outstanding: int = 0

    bronze_awarded: bool = False
    silver_awarded: bool = False

    def __eq__(self, other):
        return isinstance(other, Student) and self.id == other.id


@dataclass
class Badge:
    name: str
    completed_date: date

    def __eq__(self, other):
        return isinstance(other, Badge) and self.name == other.name


@dataclass
class Homework:
    badge_name: str
    category: str
    points: int
    due_date: date

    def __eq__(self, other):
        return isinstance(other, Homework) and self.badge_name == other.badge_name
