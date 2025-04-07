import streamlit as st
import pandas as pd

# Load your region mapping file
@st.cache_data
def load_region_mapping():
    return pd.read_csv('region_mapping.csv', quotechar='"')

# Load your place mapping file
@st.cache_data
def load_place_mapping():
    return pd.read_csv('place_mapping.csv', quotechar='"')

region_df = load_region_mapping()
place_df = load_place_mapping()

st.title("Birding Study Guide — Region Selector")

st.markdown("### Use the helper below to start with a familiar place, or manually filter regions.")

# Build place lookup dictionary
place_options = ["(Skip)"] + sorted(place_df['Place Name'].dropna().unique().tolist())
selected_place = st.selectbox("Where are you visiting? (Optional)", place_options)

# Initialize pre-selected filters
pre_selected_macros = []
pre_selected_states = []
pre_selected_display_regions = []

if selected_place != "(Skip)":
    selected_region_id = place_df.loc[place_df['Place Name'] == selected_place, 'Region ID'].values[0]
    
    # Use region_mapping.csv to get full region details
    region_details = region_df.loc[region_df['Region ID'] == selected_region_id].iloc[0]

    pre_selected_macros = [region_details['Macro Region']]
    pre_selected_states = [region_details['State/Province']]
    pre_selected_display_regions = [region_details['Region Display Name']]

    st.info(f"Auto-selected: **{region_details['Macro Region']}** → **{region_details['State/Province']}** → **{region_details['Region Display Name']}**")

# Dynamic multi-select filters

# Get full lists
all_macros = sorted(region_df['Macro Region'].dropna().unique().tolist())
all_states = sorted(region_df['State/Province'].dropna().unique().tolist())
all_display_regions = sorted(region_df['Region Display Name'].dropna().unique().tolist())

# Macro Region selection
selected_macros = st.multiselect("Select Macro Region(s) (Optional)", all_macros, default=pre_selected_macros)

# Filter states based on Macro Region
if selected_macros:
    filtered_states = sorted(region_df[region_df['Macro Region'].isin(selected_macros)]['State/Province'].dropna().unique().tolist())
else:
    filtered_states = all_states

selected_states = st.multiselect("Select State/Province(s) (Optional)", filtered_states, default=pre_selected_states)

# Filter display regions based on previous selections
display_filter = region_df.copy()

if selected_macros:
    display_filter = display_filter[display_filter['Macro Region'].isin(selected_macros)]
if selected_states:
    display_filter = display_filter[display_filter['State/Province'].isin(selected_states)]

filtered_display_regions = sorted(display_filter['Region Display Name'].dropna().unique().tolist())

selected_display_regions = st.multiselect("Select Display Region(s) (Optional)", filtered_display_regions, default=pre_selected_display_regions)

# Apply filters to main DataFrame
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

# Show results
st.markdown("### Filtered Regions")
st.dataframe(filtered_df)

st.success(f"{len(filtered_df)} regions matching your filters.")
