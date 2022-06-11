# import hydralit as hy
import streamlit as st
import hydralit_components as hc
import config_ev
import web_pages
# ticker within database
ticker_label_list = ['ADABTC', 'ONEBTC', 'HBARBTC', 'VETBTC', 'LTCBTC', 'BCHBTC', 'ETHBTC']

# set up streamlit page layout
st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

# menu data for hydralit navigation bar
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
]

def backtester():
    """_summary_
        
            Function to start up streamlit application
    """
    # theme for hydralit navbar
    over_theme = {'txc_inactive': '#eeeee4', 'menu_background':'#063970','txc_active':'#eeeee4','option_active':'#76b5c5'}

    # make navigation bar
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        hide_streamlit_markers=False, 
        sticky_nav=True, 
        sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    )
    
    # page selection
    if f"{menu_id}" == 'Home':
        web_pages.my_home() # home page
        
    elif f"{menu_id}" == 'anal_PME':
        web_pages.strat1_anal_page(2,1) # anal page for strat 1
        
    elif f"{menu_id}" == 'anal_RES':
        web_pages.strat2_anal_page(2,1) # anal page for strat 2
        
    elif f"{menu_id}" == 'anal_H':
        web_pages.strat4_anal_page(2,1) # anal page for strat 4
        
    elif f"{menu_id}" == 'Download Data':
        web_pages.download_csv_page() # download data page
        
    elif f"{menu_id}" == 'Forcasting Beta':
        web_pages.forecasting_page() # forcasting close page
    # page selection ---------------------------

  
if __name__ == '__main__':
    # set up environment variables
    config_ev.set_environment_variables()
    backtester()

