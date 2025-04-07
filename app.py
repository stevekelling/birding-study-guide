import streamlit as st
import pandas as pd

# Load your region mapping file
@st.cache_data
def load_region_mapping():
    return pd.read_csv('region_mapping.csv', quotechar='"')

region_df = load_region_mapping()

st.title("Birding Study Guide — Region Selector")

st.markdown("### Filter regions independently by Macro Region, State/Province, or Region Name.\nFilters adjust dynamically for a cleaner experience.")

# Get initial full lists
all_macros = sorted(region_df['Macro Region'].dropna().unique().tolist())
all_states = sorted(region_df['State/Province'].dropna().unique().tolist())
all_display_regions = sorted(region_df['Region Display Name'].dropna().unique().tolist())

# Macro Region selection
selected_macros = st.multiselect("Select Macro Region(s) (Optional)", all_macros)

# Dynamically filter states based on selected macro regions
if selected_macros:
    filtered_states = sorted(region_df[region_df['Macro Region'].isin(selected_macros)]['State/Province'].dropna().unique().tolist())
else:
    filtered_states = all_states

selected_states = st.multiselect("Select State/Province(s) (Optional)", filtered_states)

# Dynamically filter display regions based on selected macro regions and states
display_filter = region_df.copy()

if selected_macros:
    display_filter = display_filter[display_filter['Macro Region'].isin(selected_macros)]
if selected_states:
    display_filter = display_filter[display_filter['State/Province'].isin(selected_states)]

filtered_display_regions = sorted(display_filter['Region Display Name'].dropna().unique().tolist())

selected_display_regions = st.multiselect("Select Display Region(s) (Optional)", filtered_display_regions)

# Apply filters to the main DataFrame
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
