def get_main_styles() -> str:
    """
    Returns the main styles for the dashboard.
    """
    return """
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
    </style>
    """

def get_footer_styles() -> str:
    """
    Returns the styles for the improved footer.
    """
    return """
    <style>
    .improved-footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        color: white;
        padding: 60px 40px 30px 40px;
        margin-top: 80px;
        border-radius: 20px 20px 20px 20px;
        box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
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
    """