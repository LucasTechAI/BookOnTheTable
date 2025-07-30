# pages.py
"""
Páginas da aplicação BookOnTheTable Dashboard
"""

import streamlit as st
import time
from api_client import LogsAPI
from data_processing import load_logs_data
from charts import display_charts_grid
from components import display_metrics, display_recent_logs, create_feature_card
from config import AUTO_REFRESH_INTERVAL


def home_page() -> None:
    """Renderiza a página inicial do dashboard."""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)

    create_feature_card(
        icon="🏠",
        title="Welcome to the BookOnTheTable Dashboard",
        description=(
            "A complete monitoring and management system for the BookOnTheTable platform. "
            "Use the tabs above to navigate through the different features."
        )
    )

    # 🔄 Seção dividida em colunas
    col1, col2 = st.columns(2)

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

    st.markdown('</div>', unsafe_allow_html=True)

def _display_api_status() -> None:
    """Exibe o status atual da API."""
    with st.spinner("Checking API status..."):
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
    """Exibe estatísticas rápidas"""
    st.subheader("📈 Quick Statistics")

    api = LogsAPI()
    auth_success, _ = api.authenticate()

    if auth_success:
        with st.spinner("Loading statistics..."):
            df, message = load_logs_data(100)

        if not df.empty:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Requests (last 100)", len(df))

            with col2:
                avg_response = df['response_time_ms'].mean()
                st.metric("Avg. Response Time (ms)", f"{avg_response:.1f}")

            with col3:
                success_rate = (df['status_code'].between(200, 299).sum() / len(df)) * 100
                st.metric("Success Rate", f"{success_rate:.1f}%")

            with col4:
                unique_ips = df['ip_address'].nunique()
                st.metric("Unique IPs", unique_ips)
        else:
            st.info("No data available for quick statistics")
    else:
        st.error("Failed to load statistics – API is offline")


def logs_page() -> None:
    """Página de logs"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Get settings from sidebar
    auto_refresh = st.session_state.get('auto_refresh', False)
    log_limit = st.session_state.get('log_limit', 1000)
    
    # Load data
    with st.spinner("Loading logs..."):
        df, message = load_logs_data(log_limit)
    
    if df.empty:
        _display_logs_error(message)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.success(f"✅ {message}")
    
    # Display content
    st.subheader("📊 General Metrics")
    display_metrics(df)
    
    st.subheader("📈 Visual Analyses")
    display_charts_grid(df)
    
    display_recent_logs(df)
    
    # Auto refresh
    if auto_refresh:
        time.sleep(AUTO_REFRESH_INTERVAL)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)




def _display_logs_error(message: str) -> None:
    """Exibe erro de carregamento de logs"""
    st.error(f"Could not load log data: {message}")
    st.info("""
    **Possible causes:**
    - API unavailable
    - Authentication issue
    - Network error

    **Solutions:**
    - Check if the API is working
    - Confirm access credentials
    - Try again in a few minutes
    """)

