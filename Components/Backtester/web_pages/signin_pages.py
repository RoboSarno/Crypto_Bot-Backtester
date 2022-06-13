from multiprocessing.dummy import current_process
import streamlit as st
import tick
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import pandas as pd
import datetime 
from PIL import Image

ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
    

# https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031
names = ['Robert','name']
usernames = ['robosar','name']
passwords = ['123','name']
def signin_page():
    global names
    global usernames
    global passwords
    
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords, 'some_cookie_name','some_signature_key',cookie_expiry_days=1)
    name, authentication_status, username = authenticator.login('Login','main')
    if authentication_status:
        st.write('Welcome *%s*' % (name))
        st.title('Some content')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    return authentication_status
    # return (name, authentication_status, username)