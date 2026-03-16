"""
Multi-Language Code Quality Analyzer
ML-based code analysis for Python, Java, C++, and C
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import joblib
import tempfile
import os
from pathlib import Path
import time

# Import the analyzer module
try:
    from multi_language_analyzer import MultiLanguageAnalyzer
except ImportError:
    st.error("Error: multi_language_analyzer.py not found!")
    st.stop()

# Page config
st.set_page_config(
    page_title="Code Quality Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        padding: 1.5rem 0;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #b0b8c4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1e2433 0%, #242b3d 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2d3548;
    }
    
    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    .stMetric label {
        color: #9ca3af !important;
        font-size: 0.9rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #10b981 !important;
    }
    
    .info-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #232936 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #2d3548;
        margin: 1rem 0;
    }
    
    .info-card:hover {
        border-color: #4a5568;
    }
    
    .info-card h3 {
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .info-card p, .info-card ul {
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%);
        border-right: 1px solid #2d3548;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        font-weight: 600;
        border-radius: 8px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    }
    
    .stTextInput > div > div > input {
        background: #1a1f2e !important;
        border: 2px solid #2d3548 !important;
        border-radius: 8px;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
    }
    
    .dataframe {
        background: #1a1f2e !important;
        border: 1px solid #2d3548 !important;
        border-radius: 8px !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        padding: 1rem !important;
    }
    
    .dataframe td {
        color: #e2e8f0 !important;
        background: #1a1f2e !important;
        border-bottom: 1px solid #2d3548 !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    h1, h2, h3 {
        color: #ffffff;
    }
    
    p {
        color: #cbd5e1;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_trained_model():
    """Load the ML model"""
    try:
        clf = joblib.load('model_multilang/classifier.pkl')
        feat_names = joblib.load('model_multilang/features.pkl')
        meta = joblib.load('model_multilang/metadata.pkl')
        return clf, feat_names, meta
    except:
        return None, None, None


def analyze_code_file(file_path, clf, feat_names):
    """Analyze a single code file"""
    try:
        analyzer = MultiLanguageAnalyzer(file_path)
        
        if analyzer.language == 'unknown':
            return None
        
        feats = analyzer.extract_all_features()
        df = pd.DataFrame([feats])
        df = df[feat_names]
        
        pred = clf.predict(df)[0]
        proba = clf.predict_proba(df)[0]
        conf = max(proba) * 100
        
        return {
            'file': os.path.basename(file_path),
            'language': analyzer.language,
            'prediction': pred,
            'confidence': conf,
            'features': feats
        }
    except:
        return None


def fetch_github_files(repo_url):
    """Download files from a GitHub repo"""
    try:
        import requests
    except ImportError:
        st.error("Need to install requests: pip install requests")
        return None, None, []
    
    import re
    
    # Parse the URL
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, repo_url)
    
    if not match:
        return None, None, []
    
    owner, repo = match.groups()
    repo = repo.replace('.git', '').rstrip('/')
    
    temp_folder = tempfile.mkdtemp()
    api_base = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    try:
        resp = requests.get(api_base, timeout=10)
        if resp.status_code != 200:
            return owner, repo, []
    except:
        return owner, repo, []
    
    files_found = []
    valid_exts = ['.py', '.java', '.cpp', '.cc', '.cxx', '.c', '.h', '.hpp']
    
    def scan_dir(path=''):
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return
            
            for item in r.json():
                if item['type'] == 'file':
                    ext = Path(item['name']).suffix.lower()
                    if ext in valid_exts:
                        files_found.append({
                            'name': item['name'],
                            'url': item['download_url']
                        })
                elif item['type'] == 'dir' and not item['name'].startswith('.'):
                    if path.count('/') < 3:  # Don't go too deep
                        scan_dir(item['path'])
        except:
            pass
    
    scan_dir()
    
    # Download the files
    downloaded = []
    for f in files_found[:50]:  # Limit to 50 files
        try:
            r = requests.get(f['url'], timeout=10)
            if r.status_code == 200:
                fpath = os.path.join(temp_folder, f['name'])
                
                # Handle duplicates
                counter = 1
                while os.path.exists(fpath):
                    name, ext = os.path.splitext(f['name'])
                    fpath = os.path.join(temp_folder, f"{name}_{counter}{ext}")
                    counter += 1
                
                with open(fpath, 'w', encoding='utf-8') as file:
                    file.write(r.text)
                
                downloaded.append(fpath)
        except:
            pass
    
    return owner, repo, downloaded


def make_gauge_chart(score):
    """Create a gauge chart for quality score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Quality Score", 'font': {'size': 18, 'color': '#e2e8f0'}},
        number={'font': {'size': 48, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#6366f1"},
            'bgcolor': "#1a1f2e",
            'borderwidth': 2,
            'bordercolor': "#2d3548",
            'steps': [
                {'range': [0, 40], 'color': '#2d1a1a'},
                {'range': [40, 70], 'color': '#2d2a1a'},
                {'range': [70, 100], 'color': '#1a2d1a'}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=320,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def make_language_pie(results):
    """Create pie chart showing language distribution"""
    lang_counts = {}
    for r in results:
        lang = r['language'].upper()
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    
    fig = px.pie(
        values=list(lang_counts.values()),
        names=list(lang_counts.keys()),
        title="Languages",
        color_discrete_sequence=['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b'],
        hole=0.4
    )
    
    fig.update_traces(textfont={'size': 13, 'color': 'white'})
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=320,
        font={'color': '#e2e8f0'}
    )
    
    return fig


def make_quality_bars(results):
    """Create bar chart for quality distribution"""
    good = sum(1 for r in results if r['prediction'] == 1)
    bad = len(results) - good
    
    fig = go.Figure(data=[
        go.Bar(
            x=['Good', 'Needs Work'],
            y=[good, bad],
            marker=dict(color=['#6366f1', '#ec4899']),
            text=[good, bad],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Quality",
        paper_bgcolor='rgba(0,0,0,0)',
        height=320,
        xaxis=dict(showgrid=False, color='#9ca3af'),
        yaxis=dict(gridcolor='#2d3548', color='#9ca3af'),
        font={'color': '#e2e8f0'}
    )
    
    return fig


# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #ffffff; text-align: center;'>Menu</h2>", unsafe_allow_html=True)
    
    page = st.radio("", ["Home", "Analyze GitHub Repo", "Analyze File", "Model Info"], label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: #2d3548; margin: 2rem 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #ffffff;'>Status</h3>", unsafe_allow_html=True)
    
    model, features, metadata = load_trained_model()
    
    if model is None:
        st.error("Model not loaded")
        st.stop()
    else:
        st.success("Model loaded")
        if metadata:
            st.markdown(f"<p style='color: #cbd5e1;'>Accuracy: <strong>{metadata['test_accuracy']*100:.1f}%</strong></p>", unsafe_allow_html=True)


# Main pages
if page == "Home":
    st.markdown('<h1 class="main-title">Code Quality Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">ML-based analysis for Python, Java, C++, and C</p>', unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", "98.33%", "+8.33%")
    with col2:
        st.metric("Languages", "4")
    with col3:
        st.metric("Samples", "600")
    with col4:
        st.metric("Features", "19")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Info cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='info-card'>
                <h3>Analysis Features</h3>
                <p>Uses Random Forest with 19 code quality features</p>
                <ul>
                    <li>Code complexity</li>
                    <li>Documentation</li>
                    <li>Code smells</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='info-card'>
                <h3>Languages</h3>
                <p>Supports multiple programming languages</p>
                <ul>
                    <li>Python (.py)</li>
                    <li>Java (.java)</li>
                    <li>C++ (.cpp)</li>
                    <li>C (.c)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='info-card'>
                <h3>Model</h3>
                <p>Trained on 600 code samples</p>
                <ul>
                    <li>98.33% accuracy</li>
                    <li>Cross-validated</li>
                    <li>GitHub integration</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)


elif page == "Analyze GitHub Repo":
    st.markdown('<h1 class="main-title">GitHub Repository Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analyze code quality of entire repositories</p>', unsafe_allow_html=True)
    
    repo_url = st.text_input("Repository URL", placeholder="https://github.com/username/repository")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
    
    if analyze_btn and repo_url:
        with st.spinner("Downloading files..."):
            owner, repo, files = fetch_github_files(repo_url)
        
        if not files:
            st.error("Couldn't get files from that repo")
            st.stop()
        
        st.success(f"Got {len(files)} files from {owner}/{repo}")
        
        # Analyze all files
        with st.spinner("Analyzing..."):
            results = []
            pbar = st.progress(0)
            
            for i, fpath in enumerate(files):
                result = analyze_code_file(fpath, model, features)
                if result:
                    results.append(result)
                pbar.progress((i + 1) / len(files))
                time.sleep(0.02)
        
        if not results:
            st.error("No code files found")
            st.stop()
        
        # Calculate stats
        good = sum(1 for r in results if r['prediction'] == 1)
        bad = len(results) - good
        score = (good / len(results)) * 100
        avg_conf = sum(r['confidence'] for r in results) / len(results)
        
        st.markdown("## Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Score", f"{score:.1f}%")
        with col2:
            st.metric("Files", len(results))
        with col3:
            st.metric("Good", f"{good}")
        with col4:
            st.metric("Confidence", f"{avg_conf:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_gauge_chart(score), use_container_width=True)
        with col2:
            st.plotly_chart(make_language_pie(results), use_container_width=True)
        
        st.plotly_chart(make_quality_bars(results), use_container_width=True)
        
        # Results table
        st.markdown("### Files")
        
        df = pd.DataFrame([{
            'File': r['file'],
            'Language': r['language'].upper(),
            'Quality': 'Good' if r['prediction'] == 1 else 'Needs Work',
            'Confidence': f"{r['confidence']:.1f}%"
        } for r in results])
        
        st.dataframe(df, use_container_width=True, height=400)
        
        # Suggestions
        st.markdown("### Suggestions")
        
        low_comments = sum(1 for r in results if r['features']['comment_ratio'] < 0.05)
        no_docs = sum(1 for r in results if not r['features']['has_docstrings'])
        long_funcs = sum(1 for r in results if r['features']['very_long_functions'] > 0)
        
        if low_comments > len(results) * 0.3:
            st.warning(f"{low_comments} files need more comments")
        
        if no_docs > len(results) * 0.3:
            st.warning(f"{no_docs} files missing documentation")
        
        if long_funcs > 0:
            st.warning(f"{long_funcs} files have long functions")
        
        if low_comments + no_docs + long_funcs == 0:
            st.success("Code looks good!")


elif page == "Analyze File":
    st.markdown('<h1 class="main-title">File Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload a code file for analysis</p>', unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Choose file", type=['py', 'java', 'cpp', 'c', 'cc', 'h'])
    
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
            tmp.write(uploaded.getvalue())
            tmp_path = tmp.name
        
        with st.spinner("Analyzing..."):
            result = analyze_code_file(tmp_path, model, features)
            time.sleep(0.2)
        
        if result:
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                quality = "Good" if result['prediction'] == 1 else "Needs Work"
                st.metric("Quality", quality)
            with col2:
                st.metric("Confidence", f"{result['confidence']:.1f}%")
            with col3:
                st.metric("Language", result['language'].upper())
            
            st.markdown("### Metrics")
            
            f = result['features']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Structure**")
                m1, m2 = st.columns(2)
                with m1:
                    st.metric("Lines", f['total_lines'])
                    st.metric("Functions", f['num_functions'])
                with m2:
                    st.metric("Classes", f['num_classes'])
                    st.metric("Nesting", f['max_indentation'])
            
            with col2:
                st.markdown("**Quality**")
                m1, m2 = st.columns(2)
                with m1:
                    st.metric("Comments", f"{f['comment_ratio']*100:.1f}%")
                    st.metric("Docs", "Yes" if f['has_docstrings'] else "No")
                with m2:
                    st.metric("Magic nums", f['magic_numbers'])
                    st.metric("Long funcs", f['very_long_functions'])
        
        os.unlink(tmp_path)


elif page == "Model Info":
    st.markdown('<h1 class="main-title">Model Information</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Details about the ML model</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='info-card'>
                <h3>Model Details</h3>
                <p><strong>Algorithm:</strong> Random Forest</p>
                <p><strong>Trees:</strong> 100</p>
                <p><strong>Max Depth:</strong> 15</p>
                <p><strong>Features:</strong> 19</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if metadata:
            st.markdown(f"""
                <div class='info-card'>
                    <h3>Performance</h3>
                    <p><strong>Test Accuracy:</strong> {metadata['test_accuracy']*100:.2f}%</p>
                    <p><strong>Cross-Val:</strong> {metadata['cv_mean']*100:.2f}%</p>
                    <p><strong>Samples:</strong> {metadata['n_samples']}</p>
                </div>
            """, unsafe_allow_html=True)


st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 2rem 0; margin-top: 3rem; border-top: 1px solid #2d3548;'>
        Code Quality Analyzer | ML Project
    </div>
""", unsafe_allow_html=True)
