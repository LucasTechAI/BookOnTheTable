from pandas import DataFrame, Timedelta, to_datetime
from data_processing import (
    get_status_distribution, 
    get_top_endpoints,
    prepare_recent_logs
)
from plotly.express import bar, line, histogram
from plotly.graph_objects import Scatter
from numpy import linspace, exp
from math import sqrt, pi
from streamlit import (markdown, 
                       date_input, 
                       cache_data,
                       warning,
                       columns, 
                       selectbox, 
                       container, 
                       expander, 
                       multiselect, 
                       button, 
                       plotly_chart,
                       session_state,
                       success,
                       rerun,
                       subheader,
                       dataframe)
BLUE_PALETTE = {
    'strong': '#1e3a8a',
    'primary': '#1e40af',  
    'secondary': '#3b82f6',
    'accent': '#60a5fa',   
    'light': '#93c5fd',    
    'pale': '#dbeafe',     
    'gradient': ['#1e3a8a', 
                 '#1e40af', 
                 '#3b82f6', 
                 '#60a5fa', 
                 '#93c5fd', 
                 '#dbeafe'
    ]
}

def create_filters_section(df: DataFrame) -> dict:
    """
    Creates an organized filters section and returns selected values
    Args:
        df (DataFrame): DataFrame containing logs data
    Returns:
        dict: Dictionary with selected filters and options
    """
    markdown("##### 🔧 Filters and Settings")
    
    with container():
        col1, col2, col3 = columns([2, 1, 1])
        
        with col1:
            df['timestamp'] = to_datetime(df['timestamp'])
            min_date = df['timestamp'].min().date()
            max_date = df['timestamp'].max().date()
            
            date_range = date_input(
                "Date Range",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date,
                help="Select period for analysis",
                key="date_filter"
            )
        
        with col2:
            view_option = selectbox(
                "Time Granularity",
                ["Hour", "Day"],
                help="Choose how to group temporal data",
                key="view_option"
            )
        
        with col3:
            log_limit = selectbox(
                "Log Limit",
                [100, 500, 1000],
                index=2,
                help="Maximum number of logs to display",
                key="log_limit"
            )
    
    with expander("⚙️ **Advanced Filters**", expanded=False):
        col4, col5, col6 = columns(3)
        
        with col4:
            if 'status_code' in df.columns:
                status_options = sorted(df['status_code'].unique().tolist())
                
                selected_status = multiselect(
                    "Status Codes",
                    options=status_options,
                    default=status_options,
                    help="Filter by specific status codes",
                    key="status_filter"
                )
            else:
                selected_status = []
        
        with col5:
            if 'method' in df.columns:
                method_options = sorted(df['method'].unique().tolist())
                
                selected_methods = multiselect(
                    "HTTP Methods",
                    options=method_options,
                    default=method_options,
                    help="Filter by specific HTTP methods",
                    key="method_filter"
                )
            else:
                selected_methods = []
        
        with col6:
            if 'endpoint' in df.columns:
                sort_order = selectbox(
                    "Sort Order",
                    ["A-Z", "Z-A"],
                    help="Sort endpoints alphabetically",
                    key="sort_filter"
                )
            else:
                sort_order = "A-Z"
    
    markdown("---")
    markdown(
        """
        <div style='display: flex; justify-content: center; margin-bottom: 1rem;'>
            <div style='background-color: #fff3cd; padding: 1rem 1.5rem; border: 1px solid #ffeeba; border-radius: 6px; color: #856404; font-size: 0.95rem; max-width: 600px;'>
                ⚠️ You must apply filters to see changes in charts and data.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    markdown(
        f"""
        <script>
        function styleButtons() {{
            const buttons = document.querySelectorAll('button');
            buttons.forEach((button, index) => {{
                const text = button.textContent;
                if (text.includes('Apply Filters')) {{
                    button.style.backgroundColor = '{BLUE_PALETTE['strong']}';
                    button.style.borderColor = '{BLUE_PALETTE['strong']}';
                    button.style.color = 'white';
                }}
                if (text.includes('Refresh Data')) {{
                    button.style.backgroundColor = '{BLUE_PALETTE['accent']}';
                    button.style.borderColor = '{BLUE_PALETTE['accent']}';
                    button.style.color = 'white';
                }}
            }});
        }}
        
        // Aplicar estilos quando a página carregar
        setTimeout(styleButtons, 100);
        
        // Reaplica a cada mudança
        new MutationObserver(styleButtons).observe(document.body, {{subtree: true, childList: true}});
        </script>
        """,
        unsafe_allow_html=True
    )
    
    col_apply, col_refresh = columns(2)

    with col_apply:
        apply_filters_btn = button(
            "🔍 Apply Filters",
            type="primary",
            help="Apply selected filters to charts and data",
            use_container_width=True,
            key="apply_btn"
        )

    with col_refresh:
        refresh_data_btn = button(
            "🔄 Refresh Data",
            type="secondary",
            help="Clear cache and reload data",
            use_container_width=True,
            key="refresh_btn"
        )
    
    if refresh_data_btn:
        cache_data.clear()
        rerun()
    
    return {
        'date_range': date_range,
        'view_option': view_option,
        'sort_order': sort_order,
        'selected_status': selected_status,
        'selected_methods': selected_methods,
        'log_limit': log_limit,
        'apply_filters': apply_filters_btn
    }


def apply_filters(df: DataFrame, filters: dict) -> DataFrame:
    """
    Applies selected filters to the DataFrame
    Args:
        df (DataFrame): Original DataFrame containing logs
        filters (dict): Dictionary with selected filters and options
    Returns:
        DataFrame: Filtered DataFrame based on selected options
    """
    df_filtered = df.copy()
    
    df_filtered['timestamp'] = to_datetime(df_filtered['timestamp'])
    df_filtered = df_filtered.head(filters['log_limit'])
    
    if len(filters['date_range']) == 2:
        start_date = to_datetime(filters['date_range'][0])
        end_date = to_datetime(filters['date_range'][1]) + Timedelta(days=1) - Timedelta(seconds=1)
        df_filtered = df_filtered[
            (df_filtered['timestamp'] >= start_date) & 
            (df_filtered['timestamp'] <= end_date)
        ]
    
    if filters['selected_status'] and 'status_code' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['status_code'].isin(filters['selected_status'])]
    
    if filters['selected_methods'] and 'method' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['method'].isin(filters['selected_methods'])]
    
    if 'endpoint' in df_filtered.columns:
        ascending = True if filters['sort_order'] == "A-Z" else False
        df_filtered = df_filtered.sort_values(
            by=['endpoint', 'timestamp'], 
            ascending=[ascending, True]
        )
    else:
        df_filtered = df_filtered.sort_values('timestamp', ascending=False)
    
    return df_filtered


def create_status_chart(df: DataFrame) -> None:
    """
    Creates status distribution bar chart with enhanced blue theme
    Args:
        df (DataFrame): DataFrame containing logs data
    Returns:
        None: Displays the chart in Streamlit
    """
    if df.empty:
        warning("📭 No data available for status chart")
        return

    status_counts = get_status_distribution(df)
    
    if status_counts.empty:
        warning("📭 No status data available")
        return

    colors = {
        'Success': BLUE_PALETTE['primary'],      
        'Redirect': BLUE_PALETTE['secondary'],   
        'Client Error': BLUE_PALETTE['accent'],  
        'Server Error': BLUE_PALETTE['light'],   
        'Other': BLUE_PALETTE['pale']            
    }

    fig = bar(
        status_counts,
        x='status_category',
        y='count',
        title='Request Status Distribution',
        color='status_category',
        color_discrete_map=colors,
        text='count'
    )

    fig.update_layout(
        height=550,  
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
        gridcolor='rgba(59,130,246,0.2)', 
        tickfont_color=BLUE_PALETTE['secondary']
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(59,130,246,0.2)', 
        tickfont_color=BLUE_PALETTE['secondary']
    )
    
    plotly_chart(fig, use_container_width=True)


def get_distribution(df: DataFrame, freq: str) -> DataFrame:
    """
    Groups logs by specified frequency and counts the number of requests.
    Args:
        df (DataFrame): DataFrame containing logs data
        freq (str): Frequency for grouping ('h' for hour, 'd' for day)
    Returns:
        DataFrame: DataFrame with timestamps and request counts
    """
    if df.empty:
        return DataFrame(columns=['timestamp', 'requests'])
    
    df['timestamp'] = to_datetime(df['timestamp'])
    df_filtered = df.set_index('timestamp').resample(freq).size().reset_index(name='requests')
    return df_filtered


def create_timeline_chart(df: DataFrame, view_option: str) -> None:
    """
    Creates line chart with request distribution by hour or day with enhanced blue theme
    Args:
        df (DataFrame): DataFrame containing logs data
        view_option (str): 'Hour' or 'Day' for grouping
    Returns:
        None: Displays the chart in Streamlit
    """
    if df.empty:
        warning("📭 No data available for timeline chart")
        return

    freq = "h" if view_option == "Hour" else "d"
    grouped_df = get_distribution(df, freq)
    
    if grouped_df.empty:
        warning("📭 No timeline data available")
        return

    fig = line(
        grouped_df,
        x='timestamp',
        y='requests',
        title=f'Request Distribution by {view_option}',
        labels={'timestamp': 'Time', 'requests': 'Number of Requests'}
    )

    fig.update_traces(
        line=dict(width=3, color=BLUE_PALETTE['secondary']),
        hovertemplate='<b>%{x}</b><br>Requests: %{y}<extra></extra>',
        fill='tonexty',
        fillcolor=f'rgba(59,130,246,0.1)' 
    )

    fig.update_layout(
        height=550,  
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=BLUE_PALETTE['primary'],
        font_color=BLUE_PALETTE['primary'],
        xaxis=dict(
            tickformat="%d/%m %Hh" if freq == "h" else "%d/%m/%Y",
            tickangle=-45,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(59,130,246,0.2)',
            tickfont_color=BLUE_PALETTE['secondary'],
            autorange=True,
            type='date'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(59,130,246,0.2)',
            tickfont_color=BLUE_PALETTE['secondary']
        )
    )

    plotly_chart(fig, use_container_width=True)

def normal_pdf(x, mu, sigma):
    return (1.0 / (sigma * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sigma) ** 2)

def create_response_time_chart(df: DataFrame) -> None:
    """
    Creates response time chart with enhanced blue theme
    Args:
        df (DataFrame): DataFrame containing logs data
    Returns:
        None: Displays the chart in Streamlit
    """
    if df.empty or 'response_time_ms' not in df.columns:
        warning("📭 No response time data available")
        return

    df_clean = df.dropna(subset=['response_time_ms'])
    
    if df_clean.empty:
        warning("📭 No valid response time data available")
        return

    avg_time = df_clean['response_time_ms'].mean()
    median_time = df_clean['response_time_ms'].median()
    p95_time = df_clean['response_time_ms'].quantile(0.95)

    fig = histogram(
        df_clean,
        x='response_time_ms',
        nbins=50,
        title="Response Time Distribution",
        labels={'response_time_ms': 'Response Time (ms)', 'count': 'Frequency'},
        color_discrete_sequence=[BLUE_PALETTE['secondary']],
        histnorm='probability density'  
    )

    try:
        mu = avg_time
        sigma = df_clean['response_time_ms'].std()
        
        x_min = df_clean['response_time_ms'].min()
        x_max = df_clean['response_time_ms'].max()
        x_curve = linspace(x_min, x_max, 200)
        
        y_curve = normal_pdf(x_curve, mu, sigma)
        
        fig.add_trace(Scatter(
            x=x_curve,
            y=y_curve,
            mode='lines',
            name='Normal Distribution Curve',
            line=dict(color='rgba(30, 64, 175, 0.8)', width=3, dash='solid'),
            showlegend=False,
            hovertemplate='<b>Normal Curve</b><br>Response Time: %{x:.1f}ms<br>Density: %{y:.6f}<extra></extra>'
        ))
    except Exception:
        pass

    fig.add_vline(
        x=avg_time, 
        line_dash="dash", 
        line_color=BLUE_PALETTE['primary'],
        line_width=2
    )
    
    fig.add_vline(
        x=median_time, 
        line_dash="dot", 
        line_color=BLUE_PALETTE['accent'],
        line_width=2
    )
    
    fig.add_vline(
        x=p95_time, 
        line_dash="dashdot", 
        line_color=BLUE_PALETTE['light'],
        line_width=2
    )

    fig.add_annotation(
        text=(
            f"<b>Statistics</b><br>"
            f"<span style='color:{BLUE_PALETTE['primary']}'>─ ─ ─</span> Mean: {avg_time:.1f}ms<br>"
            f"<span style='color:{BLUE_PALETTE['accent']}'>· · ·</span> Median: {median_time:.1f}ms<br>"
            f"<span style='color:{BLUE_PALETTE['light']}'>─ · ─</span> P95: {p95_time:.1f}ms"
        ),
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        xanchor="left", yanchor="top",
        showarrow=False,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=BLUE_PALETTE['primary'],
        borderwidth=1,
        borderpad=10,
        font=dict(size=11, color=BLUE_PALETTE['primary'])
    )

    fig.update_layout(
        height=550,  
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

    plotly_chart(fig, use_container_width=True)


def create_endpoint_chart(df: DataFrame) -> None:
    """
    Creates most accessed endpoints chart with enhanced blue theme
    Args:
        df (DataFrame): DataFrame containing logs data
    Returns:
        None: Displays the chart in Streamlit
    """
    if df.empty or 'endpoint' not in df.columns:
        warning("📭 No endpoint data available")
        return

    endpoint_counts = get_top_endpoints(df, 10)
    
    if endpoint_counts.empty:
        warning("📭 No endpoint data available")
        return

    endpoint_counts = endpoint_counts.sort_values(ascending=True)

    fig = bar(
        x=endpoint_counts.values,
        y=endpoint_counts.index,
        orientation='h',
        title="Top 10 Most Accessed Endpoints",
        labels={'x': 'Number of Requests', 'y': 'Endpoint'},
        color=endpoint_counts.values,
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        height=550, 
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

    plotly_chart(fig, use_container_width=True)


def display_charts_grid(df: DataFrame) -> DataFrame:
    """
    Displays an organized grid of charts with enhanced blue theme
    Returns filtered DataFrame for use in other components
    Args:
        df (DataFrame): DataFrame containing logs data
    Returns:
        DataFrame: Filtered DataFrame after applying selected filters
    """
    
    filters = create_filters_section(df)
    
    if 'filtered_data' not in session_state:
        session_state['filtered_data'] = df.copy()
    
    if filters['apply_filters']:
        if len(filters['date_range']) != 2:
            warning("⚠️ Please select a valid date range.")
            return session_state['filtered_data']
        
        session_state['filtered_data'] = apply_filters(df, filters)
        
        filtered_count = len(session_state['filtered_data'])
        total_count = len(df)
        success(f"✅ Filters applied! Showing {filtered_count:,} of {total_count:,} records.")
    
    df_filtered = session_state['filtered_data']
    
    if df_filtered.empty:
        warning("📭 No data found with applied filters.")
        return df_filtered

    col1, col2 = columns(2, gap="large")

    with col1:
        create_status_chart(df_filtered)
        if 'response_time_ms' in df_filtered.columns:
            create_response_time_chart(df_filtered)

    with col2:
        create_timeline_chart(df_filtered, filters['view_option'])
        if 'endpoint' in df_filtered.columns:
            create_endpoint_chart(df_filtered)
    
    display_recent_logs(df_filtered)
    
    return df_filtered


def display_recent_logs(df: DataFrame) -> None:
    """
    Shows recent logs in a table format.

    Args:
        df: DataFrame containing logs
    """
    if df.empty:
        return None

    subheader("Recent Logs")

    display_df = prepare_recent_logs(df)
    display_df.rename(columns={
        'timestamp': 'Timestamp',
        'method': 'Method',
        'endpoint': 'Endpoint',
        'status_code': 'Status Code',
        'response_time_ms': 'Response Time (ms)'
    }, inplace=True)

    dataframe(
        display_df,
        use_container_width=True,
        height=400
    )