# components.py
"""
Componentes da interface do usuário
"""

import streamlit as st
import base64
from datetime import datetime
from typing import Optional
from data_processing import calculate_metrics, prepare_recent_logs
from styles import get_main_styles, get_footer_styles
from config import IMAGE_PATH, FALLBACK_IMAGE_URL


def create_header() -> None:
    """Cria o cabeçalho da aplicação"""
    st.markdown(get_main_styles(), unsafe_allow_html=True)
    st.markdown("""
    <div class="main-header">
        <div class="book-icon">📚</div>
        <h1 class="main-title">BookOnTheTable</h1>
        <p class="subtitle">Monitoring and Management System</p>
    </div>
    """, unsafe_allow_html=True)


def display_metrics(df) -> None:
    """
    Exibe métricas principais em formato de cards
    
    Args:
        df: DataFrame de logs
    """
    if df.empty:
        st.warning("No data available")
        return
    
    metrics = calculate_metrics(df)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Requests", f"{metrics['total_requests']:,}")

    with col2:
        st.metric("Average Response Time (ms)", f"{metrics['avg_response_time']:.1f}")

    with col3:
        st.metric("Success Rate", f"{metrics['success_rate']:.1f}%")

    with col4:
        st.metric("Unique Users", metrics['unique_users'])

    with col5:
        st.metric("Unique IPs", metrics['unique_ips'])


def display_recent_logs(df) -> None:
    """
    Exibe logs recentes em tabela
    
    Args:
        df: DataFrame de logs
    """
    if df.empty:
        return

    st.subheader("Recent Logs")
    
    display_df = prepare_recent_logs(df)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )


def get_base64_image(image_path: str) -> Optional[str]:
    """
    Converte imagem local para base64
    
    Args:
        image_path (str): Caminho da imagem
        
    Returns:
        Optional[str]: Imagem em base64 ou None se não encontrada
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None


def create_footer() -> None:
    """Cria o footer personalizado com informações de Lucas Mendes"""
    
    image_base64 = get_base64_image(IMAGE_PATH)
    
    if image_base64:
        profile_image_src = f"data:image/jpeg;base64,{image_base64}"
    else:
        profile_image_src = FALLBACK_IMAGE_URL
    
    st.markdown(get_footer_styles(), unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="improved-footer">
            <div class="footer-container">
                <div class="profile-card">
                    <div class="profile-image-container">
                        <img src="{profile_image_src}" alt="Lucas Mendes Barbosa" class="profile-image-improved">
                        <div class="status-badge" title="Available for projects"></div>
                    </div>
                    <div class="profile-content">
                        <h2 class="profile-name-improved">Lucas Mendes Barbosa</h2>
                        <p class="profile-title-improved">Mid-Level Data Scientist</p>
                        <p class="profile-description">
                            I'm a Data & AI professional with 4+ years of experience in LLMs, NLP, data pipelines, and visualization. 
                            I use Python, SQL, and cloud tools (AWS/GCP) to build smart, scalable solutions. 
                            Passionate about NLP, XAI, and music-AI projects like Music MoodAI.
                        </p>
                    </div>
                </div>
                <div class="connect-section">
                    <h3 class="connect-title">🔗 Connect with me</h3>
                    <div class="social-section">
                        <a href="https://www.linkedin.com/in/lucas-mendes-barbosa/" target="_blank" class="social-link-improved" title="LinkedIn">
                            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" alt="LinkedIn" width="24" height="24">
                        </a>
                        <a href="https://musicmoodai.com.br" target="_blank" class="social-link-improved" title="Website">
                            <!-- Ícone de globo nítido SVG -->
                            <img src="https://cdn-icons-png.flaticon.com/512/5452/5452003.png" alt="Website" width="24" height="24">
                        </a>
                        <a href="mailto:lucas.mendestech@gmail.com" class="social-link-improved" title="Email">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png" alt="Email" width="24" height="24">
                        </a>
                        <a href="https://github.com/LucasTechAI" target="_blank" class="social-link-improved" title="GitHub">
                            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" width="24" height="24">
                        </a>
                    </div>
                </div>
                <div class="footer-divider-improved"></div>
                <div class="footer-bottom-improved">
                    <p>© 2024 Lucas Mendes Barbosa • BookOnTheTable Dashboard</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def create_sidebar_info() -> None:
    """Cria informações da sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ System Information")
    st.sidebar.info(f"""
    **Application:** BookOnTheTable Dashboard

    **Version:** 1.0.0

    **Last Updated:** {datetime.now().strftime('%H:%M:%S')}

    **API Base:** book-on-the-table.vercel.app
    
    **Status:** {'🟢 Online' if True else '🔴 Offline'}
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("📚 **Useful Resources**")
    st.sidebar.markdown("- [API Documentation](#)")
    st.sidebar.markdown("- [User Guide](#)")
    st.sidebar.markdown("- [Technical Support](#)")


def create_feature_card(icon: str, title: str, description: str, features: list[str] = None, status_class: str = "") -> None:
    """
    Cria um card de feature estilizado em HTML.

    Args:
        icon (str): Ícone da feature
        title (str): Título da feature
        description (str): Descrição da feature
        features (list, optional): Lista de itens/funcionalidades adicionais
        status_class (str, optional): Classe CSS extra para status visual
    """
    features_html = ""
    if features:
        features_html = "<ul>" + "".join(f"<li>{feature}</li>" for feature in features) + "</ul>"

    st.markdown(f"""
    <div class="feature-card {status_class}">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
        {features_html}
    </div>
    """, unsafe_allow_html=True)