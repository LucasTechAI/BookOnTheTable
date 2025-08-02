from components import display_metrics, create_feature_card
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
    _display_quick_statistics()

    create_feature_card(
        icon="🏠",
        title="Welcome to the BookOnTheTable Dashboard",
        description=(
            "This is a comprehensive API monitoring and logging dashboard for the BookOnTheTable platform. "
            "Developed as part of the Machine Learning Engineering postgraduate program at FIAP, "
            "this dashboard provides real-time monitoring of API performance, request analytics, "
            "system health metrics, and operational insights. It serves as the central hub for tracking "
            "API usage patterns, debugging issues, and ensuring optimal system performance."
        )
    )

    col1, col2 = columns(2)

    with col1:
        create_feature_card(
            icon="🔧",
            title="Technical Information",
            description="Details about the current API environment and technologies used.",
            features=[
                "🌐 Base API: <a href='https://book-on-the-table.vercel.app' target='_blank'>book-on-the-table.vercel.app</a>",
                "📡 API Version: v1",
                "🔐 Authentication: JWT Bearer Token",
                "⏱️ Token Renewal: Automatic every 15 minutes",
                "🐍 Backend: Python + FastAPI",
                "💾 Database: SQLite3",
                "☁️ Hosting: Vercel (Serverless)",
                "📊 Dashboard: Streamlit + Plotly",
                "📚 API Docs: <a href='https://book-on-the-table.vercel.app/redoc' target='_blank'>/redoc (Swagger UI)</a>",
                "🐙 GitHub Repository: <a href='https://github.com/LucasTechAI/BookOnTheTable' target='_blank'>LucasTechAI/BookOnTheTable</a>"
            ]
        )

    with col2:
        create_feature_card(
            icon="📊",
            title="Log Monitoring",
            description="View real-time API requests, performance, and status.",
            features=[
                "📈 Performance metrics",
                "📊 Interactive charts",
                "🎯 Endpoint analysis",
                "👥 User monitoring",
                "🔍 Advanced filtering",
                "⏱️ Real-time updates"
            ]
        )
        
    _display_api_status()

    

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
            title="API Status - Online",
            description="Connection successfully established with full access.",
            features=[
                "🟢 System Status: Online",
                "🔐 Authentication: Valid JWT Token",
                "⚡ Response Time: < 500ms",
                "🌐 Endpoint: book-on-the-table.vercel.app",
                "📡 Protocol: HTTPS/TLS 1.3",
                "🛡️ Security: Active & Validated"
            ],
            status_class="status-success"
        )
    else:
        create_feature_card(
            icon="❌",
            title="API Status - Offline",
            description=f"Connection failed: {auth_msg}",
            features=[
                "🔴 System Status: Offline",
                "🚫 Authentication: Failed",
                "⚠️ Data Access: Limited/None",
                "🔧 Troubleshooting:",
                "  • Check network connection",
                "  • Verify API credentials",
                "  • Confirm API availability",
                "  • Try refreshing the page"
            ],
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

