from streamlit import markdown, warning, metric, columns
from styles import get_main_styles, get_footer_styles
from config import IMAGE_PATH, FALLBACK_IMAGE_URL
from data_processing import calculate_metrics
from base64 import b64encode
from typing import Optional
import os

def create_header() -> None:
    """
    Creates the main header with title and subtitle.
    """
    logo_path = os.path.join(os.path.dirname(__file__), "img", "logo.png")
    logo_base64 = get_base64_image(logo_path)
    
    if logo_base64:
        logo_src = f"data:image/png;base64,{logo_base64}"
        logo_html = f'<img src="{logo_src}" alt="BookOnTheTable Logo" class="logo-icon">'
    else:
        logo_html = '<div class="book-icon">📚</div>'
    
    markdown(get_main_styles(), unsafe_allow_html=True)
    
    markdown("""
    <style>
    .logo-icon {
        width: 180px;
        height: 180px;
        border-radius: 25%;
        object-fit: cover;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border: 3px solid rgba(255,255,255,0.3);
    }
    .book-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    markdown(f"""
    <div class="main-header">
        {logo_html}
        <h1 class="main-title">BookOnTheTable</h1>
        <p class="subtitle">Monitoring and Management System</p>
    </div>
    """, unsafe_allow_html=True)


def display_metrics(df) -> None:
    """
    Shows key metrics in a grid layout.
    """
    if df.empty:
        warning("No data available")
        return
    
    metrics = calculate_metrics(df)
    
    col1, col2, col3, col4, col5 = columns(5)
    
    with col1:
        metric("Total Requests", f"{metrics['total_requests']:,}")

    with col2:
        metric("Average Response Time (ms)", f"{metrics['avg_response_time']:.1f}")

    with col3:
        metric("Success Rate", f"{metrics['success_rate']:.1f}%")

    with col4:
        metric("Unique Users", metrics['unique_users'])

    with col5:
        metric("Unique IPs", metrics['unique_ips'])

def get_base64_image(image_path: str) -> Optional[str]:
    """
    Reads an image file and returns its base64 encoded string.
    Args:
        image_path (str): Path to the image file
    Returns:
        Optional[str]: Base64 encoded string of the image, or None if file not found
    """
    try:
        with open(image_path, "rb") as img_file:
            return b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None


def create_footer() -> None:
    """
    Creates the footer with profile information and social links.
    """
    
    image_base64 = get_base64_image(IMAGE_PATH)
    
    if image_base64:
        profile_image_src = f"data:image/jpeg;base64,{image_base64}"
    else:
        profile_image_src = FALLBACK_IMAGE_URL
    
    markdown(get_footer_styles(), unsafe_allow_html=True)
    
    markdown(f"""
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


def create_feature_card(icon: str, 
                        title: str, 
                        description: str, 
                        features: list[str] = None, 
                        status_class: str = ""
    ) -> None:
    """
    Creates a feature card with an icon, title, description, and optional features list.
    Args:
        icon (str): Icon to display
        title (str): Title of the card
        description (str): Description text
        features (list[str]): List of features to display
        status_class (str): CSS class for status styling
    """
    features_html = ""
    if features:
        features_html = "<ul>" + "".join(f"<li>{feature}</li>" for feature in features) + "</ul>"

    markdown(f"""
    <div class="feature-card {status_class}">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
        {features_html}
    </div>
    """, unsafe_allow_html=True)