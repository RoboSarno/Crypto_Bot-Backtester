from dotenv import load_dotenv
import os


def set_environment_variables():
    """_summary_
        generates evironment variables for Secret keys
    """
    load_dotenv()
    os.environ['DB_HOSTNAME'] = os.getenv("DB_HOSTNAME")
    os.environ['DB_PORT_ID'] = os.getenv("DB_PORT_ID")
    os.environ['DB_DATABASE'] = os.getenv("DB_DATABASE")
    os.environ['DB_PWD'] = os.getenv("DB_PWD")
    os.environ['DB_USERNAME'] = os.getenv("DB_USERNAME")
    
    os.environ["TWILIO_accountSid"] = os.getenv("TWILIO_accountSid")
    os.environ["TWILIO_authToken"] = os.getenv("TWILIO_authToken")
    # print('Finished setting environment variables')



