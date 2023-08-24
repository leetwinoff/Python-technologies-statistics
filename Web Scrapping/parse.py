from dataclasses import dataclass, astuple
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://djinni.co/jobs/"
PYTHON_VACANCIES = urljoin(BASE_URL, "?all-keywords=&any-of-keywords=&exclude-keywords=&primary_keyword=Python")

VACANCY_OUTPUT_CSV_PATH = "vacancies.csv"

@dataclass
class PythonJobVacancy:
    title: str
    location: str
    description: str
    additional_information: List[str]
    views: int
    applications: int