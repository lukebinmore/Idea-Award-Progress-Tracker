from dataclasses import dataclass


@dataclass
class Student:
    id: str
    firstname: str
    lastname: str
    classname: str
    outstanding: int = 0
    late: int = 0
