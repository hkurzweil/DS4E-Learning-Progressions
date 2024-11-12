import streamlit as st
import pandas as pd

# Read multiple tabs
sheet_id = "1bnCPKr9nhmWNNq0a8STCY-_bOx9rnu7_CfrPP0LEQ7k"

# Create a dictionary to store DataFrames from each tab
dfs = {}

tabs = {
    'Strand A': '0',  
    'Strand B': '1955303903',  
    'Strand C': '235592302',  
    'Strand D': '521956191',
    'Strand E': '223899173',
}

# Read each tab into the dictionary
for tab_name, gid in tabs.items():
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    dfs[tab_name] = pd.read_csv(url)

# Set page config
st.set_page_config(page_title="Data Science Learning Progression", layout="wide")

# Add tab selection to the interface
tab_selection = st.selectbox("Select Strand:", list(dfs.keys()))

# Use the selected DataFrame
df = dfs[tab_selection]

# Clean the data
df = df[df['👦 Grade-Level'].notna()]  # Remove NaN rows
df = df[df['👦 Grade-Level'] != '[Drop-down]']  # Remove dropdown placeholder

# Title
st.title("Data Science Learning Progression")

# Grade level filter
grade_options = ["All"] + sorted(df['👦 Grade-Level'].unique().tolist())
selected_grade = st.selectbox("Select Grade Level:", grade_options)

# Filter data based on selected grade
if selected_grade != "All":
    filtered_df = df[df['👦 Grade-Level'] == selected_grade]
else:
    filtered_df = df

# Get the correct concept column name based on the selected strand
if tab_selection == 'Strand A':
    concept_col = 'Concept Name'
elif tab_selection == 'Strand B':
    concept_col = 'Concept'
else:
    concept_col = 'Concept Names'

# Display progression by sub-strand and concept
for substrand in filtered_df['⤵️ Sub-Strand'].unique():
    st.markdown(f"## {substrand}")
    substrand_data = filtered_df[filtered_df['⤵️ Sub-Strand'] == substrand]
    
    for concept in substrand_data[concept_col].unique():
        if pd.notna(concept):  # Check if concept is not NaN
            st.markdown(f"### {concept}")
            concept_data = substrand_data[substrand_data[concept_col] == concept]
            
            for _, row in concept_data.iterrows():
                st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 5px 0; color: #000000;'>
                    <strong style='color: #1f77b4;'>{row['👦 Grade-Level']}</strong>: {row['✅ Students can...']}
                </div>
                """, unsafe_allow_html=True)

                # If there are things to avoid, display them
                if pd.notna(row['❌ What to avoid...']):
                    st.markdown(f"""
                    <div style='background-color: #ffe6e6; padding: 10px; border-radius: 5px; margin: 5px 0; color: #000000;'>
                        <strong style='color: #dc3545;'>What to avoid:</strong> {row['❌ What to avoid...']}
                    </div>
                    """, unsafe_allow_html=True)

# Add some styling
st.markdown("""
    <style>
    h2 {
        color: #1f77b4 !important;
        margin-top: 30px;
    }
    h3 {
        color: #2c3e50 !important;
        margin-top: 20px;
        font-size: 1.2em;
    }
    div[data-testid="stMarkdown"] {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Add additional information about the lenses if they exist
st.sidebar.markdown("## Learning Lenses")
lenses = {
    "Problem Cycles & Iteration": "🔄",
    "Questioning & Critique": "🔍",
    "Role of Technology": "👩‍💻",
    "Social & Cultural Implications": "🌎"
}

for lens, emoji in lenses.items():
    if f"Lens: {emoji} {lens}" in filtered_df.columns:
        lens_data = filtered_df[f"Lens: {emoji} {lens}"].value_counts()
        if not lens_data.empty:
            st.sidebar.markdown(f"### {emoji} {lens}")
            st.sidebar.write(lens_data)
