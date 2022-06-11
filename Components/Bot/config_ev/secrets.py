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
    
    os.environ['AWS_DB_HOSTNAME'] = os.getenv("AWS_DB_HOSTNAME")
    os.environ['AWS_DB_PORT_ID'] = os.getenv("AWS_DB_PORT_ID")
    os.environ['AWS_DB_DATABASE'] = os.getenv("AWS_DB_DATABASE")
    os.environ['AWS_DB_PWD'] = os.getenv("AWS_DB_PWD")
    os.environ['AWS_DB_USERNAME'] = os.getenv("AWS_DB_USERNAME")
    
    os.environ["TWILIO_accountSid"] = os.getenv("TWILIO_accountSid")
    os.environ["TWILIO_authToken"] = os.getenv("TWILIO_authToken")
    
    
    os.environ["ALPACA_base_url"] = os.getenv("ALPACA_base_url")
    os.environ["ALPACA_api_key"] = os.getenv("ALPACA_api_key")
    os.environ["ALPACA_secret_key"] = os.getenv("ALPACA_secret_key")




