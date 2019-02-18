from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    superjob_id = os.getenv("ID")
    superjob_key = os.getenv("SECRET_KEY")  
    print(superjob_id)  


if __name__ == '__main__':
    main()