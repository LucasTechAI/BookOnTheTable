from components import create_header, create_footer
from streamlit import set_page_config, tabs
from pages import home_page, logs_page
from config import APP_CONFIG


def configure_page() -> None:
    """
    Setup Streamlit page configuration.
    Sets the page title, icon, and layout.
    """
    set_page_config(
        page_title=APP_CONFIG["page_title"],
        page_icon=APP_CONFIG["page_icon"],
        layout=APP_CONFIG["layout"]
    )


def main() -> None:
    """
    Main function to run the Streamlit dashboard.
    Configures the page and sets up the header, footer, and tabs.
    """
    configure_page()
    create_header()
    
    tab1, tab2 = tabs(["🏠 Home", "📊 Logs"])
    
    with tab1:
        home_page()
    
    with tab2:
        logs_page()
    
    
    create_footer()


if __name__ == "__main__":
    main()