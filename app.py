
# Birding Study Guide App - Streamlit Version for Deployment
# ✅ Preloaded Washington dataset and ABA checklist
# ✅ Dynamic in-app table view
# ✅ Optional CSV export for power users

import streamlit as st
import pandas as pd

# --- Load and clean ABA checklist ---
def load_clean_aba(filepath):
    aba_clean = pd.read_csv(filepath)
    return aba_clean

# --- Load and clean Washington eBird data ---
def load_clean_region_data(filepath):
    ebird_raw = pd.read_csv(filepath, skiprows=16, header=None)
    num_columns = ebird_raw.shape[1]
    column_names = ['Common Name'] + [f'Freq_{i}' for i in range(1, num_columns)]
    ebird_raw.columns = column_names

    freq_columns = [col for col in ebird_raw.columns if col.startswith('Freq_')]
    for col in freq_columns:
        ebird_raw[col] = ebird_raw[col].astype(str).str.replace('%', '').astype(float)

    ebird_raw['Mean_Frequency'] = ebird_raw[freq_columns].mean(axis=1)

    def frequency_to_status(freq):
        if freq > 10:
            return 'Common'
        elif freq > 3:
            return 'Fairly Common'
        elif freq > 1:
            return 'Uncommon'
        elif freq > 0.1:
            return 'Rare'
        elif freq > 0:
            return 'Accidental'
        else:
            return 'Absent'

    ebird_raw['PNW'] = ebird_raw['Mean_Frequency'].apply(frequency_to_status)

    return ebird_raw[['Common Name', 'PNW']]

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
    st.markdown("Prepare for your next birding adventure with a custom study guide! \n \n This prototype uses preloaded data for Washington State.")

    # Load data
    aba_df = load_clean_aba('ABA_Checklist.csv')
    region_df = load_clean_region_data('Washington.csv')

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
