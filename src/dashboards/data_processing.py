from pandas import DataFrame, Series, to_datetime
from config import DEFAULT_LOG_LIMIT
from api_client import LogsAPI
from typing import Tuple


def load_logs_data(limit: int = DEFAULT_LOG_LIMIT) -> Tuple[DataFrame, str]:
    """
    Loads logs data from the API and processes it into a DataFrame.
    Args:
        limit (int): The maximum number of logs to retrieve. Default is DEFAULT_LOG_LIMIT.
    Returns:
        Tuple[DataFrame, str]: A tuple containing the DataFrame of logs and a message.
    """
    api = LogsAPI()
    logs_data, message = api.fetch_logs(limit)
    
    if logs_data:
        if isinstance(logs_data, list):
            df = DataFrame(logs_data)
        elif isinstance(logs_data, dict) and 'logs' in logs_data:
            df = DataFrame(logs_data['logs'])
        else:
            df = DataFrame([logs_data])
        
        if not df.empty:
            df = process_dataframe(df)
            
        return df, message
    
    return DataFrame(), message


def process_dataframe(df: DataFrame) -> DataFrame:
    """
    Processes the DataFrame to prepare it for analysis.
    Args:
        df (DataFrame): The DataFrame containing logs data.
    Returns:
        DataFrame: Processed DataFrame with additional columns.
    """
    df['timestamp'] = to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['status_category'] = df['status_code'].apply(categorize_status)
    
    return df


def categorize_status(status_code: int) -> str:
    """
    Categorizes HTTP status codes into groups.
    Args:
        status_code (int): The HTTP status code.
    Returns:
        str: The category of the status code.
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


def calculate_metrics(df: DataFrame) -> dict:
    """
    Calculates key metrics from the logs DataFrame.
    Args:
        df (DataFrame): The DataFrame containing logs data.
    Returns:
        dict: A dictionary containing calculated metrics.
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


def get_status_distribution(df: DataFrame) -> DataFrame:
    """
    Gets the status distribution from the logs DataFrame.
    Args:
        df (DataFrame): The DataFrame containing logs data.
    Returns:
        DataFrame: DataFrame with status distribution.
    """
    if df.empty:
        return DataFrame()
    
    status_counts = df['status_category'].value_counts().reset_index()
    status_counts.columns = ['status_category', 'count']
    return status_counts


def get_hourly_distribution(df: DataFrame) -> DataFrame:
    """
    Gets the hourly distribution of requests from the logs DataFrame.
    Args:
        df (DataFrame): The DataFrame containing logs data.
    Returns:
        DataFrame: DataFrame with hourly request counts.
    """
    if df.empty:
        return DataFrame()
    
    hourly_requests = df.groupby('hour').size().reset_index(name='requests')
    return hourly_requests


def get_top_endpoints(df: DataFrame, top_n: int = 10) -> Series:
    """
    Gets the top accessed endpoints from the logs DataFrame.
    Args:
        df (DataFrame): The DataFrame containing logs data.
        top_n (int): The number of top endpoints to return.
    Returns:
        Series: Series with the top accessed endpoints.
    """
    if df.empty:
        return Series()
    
    return df['endpoint'].value_counts().head(top_n)


def prepare_recent_logs(df: DataFrame) -> DataFrame:
    """
    Prepares the recent logs DataFrame for display.
    Args:
        df (DataFrame): The DataFrame containing logs data.
    Returns:
        DataFrame: DataFrame formatted for display.
    """
    if df.empty:
        return DataFrame()

    display_df = df[['timestamp', 'method', 'endpoint', 'status_code', 'response_time_ms']].copy()
    display_df = display_df.sort_values('timestamp', ascending=False)
    
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    display_df['response_time_ms'] = display_df['response_time_ms'].round(2)
    
    return display_df