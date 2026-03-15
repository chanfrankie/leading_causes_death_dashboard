import streamlit as st
import pandas as pd
import plotly.express as px
import io
import requests
import zipfile

st.set_page_config(layout="wide", page_title="Canada Mortality Dashboard")

@st.cache_data
def get_statcan_data():
    url = "https://www150.statcan.gc.ca/n1/tbl/csv/13100394-eng.zip"
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_filename = [f for f in z.namelist() if f.endswith('.csv') and not f.endswith('_MetaData.csv')][0]
        with z.open(csv_filename) as f:
            # We use dtype=str for REF_DATE to prevent the 1970 error
            df = pd.read_csv(f, low_memory=False)
    return df

def clean_data(df):
    # Mapping based on your screenshot
    rename_map = {
        'REF_DATE': 'Year',
        'GEO': 'Region',
        'Age at time of death': 'AgeGroup',
        'Sex': 'Sex',
        'Leading causes of death (ICD-10)': 'Cause',
        'Characteristics': 'Metric',
        'VALUE': 'Value'
    }
    df = df.rename(columns=rename_map)

    # FIX FOR THE 1970 ISSUE:
    # If Year is '2000-01-01' or just '2000', we extract just the first 4 characters
    df['Year'] = df['Year'].astype(str).str[:4].astype(int)
    
    # Drop empty values
    df = df.dropna(subset=['Value'])
    
    # Remove summary rows (Total all ages / Total all causes)
    df = df[~df['Cause'].str.contains("Total, all causes", na=False, case=False)]
    df = df[~df['AgeGroup'].str.contains("Total, all ages", na=False, case=False)]
    
    # Clean up the Cause names (remove the [ICD-10] codes)
    df['Cause'] = df['Cause'].str.replace(r' \[[^\]]*\]', '', regex=True)
    
    return df

st.title("📊 Leading Causes of Death in Canada")

try:
    with st.spinner("Downloading and processing data..."):
        raw_df = get_statcan_data()
        df = clean_data(raw_df)

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Data")
    
    # 1. Geographic Filter
    region = st.sidebar.selectbox("Region", sorted(df['Region'].unique()), index=0)
    
    # 2. Metric Filter (CRITICAL FIX)
    # This prevents mixing Ranks, Percentages, and Counts
    metric = st.sidebar.selectbox("Measure", sorted(df['Metric'].unique()), index=1) # Default to 'Number of deaths'

    # 3. Demographic Filters
    year = st.sidebar.selectbox("Year", sorted(df['Year'].unique(), reverse=True))
    age = st.sidebar.selectbox("Age Group", sorted(df['AgeGroup'].unique()))
    sex = st.sidebar.selectbox("Sex", sorted(df['Sex'].unique()))

    # --- FILTERING LOGIC ---
    mask = (
        (df['Region'] == region) & 
        (df['Year'] == year) & 
        (df['AgeGroup'] == age) & 
        (df['Sex'] == sex) &
        (df['Metric'] == metric)
    )
    filtered = df[mask].sort_values("Value", ascending=False)

    # --- VISUALS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Top 10: {metric}")
        top_10 = filtered.head(10)
        if not top_10.empty:
            fig = px.bar(top_10, x='Value', y='Cause', orientation='h', 
                         color='Value', color_continuous_scale='Viridis',
                         labels={'Value': metric})
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data found for this selection.")

    with col2:
        st.subheader("Composition")
        if not top_10.empty:
            # We only show a pie chart if it makes sense (not for 'Rank')
            if "Rank" not in metric:
                fig_pie = px.pie(top_10, values='Value', names='Cause', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Pie chart not applicable for 'Rank' metric.")

    # --- TREND ---
    st.divider()
    st.subheader(f"Historical Trend: {metric}")
    selected_cause = st.selectbox("Select a specific cause to track:", sorted(df['Cause'].unique()))
    
    trend_data = df[
        (df['Region'] == region) & 
        (df['AgeGroup'] == age) & 
        (df['Sex'] == sex) & 
        (df['Metric'] == metric) &
        (df['Cause'] == selected_cause)
    ].sort_values("Year")
    
    if not trend_data.empty:
        fig_line = px.line(trend_data, x='Year', y='Value', markers=True,
                          labels={'Value': metric})
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Trend data not available for this specific cause.")

except Exception as e:
    st.error(f"Dashboard Error: {e}")