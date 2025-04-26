import streamlit as st
import pandas as pd
from file_uploading.file_uploader import FileUploader
from file_preprocessing.file_processor import FileProcessor
from data_extraction.data_extractor import DataExtractor
from eda.eda import EDA
from summary_generation.summary_generator import SummaryGenerator
from summary_generation.llm import GoogleGenerativeLLM
import tempfile
from config import get_settings

# Streamlit app configuration
st.set_page_config(page_title="Ticket Analyzer", layout="wide")
st.sidebar.title("Ticket Data Summarizer")
page = st.sidebar.radio(" ", ("Upload", "Preview Raw Data", "Preview Processed Data", "Storytelling", "EDA Analysis"))


# Global state
if "raw_df" not in st.session_state:
    st.session_state.raw_df = None
if "processed_df" not in st.session_state:
    st.session_state.processed_df = None


# Instantiate classes
file_handler = FileUploader()
file_processor = FileProcessor()


# Load settings
REQUIRED_COLUMNS = [
    'ORDER_NUMBER', 'SERVICE_CATEGORY', 'ACCEPTANCE_TIME', 'COMPLETION_TIME',
    'ORDER_DESCRIPTION_1', 'ORDER_DESCRIPTION_2', 'ORDER_DESCRIPTION_3_MAXIMUM',
    'NOTE_MAXIMUM', 'CAUSE', 'COMPLETION_NOTE_MAXIMUM', 'CUSTOMER_NUMBER'
]
VALID_CATEGORIES = ['HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']
CATEGORY_PRODUCT_MAPPER = {
    'KAI': 'Broadband',
    'NET': 'Broadband',
    'KAV': 'Voice',
    'KAD': 'TV',
    'GIGA': 'GIGA',
    'VOD': 'VOD',
    'HDW': 'Hardware'
}


# Upload Page
if page == "Upload":
    st.subheader("📁 Upload Ticket File")
    uploaded_file = st.file_uploader("Upload a .csv or .txt file", type=['csv', 'txt'])
    if uploaded_file is not None:
        file_handler.upload_file(uploaded_file)
        if not file_handler.is_valid_format():
            st.error("Invalid file format. Please upload a .csv or .txt file.")
        else:
            try:
                if file_handler.extension == "txt":
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_csv:
                        df = file_handler.convert_txt_to_csv(tmp_csv.name)
                        st.success("Text file successfully converted to CSV.")
                else:
                    df = file_handler.load_csv()
                    st.success("CSV file successfully loaded.")

                st.session_state.raw_df = df

                # Column validation
                try:
                    if file_processor.validate_required_columns(df, REQUIRED_COLUMNS):
                        st.success("All required columns are present.")
                        st.session_state.processed_df = file_processor.process_file(st.session_state.raw_df, CATEGORY_PRODUCT_MAPPER, VALID_CATEGORIES)
                        st.success("File processed successfully.")
                except ValueError as ve:
                    st.error(str(ve))

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Preview Raw Data Page
elif page == "Preview Raw Data":
    st.subheader("Preview Raw Data")
    if st.session_state.raw_df is not None:
        st.dataframe(st.session_state.raw_df.head(100))
    else:
        st.warning("No file uploaded yet. Go to the Upload page first.")

# Preview Processed Data Page
elif page == "Preview Processed Data":
    st.subheader("Preview Filtered Data")
    if st.session_state.processed_df is not None:
        st.dataframe(st.session_state.processed_df.head(100))
    else:
        st.warning("No processed data available. Please upload and validate a file first.")

# Storytelling Page (placeholder)
elif page == "Storytelling":
    st.subheader("📖 Storytelling Summary")

    if st.session_state.processed_df is None:
        st.warning("Please upload and process data first.")
    else:

        # Load data
        categories = st.session_state.processed_df["SERVICE_CATEGORY"].unique().tolist()
        category_product_display = [
            f"{cat} - {CATEGORY_PRODUCT_MAPPER.get(cat, 'Unknown')}" for cat in categories
        ]

        selected_display = st.selectbox("Select a Category", category_product_display)
        selected_category = selected_display.split(" - ")[0]


        extractor = DataExtractor(st.session_state.processed_df)
        category_df = extractor.extract_for_category(selected_category, REQUIRED_COLUMNS)

        # Initialize session_state if not exists
        if "generated_summary" not in st.session_state:
            st.session_state.generated_summary = None
            st.session_state.generated_timestamp = None
        
        st.write(f"\n")
        # Generate summary
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                llm = GoogleGenerativeLLM()
                generator = SummaryGenerator(llm)
                data_dicts = category_df.to_dict(orient="records")
                summary, timestamp = generator.generate_summary(selected_category, data_dicts)

                # Save generated summary and timestamp to session state
                st.session_state.generated_summary = summary
                st.session_state.generated_timestamp = timestamp

        # Display saved summary (even after rerun)
        if st.session_state.generated_summary:
            st.write(f"\n\n")
            st.success(f"#### 📖 Storytelling Summary for {selected_category}")
            st.write(f"")
            st.write(st.session_state.generated_summary)

# Example usage in your Streamlit main app
elif page == "EDA Analysis":
    st.subheader("📊 Exploratory Data Analysis")

    if st.session_state.processed_df is not None:
        eda = EDA(st.session_state.processed_df)

        st.write("\n\n")
        st.divider()
        eda.show_summary_cards()
        st.divider()

        eda.plot_service_category_distribution()
        st.write("\n\n")
        st.divider()
        st.write("\n\n")
        # eda.plot_product_distribution()
        eda.plot_top_issue_causes()
        st.write("\n\n")

    else:
        st.warning("No processed data available. Please upload and process a file first.")
