import streamlit as st
from config import APP_CONFIG
from components import create_header, create_footer, create_sidebar_info
from pages import home_page, logs_page


def configure_page() -> None:
    """Configura as definições da página"""
    st.set_page_config(
        page_title=APP_CONFIG["page_title"],
        page_icon=APP_CONFIG["page_icon"],
        layout=APP_CONFIG["layout"]
    )


def main() -> None:
    """Função principal da aplicação"""
    configure_page()
    create_header()
    
    # Criação das abas
    tab1, tab2 = st.tabs(["🏠 Home", "📊 Logs"])
    
    with tab1:
        home_page()
    
    with tab2:
        logs_page()
    
    
    # Sidebar e footer
    create_sidebar_info()
    create_footer()


if __name__ == "__main__":
    main()