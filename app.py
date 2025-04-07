import streamlit as st
import pandas as pd

# Load your region mapping file
@st.cache_data
def load_region_mapping():
    return pd.read_csv('region_mapping.csv', quotechar='"')

region_df = load_region_mapping()

st.title("Birding Study Guide — Region Selector")

st.markdown("### Filter regions independently by Macro Region, State/Province, or Region Name.")

# Get unique values for selectors
macro_regions = sorted(region_df['Macro Region'].dropna().unique().tolist())
states = sorted(region_df['State/Province'].dropna().unique().tolist())
display_regions = sorted(region_df['Region Display Name'].dropna().unique().tolist())

# Build multi-selectors
selected_macros = st.multiselect("Select Macro Region(s) (Optional)", macro_regions)
selected_states = st.multiselect("Select State/Province(s) (Optional)", states)
selected_display_regions = st.multiselect("Select Display Region(s) (Optional)", display_regions)

# Apply filters independently
filtered_df = region_df.copy()

if selected_macros:
    filtered_df = filtered_df[filtered_df['Macro Region'].isin(selected_macros)]

if selected_states:
    filtered_df = filtered_df[filtered_df['State/Province'].isin(selected_states)]

if selected_display_regions:
    filtered_df = filtered_df[filtered_df['Region Display Name'].isin(selected_display_regions)]

# Sort for clean display
sort_columns = ["Macro Region", "State/Province", "Region Display Name", "County Name"]
filtered_df = filtered_df.sort_values(by=sort_columns).reset_index(drop=True)

# Show filtered results
st.markdown("### Filtered Regions")
st.dataframe(filtered_df)

st.success(f"{len(filtered_df)} regions matching your filters.")
