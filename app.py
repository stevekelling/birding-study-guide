# app.py

import streamlit as st
import pandas as pd

# ================================
# ✅ Config
# ================================

st.set_page_config(page_title="Birding Place Finder", layout="wide")

# ================================
# ✅ Load Data (cached for performance)
# ================================

@st.cache_data
def load_data():
    # Load enriched places file
    places = pd.read_csv("places_enriched.csv")

    # Load region mapping file
    region_mapping = pd.read_csv("region_mapping.csv")

    return places, region_mapping

places_df, region_mapping_df = load_data()

# ================================
# ✅ UI Header
# ================================

st.title("🦉 Birding Place Finder")
st.subheader("Search for birding places and explore their ecological regions")

# ================================
# ✅ User Input: Place Name with Autosuggest
# ================================

# Build list of unique place names for suggestions
place_names = places_df['Place'].dropna().unique().tolist()

selected_place = st.selectbox("Type or select a place:", options=sorted(place_names))

if selected_place:
    # ================================
    # ✅ Lookup place details
    # ================================

    place_row = places_df[places_df['Place'] == selected_place].iloc[0]

    st.markdown(f"### 📍 **{selected_place}**")
    st.write(f"- **State:** {place_row['State']}")
    st.write(f"- **County:** {place_row['County Name']}")
    st.write(f"- **Latitude / Longitude:** {place_row['Latitude']}, {place_row['Longitude']}")
    st.write(f"- **Region ID:** {place_row['Region ID']}")

    # ================================
    # ✅ Lookup region mapping details
    # ================================

    region_id = place_row['Region ID']
    region_row = region_mapping_df[region_mapping_df['Region ID'] == region_id]

    if not region_row.empty:
        region_info = region_row.iloc[0]
        st.markdown("### 🌎 **Region Details**")
        st.write(f"- **Region Name:** {region_info['Region Display Name']}")
        st.write(f"- **Macro Region:** {region_info['Macro Region']}")
        st.write(f"- **Country:** {region_info['Country']}")
        st.write(f"- **State / Province:** {region_info['State/Province']}")
        st.write(f"- **Notes:** {region_info.get('Notes / Description', '—')}")
        st.write(f"- **BCR Number(s):** {region_info.get('BCR Number(s)', '—')}")
        st.write(f"- **Flagship Species:** {region_info.get('Flagship Species', '—')}")
        st.write(f"- **Seasonality Focus:** {region_info.get('Seasonality Focus / Special Field Notes', '—')}")

    else:
        st.warning("⚠️ Region mapping details not found for this Region ID.")

    # ================================
    # ✅ Optional: Show raw data expander
    # ================================

    with st.expander("See raw place data"):
        st.dataframe(place_row.to_frame())

    with st.expander("See raw region mapping data"):
        if not region_row.empty:
            st.dataframe(region_row)
        else:
            st.write("No data available.")

# ================================
# ✅ Footer
# ================================

st.markdown("---")
st.markdown("Built for personalized birding study — powered by pre-enriched data 🦉")
