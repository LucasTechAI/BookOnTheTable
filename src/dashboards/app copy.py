import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time
import base64

# Configuração da página
st.set_page_config(
    page_title="BookOnTheTable - Dashboard",
    page_icon="📚",
    layout="wide"
)

# URLs da API
BASE_URL = "https://book-on-the-table.vercel.app/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
REGISTER_URL = f"{BASE_URL}/auth/register"
REFRESH_URL = f"{BASE_URL}/auth/refresh"
LOGS_URL = f"{BASE_URL}/logs/"

# Credenciais
ADMIN_CREDENTIALS = {
    "username": "superadmin",
    "password": "]qBKcgGG5~1OU{GR35)o@(`zv\\ja"
}

# CSS personalizado inspirado no logo BookOnTheTable
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        margin-top: 10px;
        opacity: 0.9;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3498db;
    }
    
    .status-success { border-left-color: #27ae60; }
    .status-warning { border-left-color: #f39c12; }
    .status-error { border-left-color: #e74c3c; }
    
    .book-icon {
        font-size: 3rem;
        color: #3498db;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .home-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .test-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 15px 0;
    }
    
    .api-status-ok {
        color: #27ae60;
        font-weight: bold;
    }
    
    .api-status-error {
        color: #e74c3c;
        font-weight: bold;
    }
    
    .tab-content {
        margin-top: 20px;
    }
    .profile-section {
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .profile-image {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        border: 3px solid #3498db;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        object-fit: cover;
    }
    
    .profile-info {
        text-align: left;
        min-width: 250px;
    }
    
    .profile-name {
        font-size: 36px;
        font-weight: bold;
        margin: 0;
        color: #ecf0f1;
    }
    
    .profile-title {
        font-size: 1rem;
        color: #3498db;
        margin: 5px 0;
        font-weight: 500;
    }
    
    .contact-links {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 10px;
    }
    
    .contact-link {
        color: #bdc3c7;
        text-decoration: none;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: color 0.3s ease;
    }
    
    .contact-link:hover {
        color: #3498db;
        text-decoration: none;
    }
    
    .social-icons {
        display: flex;
        gap: 15px;
        margin-left: 20px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .social-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: rgba(52, 152, 219, 0.2);
        border: 2px solid #3498db;
        border-radius: 50%;
        color: #3498db;
        text-decoration: none;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }
    
    .social-icon:hover {
        background: #3498db;
        color: white;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

class LogsAPI:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        
    def authenticate(self):
        """Autentica ou registra o usuário admin"""
        try:
            # Primeiro tenta fazer login
            login_response = requests.post(LOGIN_URL, json=ADMIN_CREDENTIALS, timeout=10)
            
            if login_response.status_code == 200:
                tokens = login_response.json()
                self.access_token = tokens.get('access_token')
                self.refresh_token = tokens.get('refresh_token')
                self.token_expiry = datetime.now() + timedelta(minutes=15)
                return True, "Login realizado com sucesso"
            
            elif login_response.status_code == 401:
                # Se login falhar, tenta registrar
                register_response = requests.post(REGISTER_URL, json=ADMIN_CREDENTIALS, timeout=10)
                
                if register_response.status_code in [200, 201]:
                    # Após registrar, faz login
                    login_response = requests.post(LOGIN_URL, json=ADMIN_CREDENTIALS, timeout=10)
                    if login_response.status_code == 200:
                        tokens = login_response.json()
                        self.access_token = tokens.get('access_token')
                        self.refresh_token = tokens.get('refresh_token')
                        self.token_expiry = datetime.now() + timedelta(minutes=15)
                        return True, "Usuário registrado e autenticado"
                        
        except requests.exceptions.Timeout:
            return False, "Timeout na conexão com a API"
        except requests.exceptions.ConnectionError:
            return False, "Erro de conexão com a API"
        except Exception as e:
            return False, f"Erro na autenticação: {str(e)}"
        
        return False, "Falha na autenticação"
    
    def refresh_access_token(self):
        """Renova o token de acesso"""
        if not self.refresh_token:
            return self.authenticate()
            
        try:
            refresh_response = requests.post(
                REFRESH_URL, 
                json={"refresh_token": self.refresh_token},
                timeout=10
            )
            
            if refresh_response.status_code == 200:
                tokens = refresh_response.json()
                self.access_token = tokens.get('access_token')
                self.token_expiry = datetime.now() + timedelta(minutes=15)
                return True, "Token renovado"
            else:
                # Se refresh falhar, autentica novamente
                return self.authenticate()
                
        except Exception as e:
            return self.authenticate()
    
    def get_headers(self):
        """Retorna headers com token de autorização"""
        if not self.access_token or datetime.now() >= self.token_expiry:
            self.refresh_access_token()
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def fetch_logs(self, limit=1000):
        """Busca logs da API"""
        try:
            params = {"limit": limit}
            response = requests.get(
                LOGS_URL, 
                params=params,
                headers=self.get_headers(),
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json(), "Logs loaded successfully"
            elif response.status_code == 401:
                success, msg = self.refresh_access_token()
                if success:
                    response = requests.get(
                        LOGS_URL, 
                        params=params,
                        headers=self.get_headers(),
                        timeout=15
                    )
                    if response.status_code == 200:
                        return response.json(), "Logs loaded after token refresh"

            return None, f"Error fetching logs: Status {response.status_code}"

        except requests.exceptions.Timeout:
            return None, "Timeout fetching logs"
        except requests.exceptions.ConnectionError:
            return None, "Connection error fetching logs"
        except Exception as e:
            return None, f"Error fetching logs: {str(e)}"

    def test_api_endpoints(self):
        """Testa todos os endpoints da API"""
        results = {}
        
        try:
            response = requests.get(f"{BASE_URL}/", timeout=10)
            results['base'] = {
                'status': response.status_code,
                'success': response.status_code < 400,
                'response_time': response.elapsed.total_seconds() * 1000
            }
        except Exception as e:
            results['base'] = {
                'status': 'Error',
                'success': False,
                'error': str(e),
                'response_time': 0
            }
        
        auth_success, auth_msg = self.authenticate()
        results['auth'] = {
            'success': auth_success,
            'message': auth_msg,
            'token_valid': self.access_token is not None
        }
        
        # Teste de logs
        if auth_success:
            logs_data, logs_msg = self.fetch_logs(10)
            results['logs'] = {
                'success': logs_data is not None,
                'message': logs_msg,
                'data_count': len(logs_data) if logs_data else 0
            }
        else:
            results['logs'] = {
                'success': False,
                'message': 'Não foi possível testar - falha na autenticação'
            }
        
        return results

def load_logs_data(limit=1000):
    """Carrega dados dos logs com cache"""
    api = LogsAPI()
    logs_data, message = api.fetch_logs(limit)
    
    if logs_data:
        # Converte para DataFrame
        if isinstance(logs_data, list):
            df = pd.DataFrame(logs_data)
        elif isinstance(logs_data, dict) and 'logs' in logs_data:
            df = pd.DataFrame(logs_data['logs'])
        else:
            df = pd.DataFrame([logs_data])
        
        if not df.empty:
            # Processa os dados
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            df['hour'] = df['timestamp'].dt.hour
            df['status_category'] = df['status_code'].apply(categorize_status)
            
        return df, message
    
    return pd.DataFrame(), message

def categorize_status(status_code):
    """Categoriza códigos de status HTTP"""
    if 200 <= status_code < 300:
        return "Success"
    elif 300 <= status_code < 400:
        return "Redirect"
    elif 400 <= status_code < 500:
        return "Client Error"
    elif 500 <= status_code:
        return "Server Error"
    else:
        return "Other"

def create_header():
    """Cria o cabeçalho da aplicação"""
    st.markdown("""
    <div class="main-header">
        <div class="book-icon">📚</div>
        <h1 class="main-title">BookOnTheTable</h1>
        <p class="subtitle">Monitoring and Management System</p>
    </div>
    """, unsafe_allow_html=True)
def get_base64_image(image_path):
    """Converte imagem local para base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def create_footer():
    """Cria o footer personalizado com informações de Lucas Mendes"""
    
    image_path = "/home/lucas/BookOnTheTable/src/dashboards/img/my.jpeg"
    image_base64 = get_base64_image(image_path)
    
    if image_base64:
        profile_image_src = f"data:image/jpeg;base64,{image_base64}"
    else:
        profile_image_src = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face&auto=format&q=80"
    
    st.markdown("""
    <style>
    .improved-footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        color: white;
        padding: 60px 40px 30px 40px;
        margin-top: 80px;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .improved-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981, #f59e0b);
    }
    
    .footer-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .profile-card {
        display: flex;
        align-items: center;
        gap: 40px;
        margin-bottom: 40px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .profile-image-container {
        position: relative;
    }
    
    .profile-image-improved {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        border: 4px solid #3b82f6;
        box-shadow: 
            0 8px 32px rgba(59, 130, 246, 0.3),
            0 4px 16px rgba(0, 0, 0, 0.2);
        object-fit: cover;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .profile-image-improved:hover {
        transform: scale(1.05);
        box-shadow: 
            0 12px 48px rgba(59, 130, 246, 0.4),
            0 6px 24px rgba(0, 0, 0, 0.3);
    }
    
    .profile-content {
        flex: 1;
        min-width: 300px;
        text-align: left;
    }
    
    .profile-name-improved {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        background: linear-gradient(135deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .profile-title-improved {
        font-size: 1.25rem;
        color: #3b82f6;
        margin: 0 0 20px 0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .profile-description {
        font-size: 1rem;
        color: #cbd5e1;
        line-height: 1.6;
        margin-bottom: 24px;
        max-width: 500px;
    }
    
    .social-section {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin: 32px 0;
        flex-wrap: wrap;
    }
    
    .social-link-improved {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        color: white;
        text-decoration: none;
        font-size: 1.5rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .connect-section {
        text-align: center;
        margin-top: 20px;
    }

    .connect-title {
        font-size: 1.3rem;
        color: #e2e8f0;
        margin-bottom: 16px;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.5px;
    }

    .footer-quote {
        margin-top: 8px;
        font-size: 0.85rem;
        color: #cbd5e1;
        font-style: italic;
    }
    .social-link-improved:hover {
        background: #3b82f6;
        border-color: #3b82f6;
        transform: translateY(-4px) scale(1.1);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        color: white;
        text-decoration: none;
    }
    
    .footer-divider-improved {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.5), transparent);
        margin: 32px 0 24px 0;
    }
    
    .footer-bottom-improved {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        padding-top: 16px;
    }
    
    @media (max-width: 768px) {
        .improved-footer {
            padding: 40px 20px 20px 20px;
        }
        
        .profile-card {
            flex-direction: column;
            text-align: center;
            gap: 24px;
        }
        
        .profile-content {
            text-align: center;
            min-width: auto;
        }
        
        .profile-name-improved {
            font-size: 2rem;
        }
        
        .contact-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-section {
            gap: 20px;
        }
        
        .social-section {
            gap: 16px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
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
                            💼
                        </a>
                        <a href="https://musicmoodai.com.br" target="_blank" class="social-link-improved" title="Website">
                            🌐
                        </a>
                        <a href="mailto:lucas.mendestech@gmail.com" class="social-link-improved" title="Email">
                            📧
                        </a>
                        <a href="https://github.com/lucasmendesbarbosa" target="_blank" class="social-link-improved" title="GitHub">
                            🐙
                        </a>
                    </div>
                </div>
                <div class="footer-divider-improved"></div>
                <div class="footer-bottom-improved">
                    <p>© 2024 Lucas Mendes Barbosa • BookOnTheTable Dashboard • Built with ❤️ using Streamlit</p>
                    <p class="footer-quote">
                        "Transforming data into insights, one dashboard at a time"
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)



def home_page():
    """Página inicial do dashboard"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="home-card">
        <h2>🏠 Welcome to the BookOnTheTable Dashboard</h2>
        <p>A complete monitoring and management system for the BookOnTheTable platform.
         Use the tabs above to navigate through the different features.</p>
    </div>
    """, unsafe_allow_html=True)

    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Log Monitoring</h3>
            <p>View real-time API requests, performance, and status.</p>
            <ul>
                <li>Performance metrics</li>
                <li>Interactive charts</li>
                <li>Endpoint analysis</li>
                <li>User monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>🔧 Technical Information</h3>
            <p><strong>Base API:</strong> book-on-the-table.vercel.app</p>
            <p><strong>API Version:</strong> v1</p>
            <p><strong>Authentication:</strong> JWT Bearer Token</p>
            <p><strong>Renewal:</strong> Automatic every 15 minutes</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🧪 System Tests</h3>
            <p>Run automated tests to check the API status.</p>
            <ul>
                <li>Connectivity test</li>
                <li>Authentication validation</li>
                <li>Endpoint verification</li>
                <li>Performance analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # API quick status
        with st.spinner("Checking API status..."):
            api = LogsAPI()
            auth_success, auth_msg = api.authenticate()

        if auth_success:
            st.markdown("""
            <div class="feature-card status-success">
                <h3>✅ API Status</h3>
                <p class="api-status-ok">System Online</p>
                <p>Connection successfully established</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feature-card status-error">
                <h3>❌ API Status</h3>
                <p class="api-status-error">System Offline</p>
                <p>{auth_msg}</p>
            </div>
            """, unsafe_allow_html=True)

    # Quick statistics
    st.subheader("📈 Quick Statistics")

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

    st.markdown('</div>', unsafe_allow_html=True)


def display_metrics(df):
    if df.empty:
        st.warning("No data available")
        return
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_requests = len(df)
        st.metric("Total Requests", f"{total_requests:,}")

    with col2:
        avg_response_time = df['response_time_ms'].mean()
        st.metric("Average Response Time (ms)", f"{avg_response_time:.1f}")

    with col3:
        success_rate = (df['status_code'].between(200, 299).sum() / len(df)) * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")

    with col4:
        unique_users = df['username'].nunique() if 'username' in df.columns else 0
        st.metric("Unique Users", unique_users)

    with col5:
        unique_ips = df['ip_address'].nunique()
        st.metric("Unique IPs", unique_ips)

def create_status_chart(df):
    """Cria gráfico de distribuição de status em barras"""
    if df.empty:
        return
    
    status_counts = df['status_category'].value_counts().reset_index()
    status_counts.columns = ['status_category', 'count']
    
    # Dois tons de azul: escuro e claro, os outros em cinza e vermelho
    colors = {
        'Success': '#1f3b73',      # Azul escuro
        'Redirect': '#4a90e2',     # Azul claro
        'Client Error': "#217fec", # Amarelo
        'Server Error': '#e74c3c', # Vermelho
        'Other': '#bdc3c7'         # Cinza
    }

    fig = px.bar(
        status_counts,
        x='status_category',
        y='count',
        title='Request Status Distribution',
        color='status_category',
        color_discrete_map=colors,
        text='count'
    )

    fig.update_layout(
        height=400,
        xaxis_title="Status Category",
        yaxis_title="Number of Requests",
    )
    fig.update_traces(textposition='outside')

    st.plotly_chart(fig, use_container_width=True)


def create_timeline_chart(df):
    """Cria gráfico de timeline das requisições"""
    if df.empty:
        return
    
    hourly_requests = df.groupby('hour').size().reset_index(name='requests')
    
    fig = px.bar(
        hourly_requests,
        x='hour',
        y='requests',
        title="Request Distribution by Hour",
        labels={'hour': 'Hour of Day', 'requests': 'Number of Requests'}
    )
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=2),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_response_time_chart(df):
    """Cria gráfico de tempo de resposta"""
    if df.empty:
        return
    
    fig = px.histogram(
        df,
        x='response_time_ms',
        nbins=30,
        title="Response Time Distribution",
        labels={'response_time_ms': 'Response Time (ms)', 'count': 'Frequency'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def create_endpoint_chart(df):
    """Cria gráfico dos endpoints mais acessados"""
    if df.empty:
        return
    
    endpoint_counts = df['endpoint'].value_counts().head(10)
    
    fig = px.bar(
        x=endpoint_counts.values,
        y=endpoint_counts.index,
        orientation='h',
        title="Top 10 Endpoints more accessed",
        labels={'x': 'Number of Requests', 'y': 'Endpoint'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def display_recent_logs(df):
    """Exibe logs recentes em tabela"""
    if df.empty:
        return

    st.subheader("Recent Logs")

    display_df = df[['timestamp', 'method', 'endpoint', 'status_code', 'response_time_ms', 'ip_address']].copy()
    display_df = display_df.sort_values('timestamp', ascending=False)
    
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    display_df['response_time_ms'] = display_df['response_time_ms'].round(2)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )

def logs_page():
    """Página de logs"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    st.sidebar.header("🔧 Log Settings")

    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)

    log_limit = st.sidebar.selectbox(
        "Log Limit",
        [100, 500, 1000, 2000],
        index=2
    )
    
    if st.sidebar.button("🔄 Update Data"):
        st.cache_data.clear()
    
    with st.spinner("Loading logs..."):
        df, message = load_logs_data(log_limit)
    
    if df.empty:
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
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.success(f"✅ {message}")
    
    st.subheader("📊 General Metrics")
    display_metrics(df)
    
    st.subheader("📈 Visual Analyses")

    col1, col2 = st.columns(2)
    
    with col1:
        create_status_chart(df)
        create_response_time_chart(df)
    
    with col2:
        create_timeline_chart(df)
        create_endpoint_chart(df)
    
    display_recent_logs(df)
    
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Função principal da aplicação"""
    create_header()
    
    tab1, tab2 = st.tabs(["🏠 Home", "📊 Logs"])
    
    with tab1:
        home_page()
    
    with tab2:
        logs_page()
    
    
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

    create_footer()

if __name__ == "__main__":
    main()