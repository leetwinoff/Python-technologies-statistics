import csv
import re
from dataclasses import dataclass, astuple
from typing import List

import requests
from bs4 import BeautifulSoup

from config import ALL_TECHNOLOGIES_LOWER, PYTHON_VACANCIES, VACANCY_OUTPUT_CSV_PATH


@dataclass
class PythonJobVacancy:
    title: str
    location: str
    description: str
    additional_information: List[str]
    views: int
    applications: int
    filtered_technologies: List[str]


def get_clean_description(vacancy_soup: BeautifulSoup):
    description_element = vacancy_soup.select_one(".job-list-item__description > span")
    description = description_element.get("data-original-text", "").strip().rstrip().lower()
    description = BeautifulSoup(description, "html.parser").get_text()
    return description


def get_technologies_from_description(description):
    description_words = re.split(r'[ /,]', description)
    description_words = description_words
    filtered_technologies = set([tech.upper() for tech in description_words if tech in ALL_TECHNOLOGIES_LOWER])
    return list(filtered_technologies)


def get_clean_location(vacancy_soup: BeautifulSoup):
    location = vacancy_soup.select(".location-text")
    location_parts = []

    for element in location:
        location_parts.extend(re.split(r'[\n\W_]+', element.text.strip()))

    non_empty_location_parts = [part for part in location_parts if part]
    return non_empty_location_parts


def parse_single_vacancy(vacancy_soup: BeautifulSoup) -> PythonJobVacancy:
    description = get_clean_description(vacancy_soup)
    location = get_clean_location(vacancy_soup)
    additional_information_elements = vacancy_soup.select(".job-list-item__job-info .nobr")
    views_element = vacancy_soup.select_one(".bi-eye")
    applications_element = vacancy_soup.select_one(".bi-people")
    filtered_technologies = get_technologies_from_description(description)
    views = int(views_element.next_sibling.strip()) if views_element else 0
    applications = int(applications_element.next_sibling.strip()) if applications_element else 0


    return PythonJobVacancy(
        title=vacancy_soup.select_one(".job-list-item__link").text.strip().rstrip(),
        location=location,
        description=description,
        additional_information=[info.text.replace('·', '').strip() for info in additional_information_elements],
        views=views,
        applications=applications,
        filtered_technologies=filtered_technologies
    )


def get_single_page_vacancies(page_soup: BeautifulSoup) -> List[PythonJobVacancy]:
    vacancies = page_soup.select(".list-jobs__item")

    return [parse_single_vacancy(vacancy_soup) for vacancy_soup in vacancies]


def get_num_pages(page_soup: BeautifulSoup) -> int:
    pagination = page_soup.select_one(".pagination_with_numbers")

    if pagination is None:
        return 1

    return int(pagination.select("li")[-2].text)


def get_job_listings() -> List[PythonJobVacancy]:

    page = requests.get(PYTHON_VACANCIES).content
    first_page_soup = BeautifulSoup(page, "html.parser")

    num_pages = get_num_pages(first_page_soup)

    all_vacancies = get_single_page_vacancies(first_page_soup)

    for page_num in range(2, num_pages + 1):
        page = requests.get(PYTHON_VACANCIES, {"page": page_num}).content
        soup = BeautifulSoup(page, "html.parser")
        all_vacancies.extend(get_single_page_vacancies(soup))

    return all_vacancies


def write_vacancies_to_csv(vacancies: List[PythonJobVacancy]) -> None:
    with open(VACANCY_OUTPUT_CSV_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Title", "Location", "Description", "Additional Information", "Views", "Applications", "Filtered Technologies"])
        writer.writerows([astuple(vacancy) for vacancy in vacancies])


def main():
    vacancies = get_job_listings()
    write_vacancies_to_csv(vacancies)


if __name__ == "__main__":
    main()

