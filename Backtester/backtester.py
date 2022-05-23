# import hydralit as hy
import streamlit as st
import hydralit_components as hc
from PIL import Image

# https://github.com/okld/streamlit-elements
import config_ev
import pages
# account = {'username':'robosar', 'password':'123'}
ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']
st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)
menu_data = [
    {'icon': "🏠",
     'label': "Home"},
    {'icon': "📊",
     'label':"30 min Strategies", 
     'submenu':[{'id':'anal_PME','icon': "📈", 'label':"PME Analysis"}]},
    {'icon': "📊",
     'label':"15 min Strategies", 
     'submenu':[{'id':'anal_RES','icon': "📈", 'label':"RES Analysis"},
                {'id':'anal_H','icon': "📈", 'label':"H Analysis"}]},
    {'icon': "🧠",
     'label':"Forcasting Beta"},
    {'icon': "ℹ️",
     'label':"Download Data"},
    # {'icon': "🔒",
    #  'label':"Account",
    #  'submenu':[{'id':'sign_in','icon': "🚪", 'label':"Sign Out"},
    #             {'id':'wal_set','icon': "⚙️", 'label':"Wallet Settings"}]}
]

def backtester():
    global account
    
    over_theme = {'txc_inactive': '#eeeee4', 'menu_background':'#063970','txc_active':'#eeeee4','option_active':'#76b5c5'}
    # login_name='Logout',
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    )
    # authentication_status = pages.signin_page()
    
    # if authentication_status:
    print(f"Current page {menu_id}")
    if f"{menu_id}" == 'Home':
        pages.my_home() 
        
    elif f"{menu_id}" == 'anal_PME':
        pages.strat1_anal_page(1,1.5)
        
    elif f"{menu_id}" == 'anal_RES':
        pages.strat2_anal_page(2,1)
        
    elif f"{menu_id}" == 'anal_H':
        pages.strat4_anal_page(2,1)
        
    elif f"{menu_id}" == 'Download Data':
        st.write('Not Built Yet.')
        
    elif f"{menu_id}" == 'Forcasting Beta':
        st.write('''
                 ### Welcome to my Neural Network Forcaster:
                 
                 - Please select a ticker below
                 - Will try to predict the price for the next week.
                 - Note: This is still in beta 
                 
                 ''')
        ticker = st.selectbox(
            'What ticker would you like to forcast?',
            ticker_label_list)

        st.write('You selected:', ticker)
        b = st.button('Process Request')
        if b:
            st.write(f'''
                    ### Forcast Image for {ticker}
                    ''')
            image = Image.open('/Users/robertsarno/Documents/Spring_2022/Side_Projects/Crypto_Bot/bot/V1/Backtester/pages/graph.png')
            st.image(image)
            
    # while not account_status[1]:

  
if __name__ == '__main__':
    config_ev.set_environment_variables()
    backtester()

