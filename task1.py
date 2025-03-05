import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Custom styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: white;
    }
    .stButton > button {
        background-color: #ff6f61;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description with emojis
st.title("🚀 Datasweeper Sterling Integrator By Jaweria")
st.write("✨ Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3! 📊")

# File uploader
uploaded_files = st.file_uploader("📂 Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File preview
        st.subheader(f"📜 Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"✅ Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✔️ Duplicates removed!")

            with col2:
                if st.button(f"🩹 Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✔️ Missing values have been filled")

            # Select columns to keep
            st.subheader("📌 Select Columns To Keep")
            columns = st.multiselect(f"🎯 Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"🔁 Convert {file.name} to:", ["CSV", "EXCEL"], key=file.name)

        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "EXCEL":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    st.success("🎉 All files processed successfully!")