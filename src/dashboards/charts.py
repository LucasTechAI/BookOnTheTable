# charts.py
"""
Chart components for the dashboard with enhanced blue color scheme
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data_processing import (
    get_status_distribution, 
    get_top_endpoints
)

# Enhanced blue color palette
BLUE_PALETTE = {
    'primary': '#1e40af',      # Dark blue
    'secondary': '#3b82f6',    # Medium blue  
    'accent': '#60a5fa',       # Light blue
    'light': '#93c5fd',        # Very light blue
    'pale': '#dbeafe',         # Pale blue
    'gradient': ['#1e3a8a', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe']
}

def _create_logs_sidebar() -> None:
    """Creates sidebar for logs page"""
    st.sidebar.header("🔧 Log Settings")

    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
    st.session_state['auto_refresh'] = auto_refresh

    log_limit = st.sidebar.selectbox(
        "Log Limit",
        [100, 500, 1000],
        index=2
    )
    st.session_state['log_limit'] = log_limit
    
    if st.sidebar.button("🔄 Update Data"):
        st.cache_data.clear()


def create_filters_section(df: pd.DataFrame) -> dict:
    """
    Creates an organized filters section and returns selected values
    """
    st.markdown("#### 🔧 Filters and Settings")
    
    # Container for filters
    with st.container():
        # First row of filters
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Date filter
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            min_date = df['timestamp'].min().date()
            max_date = df['timestamp'].max().date()
            
            date_range = st.date_input(
                "📅 Date Range",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date,
                help="Select period for analysis"
            )
        
        with col2:
            # Hour or Day selection
            view_option = st.selectbox(
                "⏰ Time Granularity",
                ["Hour", "Day"],
                help="Choose how to group temporal data"
            )
        
        with col3:
            # Sorting (if endpoint exists)
            if 'endpoint' in df.columns:
                sort_order = st.selectbox(
                    "🔤 Sort Order",
                    ["A-Z", "Z-A"],
                    help="Sort endpoints alphabetically"
                )
            else:
                sort_order = "A-Z"
    
    # Advanced filters section with expander
    with st.expander("⚙️ **Advanced Filters**", expanded=False):
        if 'status_code' in df.columns or 'method' in df.columns:
            col4, col5 = st.columns(2)
            
            with col4:
                if 'status_code' in df.columns:
                    status_options = sorted(df['status_code'].unique().tolist())
                    # Add "ALL" option at the beginning
                    status_display_options = ["ALL"] + [str(code) for code in status_options]
                    
                    selected_status_display = st.multiselect(
                        "📊 Status Codes",
                        options=status_display_options,
                        default=["ALL"],
                        help="Filter by specific status codes (ALL = show all codes)"
                    )
                    
                    # Convert back to actual values
                    if "ALL" in selected_status_display:
                        selected_status = status_options
                    else:
                        selected_status = [int(code) for code in selected_status_display if code != "ALL"]
                else:
                    selected_status = []
            
            with col5:
                if 'method' in df.columns:
                    method_options = sorted(df['method'].unique().tolist())
                    # Add "ALL" option at the beginning
                    method_display_options = ["ALL"] + method_options
                    
                    selected_methods_display = st.multiselect(
                        "🔧 HTTP Methods",
                        options=method_display_options,
                        default=["ALL"],
                        help="Filter by specific HTTP methods (ALL = show all methods)"
                    )
                    
                    # Convert back to actual values
                    if "ALL" in selected_methods_display:
                        selected_methods = method_options
                    else:
                        selected_methods = [method for method in selected_methods_display if method != "ALL"]
                else:
                    selected_methods = []
        else:
            selected_status = []
            selected_methods = []
    
    st.divider()
    
    return {
        'date_range': date_range,
        'view_option': view_option,
        'sort_order': sort_order,
        'selected_status': selected_status,
        'selected_methods': selected_methods
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Applies selected filters to the DataFrame
    """
    df_filtered = df.copy()
    
    # Date filter
    if len(filters['date_range']) == 2:
        start_date = pd.to_datetime(filters['date_range'][0])
        end_date = pd.to_datetime(filters['date_range'][1])
        df_filtered = df_filtered[
            (df_filtered['timestamp'] >= start_date) & 
            (df_filtered['timestamp'] <= end_date)
        ]
    
    # Status filter
    if filters['selected_status'] and 'status_code' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['status_code'].isin(filters['selected_status'])]
    
    # Methods filter
    if filters['selected_methods'] and 'method' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['method'].isin(filters['selected_methods'])]
    
    # Sorting
    if 'endpoint' in df_filtered.columns:
        ascending = True if filters['sort_order'] == "A-Z" else False
        df_filtered = df_filtered.sort_values(
            by=['endpoint', 'timestamp'], 
            ascending=[ascending, True]
        )
    
    return df_filtered


def create_status_chart(df: pd.DataFrame) -> None:
    """
    Creates status distribution bar chart with enhanced blue theme
    """
    if df.empty:
        st.warning("📭 No data available for status chart")
        return

    status_counts = get_status_distribution(df)

    # Enhanced blue tones color palette for status categories
    colors = {
        'Success': BLUE_PALETTE['primary'],      # Dark blue for success
        'Redirect': BLUE_PALETTE['secondary'],   # Medium blue for redirects
        'Client Error': BLUE_PALETTE['accent'],  # Light blue for client errors
        'Server Error': BLUE_PALETTE['light'],   # Very light blue for server errors
        'Other': BLUE_PALETTE['pale']            # Pale blue for others
    }

    fig = px.bar(
        status_counts,
        x='status_category',
        y='count',
        title='📊 Request Status Distribution',
        color='status_category',
        color_discrete_map=colors,
        text='count'
    )

    fig.update_layout(
        height=450,
        xaxis_title="Status Category",
        yaxis_title="Number of Requests",
        showlegend=False,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=BLUE_PALETTE['primary'],
        font_color=BLUE_PALETTE['primary']
    )
    
    fig.update_traces(
        textposition='outside',
        texttemplate='%{text}',
        hovertemplate='<b>%{x}</b><br>Requests: %{y}<extra></extra>',
        textfont_color=BLUE_PALETTE['primary']
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(59,130,246,0.2)',  # Blue grid
        tickfont_color=BLUE_PALETTE['secondary']
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(59,130,246,0.2)',  # Blue grid
        tickfont_color=BLUE_PALETTE['secondary']
    )
    
    st.plotly_chart(fig, use_container_width=True)


def get_distribution(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    """
    Groups logs by specified frequency and counts the number of requests.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_filtered = df.set_index('timestamp').resample(freq).size().reset_index(name='requests')
    return df_filtered


def create_timeline_chart(df: pd.DataFrame, view_option: str) -> None:
    """
    Creates line chart with request distribution by hour or day with enhanced blue theme
    """
    if df.empty:
        st.warning("📭 No data available for timeline chart")
        return

    freq = "h" if view_option == "Hour" else "d"
    grouped_df = get_distribution(df, freq)

    fig = px.line(
        grouped_df,
        x='timestamp',
        y='requests',
        title=f'📈 Request Distribution by {view_option}',
        labels={'timestamp': 'Time', 'requests': 'Number of Requests'}
    )

    fig.update_traces(
        line=dict(width=3, color=BLUE_PALETTE['secondary']),
        hovertemplate='<b>%{x}</b><br>Requests: %{y}<extra></extra>',
        fill='tonexty',
        fillcolor=f'rgba(59,130,246,0.1)'  # Light blue fill
    )

    fig.update_layout(
        height=450,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=BLUE_PALETTE['primary'],
        font_color=BLUE_PALETTE['primary'],
        xaxis=dict(
            tickformat="%d/%m %Hh" if freq == "H" else "%d/%m/%Y",
            tickangle=-45,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(59,130,246,0.2)',
            tickfont_color=BLUE_PALETTE['secondary']
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(59,130,246,0.2)',
            tickfont_color=BLUE_PALETTE['secondary']
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def create_response_time_chart(df: pd.DataFrame) -> None:
    """
    Creates response time chart with enhanced blue theme
    """
    if df.empty:
        st.warning("📭 No data available for response time chart")
        return

    # Calculate statistics
    avg_time = df['response_time_ms'].mean()
    median_time = df['response_time_ms'].median()

    fig = px.histogram(
        df,
        x='response_time_ms',
        nbins=30,
        title="⚡ Response Time Distribution",
        labels={'response_time_ms': 'Response Time (ms)', 'count': 'Frequency'},
        color_discrete_sequence=[BLUE_PALETTE['secondary']]
    )

    # Add mean and median lines with different blue tones
    fig.add_vline(
        x=avg_time, 
        line_dash="dash", 
        line_color=BLUE_PALETTE['primary'],
        line_width=2,
        annotation_text=f"Mean: {avg_time:.1f}ms",
        annotation_font_color=BLUE_PALETTE['primary']
    )
    
    fig.add_vline(
        x=median_time, 
        line_dash="dot", 
        line_color=BLUE_PALETTE['accent'],
        line_width=2,
        annotation_text=f"Median: {median_time:.1f}ms",
        annotation_font_color=BLUE_PALETTE['accent']
    )

    fig.update_layout(
        height=450,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        title_font_color=BLUE_PALETTE['primary'],
        font_color=BLUE_PALETTE['primary']
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(59,130,246,0.2)',
        tickfont_color=BLUE_PALETTE['secondary']
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(59,130,246,0.2)',
        tickfont_color=BLUE_PALETTE['secondary']
    )

    st.plotly_chart(fig, use_container_width=True)


def create_endpoint_chart(df: pd.DataFrame) -> None:
    """
    Creates most accessed endpoints chart with enhanced blue theme
    """
    if df.empty:
        st.warning("📭 No data available for endpoints chart")
        return

    endpoint_counts = get_top_endpoints(df, 10)

    fig = px.bar(
        x=endpoint_counts.values,
        y=endpoint_counts.index,
        orientation='h',
        title="🎯 Top 10 Most Accessed Endpoints",
        labels={'x': 'Number of Requests', 'y': 'Endpoint'},
        color=endpoint_counts.values,
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        height=450,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        coloraxis_showscale=False,
        title_font_color=BLUE_PALETTE['primary'],
        font_color=BLUE_PALETTE['primary']
    )
    
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Requests: %{x}<extra></extra>',
        marker_line_color=BLUE_PALETTE['primary'],
        marker_line_width=0.5
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(59,130,246,0.2)',
        tickfont_color=BLUE_PALETTE['secondary']
    )
    fig.update_yaxes(
        showgrid=False,
        tickfont_color=BLUE_PALETTE['secondary']
    )

    st.plotly_chart(fig, use_container_width=True)


def create_metrics_row(df: pd.DataFrame) -> None:
    """
    Creates a row of important metrics with blue theme
    """
    if df.empty:
        return
    
    # Custom CSS for blue-themed metrics
    st.markdown("""
    <style>
    .metric-container {
        background: linear-gradient(135deg, rgba(59,130,246,0.1) 0%, rgba(147,197,253,0.1) 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_requests = len(df)
        st.metric(
            "📊 Total Requests",
            f"{total_requests:,}",
            help="Total number of requests in selected period"
        )
    
    with col2:
        if 'response_time_ms' in df.columns:
            avg_response = df['response_time_ms'].mean()
            st.metric(
                "⚡ Average Time",
                f"{avg_response:.1f} ms",
                help="Average response time of requests"
            )
    
    with col3:
        if 'status_code' in df.columns:
            error_rate = (df['status_code'] >= 400).sum() / len(df) * 100
            st.metric(
                "🚨 Error Rate",
                f"{error_rate:.1f}%",
                help="Percentage of requests with errors (4xx and 5xx)"
            )
    
    with col4:
        unique_endpoints = df['endpoint'].nunique() if 'endpoint' in df.columns else 0
        st.metric(
            "🎯 Unique Endpoints",
            f"{unique_endpoints}",
            help="Number of unique endpoints accessed"
        )


def display_charts_grid(df: pd.DataFrame) -> None:
    """
    Displays an organized grid of charts with enhanced blue theme
    """
    
    # Create sidebar
    _create_logs_sidebar()
    
    # Filters section
    filters = create_filters_section(df)
    
    # Apply filters
    if len(filters['date_range']) != 2:
        st.warning("⚠️ Please select a valid date range.")
        return
    
    df_filtered = apply_filters(df, filters)
    
    if df_filtered.empty:
        st.warning("📭 No data found with applied filters.")
        return
    
    # Main metrics
    create_metrics_row(df_filtered)
    
    st.divider()
    
    # Charts grid
    col1, col2 = st.columns(2, gap="large")

    with col1:
        create_status_chart(df_filtered)
        create_response_time_chart(df_filtered)

    with col2:
        create_timeline_chart(df_filtered, filters['view_option'])
        create_endpoint_chart(df_filtered)