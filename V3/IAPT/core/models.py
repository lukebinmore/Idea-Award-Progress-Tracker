from dataclasses import dataclass, field
from datetime import date


@dataclass
class Student:
    id: str
    firstname: str
    lastname: str
    classname: str
    account_found: bool = False
    on_roll: bool = False
    disabled: bool = False

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

    def __str__(self):
        if self.silver_awarded:
            return f"{self.id} - {self.firstname} {self.lastname} - Silver Certificate"
        elif self.bronze_awarded:
            return f"{self.id} - {self.firstname} {self.lastname} - Bronze Certificate"

        return f"{self.id} - {self.firstname} {self.lastname} - {self.outstanding} Outstanding, {self.late} Late"


@dataclass
class Badge:
    id: str
    name: str
    completed_date: date

    def __eq__(self, other):
        return isinstance(other, Badge) and self.name == other.name

    def __str__(self):
        return f"{self.name} - Completed on {self.completed_date}"


@dataclass
class Homework:
    id: str
    badge_name: str
    category: str
    points: int
    due_date: date

    def __eq__(self, other):
        return isinstance(other, Homework) and self.id == other.id

    def __str__(self):
        if self.badge_name:
            return f"{self.badge_name} - {self.category} - {self.points} Points - Due on {self.due_date}"

        return f"{self.points} Points - Due on {self.due_date}"


@dataclass
class Class:
    name: str
    student_count: int = 0
    outstanding_count: int = 0
    late_count: int = 0
    completed_count: int = 0

    def __eq__(self, other):
        return isinstance(other, Class) and self.name == other.name

    def __str__(self):
        return f"{self.name} - {self.student_count} Students - {self.outstanding_count} Outstanding - {self.late_count} - Lates"
