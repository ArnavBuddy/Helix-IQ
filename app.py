import streamlit as st
import pandas as pd
from src.data_sources.linkedin import LinkedInSource
from src.data_sources.pubmed import PubMedSource
from src.enrichment.geo import enrich_location_data
from src.enrichment.contact import enrich_contact_info
from src.ranking.scorer import LeadScorer
import pydeck as pdk

# Page Config
# Page Config
st.set_page_config(page_title="AI Lead Gen Agent", page_icon="🧬", layout="wide")

# --- CUSTOM CSS & THEME SETUP ---
def setup_custom_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global Background & Font */
        .stApp {
            background-color: #0B0E13;
            color: #E2E8F0;
            font-family: 'Inter', sans-serif;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0F1218; 
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            color: #F8FAFC !important;
            font-weight: 600;
        }
        p {
            color: #94A3B8;
            font-family: 'Inter', sans-serif;
        }
        
        /* Custom Metric Card */
        .metric-card {
            background: linear-gradient(145deg, #11151D 0%, #0F1218 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.15);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .metric-card:hover {
            border-color: rgba(60, 113, 221, 0.4);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
        }
        .metric-title {
            color: #94A3B8;
            font-size: 13px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }
        .metric-value {
            color: #F8FAFC;
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        .metric-desc {
            color: #64748B;
            font-size: 12px;
            margin-top: 6px;
        }
        
        /* DataFrame/Table styling enhancements */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            background-color: #11151D;
            padding: 4px;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #3C71DD;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.2s;
        }
        .stButton button:hover {
            background-color: #2D5Bbf;
            border: none;
            box-shadow: 0 4px 12px rgba(60, 113, 221, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

setup_custom_theme()

# --- HELPER COMPONENTS ---
def display_metric_card(col, title, value, description=None):
    with col:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
                {'<div class="metric-desc">' + description + '</div>' if description else ''}
            </div>
        """, unsafe_allow_html=True)

# Title and Breadcrumbs styled header
st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 24px; font-weight: 600; margin-bottom: 5px;">🧬 Lead Generation Intelligence</h1>
        <p style="font-size: 14px; margin-top: 0;">Identify, enrich, and rank high-probability leads for 3D in-vitro model therapies.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("Filter Controls")
source_type = st.sidebar.multiselect(
    "Data Sources", 
    ["LinkedIn", "PubMed"], 
    default=["LinkedIn", "PubMed"]
)
st.sidebar.markdown("---")
num_leads = st.sidebar.slider("Leads to Fetch", 10, 100, 50)
min_score = st.sidebar.slider("Min Propensity Score", 0, 100, 50)
location_filter = st.sidebar.text_input("Location Filter (e.g., Boston)")

# Run Agent Button (Styled)
if st.sidebar.button("🚀 Run Lead Gen Agent", type="primary"):
    with st.spinner("Gathering intelligence..."):
        all_leads = []
        
        # 1. Identification
        if "LinkedIn" in source_type:
            li_source = LinkedInSource()
            leads = li_source.fetch_data(limit=num_leads//2 if "PubMed" in source_type else num_leads)
            all_leads.extend(leads)
            
        if "PubMed" in source_type:
            pm_source = PubMedSource()
            leads = pm_source.fetch_data(limit=num_leads//2 if "LinkedIn" in source_type else num_leads)
            all_leads.extend(leads)
            
        # 2. Enrichment & 3. Ranking
        scorer = LeadScorer()
        processed_leads = []
        
        for lead in all_leads:
            # Enrichment
            lead = enrich_location_data(lead)
            lead = enrich_contact_info(lead)
            
            # Ranking
            lead = scorer.score_profile(lead)
            
            processed_leads.append(lead)
            
        # Create DataFrame
        df = pd.DataFrame(processed_leads)
        
        # Filtering
        if location_filter:
            df = df[df['location'].str.contains(location_filter, case=False, na=False)]
            
        df = df[df['score'] >= min_score]
        
        # Sort by Score
        df = df.sort_values(by="score", ascending=False)
        
        # --- DASHBOARD METRICS ---
        st.markdown("### Key Performance Indicators")
        m_col1, m_col2, m_col3 = st.columns(3)
        
        total_found = len(all_leads)
        qualified_count = len(df)
        avg_score = df['score'].mean() if not df.empty else 0
        
        display_metric_card(m_col1, "Total Leads Found", f"{total_found}", "Raw leads gathered from sources")
        display_metric_card(m_col2, "Qualified Opportunities", f"{qualified_count}", f"> {min_score} Propensity Score")
        display_metric_card(m_col3, "Avg. Propensity Score", f"{avg_score:.1f}", "Overall lead quality index")
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

        # --- MAIN TABLE ---
        st.markdown("### 🎯 Qualified Targets")
        
        # Configure columns for display
        display_cols = [
            "score", "name", "title", "company", "location_details", "email", "score_reasons", "source"
        ]
        
        st.dataframe(
            df[display_cols].style.background_gradient(subset=['score'], cmap='Greens'),
            column_config={
                "score": st.column_config.ProgressColumn(
                    "Score",
                    help="Probability of buying (0-100)",
                    format="%d",
                    min_value=0,
                    max_value=100,
                ),
                "linkedin_url": st.column_config.LinkColumn("Profile"),
                "email": st.column_config.LinkColumn("Email")
            },
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        # --- VISUALIZATION ---
        st.markdown("### 🌍 Location Intelligence")
        col_map, col_stat = st.columns([2, 1])
        
        with col_stat:
            remote_count = df['is_remote'].sum()
            hq_count = len(df) - remote_count
            
            # Using custom card for stats too, or just simple text
            st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 10px;">
                    <div class="metric-title">Remote / Field</div>
                    <div class="metric-value">{remote_count}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">HQ / Office</div>
                    <div class="metric-value">{hq_count}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if not df.empty:
               st.markdown("#### Top Hubs")
               st.bar_chart(df['company_hq'].value_counts().head(5), color="#3C71DD") # Using one of the theme colors

        with col_map:
             if not df.empty:
                # Placeholder for map
                # Filter valid coordinates
                map_data = df.dropna(subset=['lat', 'lon'])
                
                if not map_data.empty:
                    # Calculate view state
                    mid_lat = map_data['lat'].mean()
                    mid_lon = map_data['lon'].mean()
                    
                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=map_data,
                        get_position='[lon, lat]',
                        get_color='[60, 113, 221, 160]', # #3C71DD with alpha
                        get_radius=20000, # 20km radius
                        pickable=True,
                        auto_highlight=True,
                    )
                    
                    view_state = pdk.ViewState(
                        latitude=mid_lat,
                        longitude=mid_lon,
                        zoom=3,
                        pitch=0,
                    )
                    
                    st.pydeck_chart(pdk.Deck(
                        map_style='mapbox://styles/mapbox/dark-v10', # Dark style, careful with token requirements in real apps, Streamlit handles some defaults
                        initial_view_state=view_state,
                        layers=[layer],
                        tooltip={"text": "{name}\n{company}\n{location}"}
                    ))
                else:
                    st.info("No location data available for map.")
            
else:
    # Empty State with style
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; background-color: #11151D; border-radius: 8px; border: 1px dashed rgba(255,255,255,0.1); margin-top: 50px;">
            <div style="font-size: 40px; margin-bottom: 20px;">👈</div>
            <h3 style="color: #F0F2F4;">Ready to Scout</h3>
            <p style="color: #818898;">Adjust filters in the sidebar and click 'Run Lead Gen Agent' to start.</p>
        </div>
    """, unsafe_allow_html=True)
