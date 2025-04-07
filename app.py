# Birding Study Guide App - Streamlined Version for Pre-Cleaned Data
# ✅ Assumes pre-cleaned ABA checklist and Washington regional dataset
# ✅ Dynamic in-app table view
# ✅ Optional CSV export for power users

import streamlit as st
import pandas as pd

# --- Load ABA checklist (already clean) ---
def load_aba(filepath):
    return pd.read_csv(filepath)

# --- Load Washington region data (already clean) ---
def load_region_data(filepath):
    return pd.read_csv(filepath)

# --- Generate Study Guide ---
def generate_study_guide(aba_df, region_df):
    final_df = aba_df.merge(region_df, on='Common Name', how='left')
    final_df['PNW'] = final_df['PNW'].fillna('Absent')
    final_df['Arizona'] = 'Absent'  # Placeholder
    final_df['Northern California'] = 'Absent'  # Placeholder
    final_df['Subregion Notes'] = 'Prototype run with Washington data only.'
    return final_df

# --- Main App ---
def main():
    st.set_page_config(page_title="Birding Study Guide Generator", layout="wide")

    st.title("🪶 Birding Study Guide Generator")
    st.markdown("Prepare for your next birding adventure with a custom study guide! \n \n This prototype uses preloaded, pre-cleaned data for Washington State.")

    # Load data
    aba_df = load_aba('ABA_Checklist.csv')
    region_df = load_region_data('Washington.csv')

    if st.button("Generate Study Guide"):
        study_guide_df = generate_study_guide(aba_df, region_df)
        st.success("Study guide generated!")

        # Display dynamic table
        st.subheader("Your Regional Study Guide")
        st.dataframe(study_guide_df, use_container_width=True)

        # Optional: Download button
        csv = study_guide_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Study Guide as CSV",
            data=csv,
            file_name='Birding_Study_Guide.csv',
            mime='text/csv'
        )

# Run the app
if __name__ == '__main__':
    main()
