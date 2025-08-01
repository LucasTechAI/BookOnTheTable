# pages.py
"""
Páginas da aplicação BookOnTheTable Dashboard
"""

from components import display_metrics, display_recent_logs, create_feature_card
from data_processing import load_logs_data
from config import AUTO_REFRESH_INTERVAL
from charts import display_charts_grid
from api_client import LogsAPI
from streamlit import (markdown, 
                       columns, 
                       subheader, 
                       metric, 
                       info, 
                       success, 
                       error, 
                       session_state, 
                       rerun, 
                       spinner
)
from time import sleep


def home_page() -> None:
    """
    Home page of the BookOnTheTable Dashboard.
    Displays the main features and quick statistics.
    """
    markdown('<div class="tab-content">', unsafe_allow_html=True)

    create_feature_card(
        icon="🏠",
        title="Welcome to the BookOnTheTable Dashboard",
        description=(
            "A complete monitoring and management system for the BookOnTheTable platform. "
            "Use the tabs above to navigate through the different features."
        )
    )

    col1, col2 = columns(2)

    with col1:
        create_feature_card(
            icon="🔧",
            title="Technical Information",
            description="Details about the current API environment.",
            features=[
                "Base API: book-on-the-table.vercel.app",
                "API Version: v1",
                "Authentication: JWT Bearer Token",
                "Renewal: Automatic every 15 minutes"
            ]
        )

    with col2:
        create_feature_card(
            icon="📊",
            title="Log Monitoring",
            description="View real-time API requests, performance, and status.",
            features=[
                "Performance metrics",
                "Interactive charts",
                "Endpoint analysis",
                "User monitoring"
            ]
        )
        
    _display_api_status()

    _display_quick_statistics()

    markdown('</div>', unsafe_allow_html=True)

def _display_api_status() -> None:
    """
    Checks the API status and displays it in a feature card.
    """
    with spinner("Checking API status..."):
        api = LogsAPI()
        auth_success, auth_msg = api.authenticate()

    if auth_success:
        create_feature_card(
            icon="✅",
            title="API Status",
            description="Connection successfully established.",
            features=["System Online"],
            status_class="status-success"
        )
    else:
        create_feature_card(
            icon="❌",
            title="API Status",
            description=auth_msg,
            features=["System Offline"],
            status_class="status-error"
        )


def _display_quick_statistics() -> None:
    """
    Displays quick statistics about the API usage.
    """
    subheader("📈 Quick Statistics")

    api = LogsAPI()
    auth_success, _ = api.authenticate()

    if auth_success:
        with spinner("Loading statistics..."):
            df, message = load_logs_data()

        if not df.empty:
            col1, col2, col3, col4 = columns(4)

            with col1:
                metric("Requests", len(df))

            with col2:
                avg_response = df['response_time_ms'].mean()
                metric("Avg. Response Time (ms)", f"{avg_response:.1f}")

            with col3:
                success_rate = (df['status_code'].between(200, 299).sum() / len(df)) * 100
                metric("Success Rate", f"{success_rate:.1f}%")

            with col4:
                unique_ips = df['ip_address'].nunique()
                metric("Unique IPs", unique_ips)
        else:
            info("No data available for quick statistics")
    else:
        error("Failed to load statistics – API is offline")


def logs_page() -> None:
    """
    Logs page of the BookOnTheTable Dashboard.
    """
    markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    auto_refresh = session_state.get('auto_refresh', False)
    log_limit = session_state.get('log_limit', 1000)
    
    with spinner("Loading logs..."):
        df, message = load_logs_data(log_limit)
    
    if df.empty:
        _display_logs_error(message)
        markdown('</div>', unsafe_allow_html=True)
        return
    
    success(f"✅ {message}")
    
    subheader("📊 General Metrics")
    display_metrics(df)
    
    subheader("📈 Visual Analyses")
    display_charts_grid(df)
    
    display_recent_logs(df)
    
    if auto_refresh:
        sleep(AUTO_REFRESH_INTERVAL)
        rerun()
    
    markdown('</div>', unsafe_allow_html=True)


def _display_logs_error(message: str) -> None:
    """
    Displays an error message when logs cannot be loaded.
    Args:
        message (str): The error message to display.
    """
    error(f"Could not load log data: {message}")
    info("""
    **Possible causes:**
    - API unavailable
    - Authentication issue
    - Network error

    **Solutions:**
    - Check if the API is working
    - Confirm access credentials
    - Try again in a few minutes
    """)

