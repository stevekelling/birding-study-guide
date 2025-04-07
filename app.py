# Birding Study Guide App - Multi-Region Version for Pre-Cleaned Data
# ✅ Assumes pre-cleaned ABA checklist and multiple regional datasets
# ✅ Dynamic in-app table view with region selection
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

    # Load data
    aba_df = load_aba('ABA_Checklist.csv')
    region_df = load_region_data(regions[selected_region])

    if st.button("Generate Study Guide"):
        study_guide_df = generate_study_guide(aba_df, region_df, selected_region)
        st.success(f"Study guide for {selected_region} generated!")

        # Display dynamic table
        st.subheader(f"Your Regional Study Guide: {selected_region}")
        st.dataframe(study_guide_df, use_container_width=True)

        # Optional: Download button
        csv = study_guide_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Study Guide as CSV",
            data=csv,
            file_name=f'Birding_Study_Guide_{selected_region.replace(" ", "_")}.csv',
            mime='text/csv'
        )

# Run the app
if __name__ == '__main__':
    main()
