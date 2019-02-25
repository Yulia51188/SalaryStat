from dotenv import load_dotenv
import os
import argparse
import requests
import json
import time
from itertools import count


SEC_IN_DAY = 24 * 60 * 60


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Get vacancies from SuperJob by vacancy name (keyword)'
    )
    parser.add_argument(
        '-n', '--vacancy_name',
        default='разработчик python',
        type=str,
        help='necessary vacancy name, default is "разработчик python"',
    )
    parser.add_argument(
        '-p', '--search_period',
        default=30,
        type=int,
        help='the maximum allowed period of time from the moment of opening'
                ' a vacancy (in days)',
    )
    return parser.parse_args()


def get_page_with_vacancies( url, key, params, page_index=0):
    headers = { 'X-Api-App-Id': key } 
    params_with_page_index = params
    params_with_page_index ["page"] = page_index
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    if response.ok:
        return response.json()


def fetch_all_pages_with_vacancies(vacancy_name, key, period='30', 
        version='2.0', method='vacancies', 
        url_template='https://api.superjob.ru/{version}/{method}/'):
    params = { 
        'keyword': vacancy_name,
        'town': '4',
        'no_agreement': '1',
        'date_published_from': get_publication_date_from(period), 
    }
    url = url_template.format(version=version, method=method)
    vacancies = []
    for page_index in count(start=0):
        data_page = get_page_with_vacancies(url, key, params, 
                                            page_index=page_index)
        yield from data_page["objects"]
        if not data_page["more"]:
            break


def get_salary_data(vacancy_name, key, period_int=30):
    vacancies = list(fetch_all_pages_with_vacancies(
        vacancy_name, 
        key, 
        period=period_int
    ))
    salary_data = []
    for vacancy in vacancies:
        salary_data.append({
            "id": vacancy["id"],
            "name": vacancy["profession"],
            "salary_from": vacancy["payment_from"],
            "salary_to": vacancy["payment_to"],
            "salary_currency": vacancy["currency"],
        })
    return salary_data


def get_publication_date_from(period):
    period_in_sec = period * SEC_IN_DAY
    current_time = time.time()
    limit_time = int(current_time - period_in_sec) 
    return limit_time


def main():
    args = parse_arguments()
    print('Period is {0}'.format(args.search_period))
    load_dotenv()
    key = os.getenv("SECRET_KEY")     
    try:
        salary = get_salary_data(args.vacancy_name, key, period_int=args.search_period)
        print(salary)
    except requests.exceptions.HTTPError as error:
        print("Can't get data from SuperJob with error:\n {0}". format(error))


if __name__ == '__main__':
    main()