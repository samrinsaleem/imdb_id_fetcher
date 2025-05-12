import streamlit as st
import pandas as pd
import os
from imdb_scraper import get_top_imdb_matches

# App Title
st.title("IMDb ID Finder for Movies & TV Shows 🎬")

# Upload file section
uploaded_file = st.file_uploader("Upload a CSV or Excel file. Must contain the following column(s): Title. May contain additional column(s) such as: Year, Rating, ID (non-IMDb).", type=["csv", "xlsx"])

if uploaded_file:
    # Read file into a DataFrame
    file_ext = os.path.splitext(uploaded_file.name)[1]
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Check if the required column exists
    if "Title" not in df.columns:
        st.error("The file must contain a 'Title' column.")
    else:
        st.write("Preview of uploaded file:")
        st.dataframe(df.head())

        year_available = "Year" in df.columns

        # Process IMDb IDs
        imdb_ids = []
        manual_mode = st.checkbox("Enable manual review for uncertain matches (slower)", value=True)
        progress_bar = st.progress(0)

        for i, row in df.iterrows():
            title = row["Title"]
            year = row["Year"] if year_available else None
            matches = get_top_imdb_matches(title, year)

            if not matches:
                imdb_ids.append(None)
            elif manual_mode and len(matches) > 1:
                choice = st.selectbox(f"Select IMDb match for: {title}", options=matches, format_func=lambda x: x[0], key=i)
                imdb_ids.append(choice[1])
            else:
                imdb_ids.append(matches[0][1])  # auto-pick top match

            progress_bar.progress((i + 1) / len(df))

        # Add IMDb IDs to DataFrame
        df["IMDb ID"] = imdb_ids

        missing = df["IMDb ID"].isna().sum()
        if missing:
            st.warning(f"{missing} titles could not be matched on IMDb.")

        # Display the updated table
        st.write("Updated Data:")
        st.dataframe(df)

        # File download section
        base_filename = os.path.splitext(uploaded_file.name)[0]
        output_filename = f"{base_filename}_with_imdb_id.xlsx"
        df.to_excel(output_filename, index=False)

        with open(output_filename, "rb") as f:
            st.download_button(
                label="Download Updated File",
                data=f,
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Cleanup temporary file
        os.remove(output_filename)