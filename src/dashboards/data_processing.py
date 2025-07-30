import pandas as pd
import streamlit as st
from typing import Tuple, Any
from api_client import LogsAPI
from config import DEFAULT_LOG_LIMIT


def load_logs_data(limit: int = DEFAULT_LOG_LIMIT) -> Tuple[pd.DataFrame, str]:
    """
    Carrega dados dos logs com cache
    
    Args:
        limit (int): Limite de logs para carregar
        
    Returns:
        Tuple[pd.DataFrame, str]: (dataframe, message)
    """
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
            df = process_dataframe(df)
            
        return df, message
    
    return pd.DataFrame(), message


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa o DataFrame de logs adicionando colunas derivadas
    
    Args:
        df (pd.DataFrame): DataFrame original
        
    Returns:
        pd.DataFrame: DataFrame processado
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['status_category'] = df['status_code'].apply(categorize_status)
    
    return df


def categorize_status(status_code: int) -> str:
    """
    Categoriza códigos de status HTTP
    
    Args:
        status_code (int): Código de status HTTP
        
    Returns:
        str: Categoria do status
    """
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


def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas principais dos logs
    
    Args:
        df (pd.DataFrame): DataFrame de logs
        
    Returns:
        dict: Dicionário com as métricas
    """
    if df.empty:
        return {
            'total_requests': 0,
            'avg_response_time': 0,
            'success_rate': 0,
            'unique_users': 0,
            'unique_ips': 0
        }
    
    total_requests = len(df)
    avg_response_time = df['response_time_ms'].mean()
    success_rate = (df['status_code'].between(200, 299).sum() / len(df)) * 100
    unique_users = df['username'].nunique() if 'username' in df.columns else 0
    unique_ips = df['ip_address'].nunique()
    
    return {
        'total_requests': total_requests,
        'avg_response_time': avg_response_time,
        'success_rate': success_rate,
        'unique_users': unique_users,
        'unique_ips': unique_ips
    }


def get_status_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna distribuição de status
    
    Args:
        df (pd.DataFrame): DataFrame de logs
        
    Returns:
        pd.DataFrame: DataFrame com distribuição de status
    """
    if df.empty:
        return pd.DataFrame()
    
    status_counts = df['status_category'].value_counts().reset_index()
    status_counts.columns = ['status_category', 'count']
    return status_counts


def get_hourly_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna distribuição por hora
    
    Args:
        df (pd.DataFrame): DataFrame de logs
        
    Returns:
        pd.DataFrame: DataFrame com distribuição por hora
    """
    if df.empty:
        return pd.DataFrame()
    
    hourly_requests = df.groupby('hour').size().reset_index(name='requests')
    return hourly_requests


def get_top_endpoints(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Retorna os endpoints mais acessados
    
    Args:
        df (pd.DataFrame): DataFrame de logs
        top_n (int): Número de endpoints para retornar
        
    Returns:
        pd.Series: Série com os endpoints mais acessados
    """
    if df.empty:
        return pd.Series()
    
    return df['endpoint'].value_counts().head(top_n)


def prepare_recent_logs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara dados dos logs recentes para exibição
    
    Args:
        df (pd.DataFrame): DataFrame de logs
        n_logs (int): Número de logs recentes para retornar
        
    Returns:
        pd.DataFrame: DataFrame formatado para exibição
    """
    if df.empty:
        return pd.DataFrame()

    display_df = df[['timestamp', 'method', 'endpoint', 'status_code', 'response_time_ms', 'ip_address']].copy()
    display_df = display_df.sort_values('timestamp', ascending=False)
    
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    display_df['response_time_ms'] = display_df['response_time_ms'].round(2)
    
    return display_df