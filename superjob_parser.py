from dotenv import load_dotenv
import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Get vacancies from SuperJob by vacancy name (keyword)'
    )
    parser.add_argument(
        '-n', '--vacancy_name',
        default='программист python',
        type=str,
        nargs='+',
        help='necessary vacancy name, default is "программист python"',
    )
    parser.add_argument(
        '-p', '--search_period',
        default=30,
        type=int,
        help='the maximum allowed period of time from the moment of opening'
                ' a vacancy (in days)',
    )
    return parser.parse_args()


def get_page_with_vacancies(url, key, params, page_index=0):
    header = { 'X-Api-App-Id': key} 
    params = { 'keyword': 'python'}
    url = 'https://api.superjob.ru/2.0/vacancies/'
    response = requests.get(url, header=header, params=params)
    print(response.text)


def get_all_pages_with_vacancies(vacancy_name, key, period="30"):
    pass


def join_vacancies_pages(data_pages):
    vacancy_list = []
    for data_page in data_pages:
        for item in data_page["objects"]:
            vacancy_list.append(item)
    return vacancy_list


def get_salary_data(vacancy_name, key, period="30"):
    vacancies = get_all_pages_with_vacancies(vacancy_name, key, period=period)
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


def main():
    load_dotenv()
    superjob_id = os.getenv("ID")
    superjob_key = os.getenv("SECRET_KEY")  
    args = parse_arguments()
    vacancy_name = ' '.join(args.vacancy_name)
    search_period = str(args.search_period)    
    #DEBUGGING
    get_page_with_vacancies("", superjob_key, {}, 0)
    exit()
    #
    salary = get_salary_data(vacancy_name, superjob_key, period=search_period)
    print(salary)


if __name__ == '__main__':
    main()