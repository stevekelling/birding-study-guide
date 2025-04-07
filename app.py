# Birding Study Guide App - Multi-Region Version with Fixed Session State
# ✅ Pre-cleaned ABA checklist and multiple regional datasets
# ✅ Dynamic in-app table view with region selection
# ✅ Persistent sidebar filters
# ✅ Optional CSV export for power users

import streamlit as st
import pandas as pd

# --- Load ABA checklist (already clean) ---
def load_aba(filepath):
    return pd.read_csv(filepath)

# --- Load region data (already clean) ---
def load_region_data(filepath):
    return pd.read_csv(filepath)

# --- Generate Study Guide ---
def generate_study_guide(aba_df, region_df, region_name):
    final_df = aba_df.merge(region_df, on='Common Name', how='left')
    final_df[region_name] = final_df['Status'].fillna('Absent')
    final_df.drop(columns=['Status'], inplace=True)

    # Add placeholders for other regions (optional)
    all_regions = ['PNW', 'Arizona', 'Northern California', 'British Columbia', 'Idaho', 'California', 'Oregon']
    for region in all_regions:
        if region != region_name and region not in final_df.columns:
            final_df[region] = 'Absent'

    final_df['Subregion Notes'] = f'Custom run for {region_name} region.'
    return final_df

# --- Main App ---
def main():
    st.set_page_config(page_title="Birding Study Guide Generator", layout="wide")

    st.title("🪶 Birding Study Guide Generator")
    st.markdown("Prepare for your next birding adventure with a custom study guide! \n \n Select your target region to generate a tailored list.")

    # Region selection
    regions = {
        'Pacific Northwest (Washington)': 'Washington.csv',
        'Oregon': 'Oregon.csv',
        'Idaho': 'Idaho.csv',
        'British Columbia': 'British Columbia.csv',
        'California': 'California.csv',
        'Arizona': 'Arizona.csv'
    }

    selected_region = st.selectbox("Select your region:", list(regions.keys()))

    # --- Filter section (always visible) ---
    st.sidebar.header("Filter your study guide")
    status_options = ['Common', 'Fairly Common', 'Uncommon', 'Rare', 'Accidental', 'Absent']
    selected_status = st.sidebar.multiselect(
        "Select statuses to include:",
        options=status_options,
        default=['Common', 'Fairly Common', 'Uncommon', 'Rare']
    )

    # Load data
    aba_df = load_aba('ABA_Checklist.csv')
    region_df = load_region_data(regions[selected_region])

    # Use region-specific session state key
    session_key = f"study_guide_df_{selected_region.replace(' ', '_')}"

    if st.button("Generate Study Guide") or session_key in st.session_state:
        if session_key not in st.session_state:
            st.session_state[session_key] = generate_study_guide(aba_df, region_df, selected_region)

        # Apply filter
        filtered_df = st.session_state[session_key][st.session_state[session_key][selected_region].isin(selected_status)]

        st.success(f"Study guide for {selected_region} generated!")

        # Display dynamic table
        st.subheader(f"Your Regional Study Guide: {selected_region}")
        st.dataframe(filtered_df, use_container_width=True)

        # Optional: Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Study Guide as CSV",
            data=csv,
            file_name=f'Birding_Study_Guide_{selected_region.replace(" ", "_")}.csv',
            mime='text/csv'
        )

# Run the app
if __name__ == '__main__':
    main()
