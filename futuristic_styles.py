import streamlit as st

def apply_futuristic_theme():
    """Apply a sleek futuristic theme with holographic elements"""
    
    st.markdown("""
    <style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Exo+2:wght@300;400;600;800&display=swap');
    
    /* Global styling */
    .stApp {
        background: radial-gradient(circle at 20% 80%, #120458 0%, #000000 50%, #1a0033 100%);
        color: #E0E6ED;
        font-family: 'Exo 2', sans-serif;
        overflow-x: hidden;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Animated background particles */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(2px 2px at 20px 30px, #00FFFF, transparent),
            radial-gradient(2px 2px at 40px 70px, #FF00FF, transparent),
            radial-gradient(1px 1px at 90px 40px, #FFFF00, transparent),
            radial-gradient(1px 1px at 130px 80px, #00FF00, transparent),
            radial-gradient(2px 2px at 160px 30px, #FF0080, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: float 20s infinite linear;
        opacity: 0.1;
        z-index: -1;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) translateX(0px); }
        33% { transform: translateY(-100px) translateX(100px); }
        66% { transform: translateY(-200px) translateX(-100px); }
        100% { transform: translateY(0px) translateX(0px); }
    }
    
    /* Main header */
    .main-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(45deg, #00FFFF, #FF00FF, #FFFF00, #00FF00, #FF0080);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
        text-shadow: 0 0 50px rgba(0, 255, 255, 0.5);
        margin: 0;
        line-height: 1.1;
    }
    
    .subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.4rem;
        color: #00FFFF;
        margin-top: 1rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        opacity: 0.9;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Stats bar */
    .stats-bar {
        display: flex;
        justify-content: space-around;
        padding: 2rem;
        margin: 2rem 0;
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
    }
    
    .stat-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #00FFFF;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
        animation: pulse-glow 2s ease-in-out infinite alternate;
    }
    
    .stat-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    @keyframes pulse-glow {
        from { text-shadow: 0 0 20px rgba(0, 255, 255, 0.8), 0 0 30px rgba(0, 255, 255, 0.4); }
        to { text-shadow: 0 0 25px rgba(0, 255, 255, 1), 0 0 40px rgba(0, 255, 255, 0.6); }
    }
    
    /* Dashboard sections */
    .dashboard-section {
        margin: 3rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.02), rgba(0, 255, 255, 0.03));
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 25px;
        backdrop-filter: blur(15px);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-section::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00FFFF, transparent);
        animation: scanner 4s infinite;
    }
    
    @keyframes scanner {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .section-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        color: #FF00FF;
        margin-bottom: 1.5rem;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        position: relative;
    }
    
    .section-title::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FF00FF, transparent);
    }
    
    /* Holographic data cards */
    .data-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.05), rgba(255, 0, 255, 0.05));
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .data-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0, 255, 255, 0.2);
        border-color: rgba(0, 255, 255, 0.6);
    }
    
    /* Neural network visualization */
    .neural-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 1rem;
        padding: 2rem 0;
    }
    
    .neural-node {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 255, 255, 0.8), rgba(0, 255, 255, 0.2));
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #000;
        animation: neural-pulse 2s ease-in-out infinite;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
    }
    
    .neural-node:nth-child(even) {
        animation-delay: 1s;
        background: radial-gradient(circle, rgba(255, 0, 255, 0.8), rgba(255, 0, 255, 0.2));
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.6);
    }
    
    @keyframes neural-pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    
    /* Enhanced metrics styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #00FFFF;
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
    }
    
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        color: #00FF00;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00FFFF, #FF00FF);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #FF00FF, #00FFFF);
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 3px solid rgba(0, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00FFFF;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .stats-bar {
            flex-direction: column;
            gap: 1rem;
        }
        
        .stat-value {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)