import hh_parser.py
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Count mean salary for developers'
    )
    parser.add_argument(
        '-l', '--lang_list',
        default='python',
        type=str,
        nargs='+',
        help='programming languages for comparison',
    )
    parser.add_argument(
        '-p', '--search_period',
        default=30,
        type=int,
        help='the maximum allowed period of time from the moment of opening'
                ' a vacancy (in days)',
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    for lang in args.lang_list:
        vacancy_name = ' '.join(args.vacancy_name)
        search_period = str(args.search_period)
        python_salary_data = hh_parser.get_vacancies()


if __name__ == '__main__':
    main()