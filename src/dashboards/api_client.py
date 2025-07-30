import requests
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Any
from config import (
    LOGIN_URL, REGISTER_URL, REFRESH_URL, LOGS_URL, BASE_URL,
    ADMIN_CREDENTIALS, REQUEST_TIMEOUT, LOGS_TIMEOUT, TOKEN_EXPIRY_MINUTES
)


class LogsAPI:
    """
    Class to handle API interactions for the BookOnTheTable dashboard.
    Handles authentication, token management, and fetching logs.
    """
    
    def __init__(self) -> None:
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        
    def authenticate(self) -> Tuple[bool, str]:
        """
        Autentica ou registra o usuário admin
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Primeiro tenta fazer login
            login_response = requests.post(
                LOGIN_URL, 
                json=ADMIN_CREDENTIALS, 
                timeout=REQUEST_TIMEOUT
            )
            
            if login_response.status_code == 200:
                tokens = login_response.json()
                self._set_tokens(tokens)
                return True, "Login realizado com sucesso"
            
            elif login_response.status_code == 401:
                # Se login falhar, tenta registrar
                register_response = requests.post(
                    REGISTER_URL, 
                    json=ADMIN_CREDENTIALS, 
                    timeout=REQUEST_TIMEOUT
                )
                
                if register_response.status_code in [200, 201]:
                    # Após registrar, faz login
                    login_response = requests.post(
                        LOGIN_URL, 
                        json=ADMIN_CREDENTIALS, 
                        timeout=REQUEST_TIMEOUT
                    )
                    if login_response.status_code == 200:
                        tokens = login_response.json()
                        self._set_tokens(tokens)
                        return True, "Usuário registrado e autenticado"
                        
        except requests.exceptions.Timeout:
            return False, "Timeout na conexão com a API"
        except requests.exceptions.ConnectionError:
            return False, "Erro de conexão com a API"
        except Exception as e:
            return False, f"Erro na autenticação: {str(e)}"
        
        return False, "Falha na autenticação"
    
    def _set_tokens(self, tokens: Dict[str, str]) -> None:
        """Define os tokens de acesso e refresh"""
        self.access_token = tokens.get('access_token')
        self.refresh_token = tokens.get('refresh_token')
        self.token_expiry = datetime.now() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    
    def refresh_access_token(self) -> Tuple[bool, str]:
        """
        Renova o token de acesso
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.refresh_token:
            return self.authenticate()
            
        try:
            refresh_response = requests.post(
                REFRESH_URL, 
                json={"refresh_token": self.refresh_token},
                timeout=REQUEST_TIMEOUT
            )
            
            if refresh_response.status_code == 200:
                tokens = refresh_response.json()
                self.access_token = tokens.get('access_token')
                self.token_expiry = datetime.now() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
                return True, "Token renovado"
            else:
                # Se refresh falhar, autentica novamente
                return self.authenticate()
                
        except Exception:
            return self.authenticate()
    
    def get_headers(self) -> Dict[str, str]:
        """
        Retorna headers com token de autorização
        
        Returns:
            Dict[str, str]: Headers para requisições
        """
        if not self.access_token or datetime.now() >= self.token_expiry:
            self.refresh_access_token()
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def fetch_logs(self, limit: int = 1000) -> Tuple[Optional[Any], str]:
        """
        Busca logs da API
        
        Args:
            limit (int): Limite de logs para buscar
            
        Returns:
            Tuple[Optional[Any], str]: (logs_data, message)
        """
        try:
            params = {"limit": limit}
            response = requests.get(
                LOGS_URL, 
                params=params,
                headers=self.get_headers(),
                timeout=LOGS_TIMEOUT
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
                        timeout=LOGS_TIMEOUT
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

        """
        Testa todos os endpoints da API
        
        Returns:
            Dict[str, Any]: Resultados dos testes
        """
        results = {}
        
        # Teste do endpoint base
        try:
            response = requests.get(f"{BASE_URL}/", timeout=REQUEST_TIMEOUT)
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
        
        # Teste de autenticação
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