import streamlit as st
import os
from extractor import BillExtractor
from filler import ExcelFiller
import tempfile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(page_title="EnergyBae Solar Load Calculator", layout="centered")

# Custom CSS for high contrast and premium look
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Headers and text visibility */
    h1, h2, h3, p, span, label {
        color: #1E3D59 !important;
    }
    .stMarkdown p {
        color: #1E3D59 !important;
    }
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #FF4B4B;
        color: white !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #E03E3E;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    /* Download button */
    .stDownloadButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #28A745;
        color: white !important;
        font-weight: bold;
        border: none;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1E3D59;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App Content
st.title("☀️ Solar Load Calculator")
st.markdown("### Empowering People with Renewable Energy Solutions")

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input("Enter Gemini API Key", value=env_key, type="password")
    
    if not api_key:
        st.info("Get your API key from [Google AI Studio](https://aistudio.google.com/)")
    elif env_key:
        st.success("✅ Using API Key from .env")
    else:
        st.warning("🔑 API Key entered manually")

# Main Content
st.write("---")
uploaded_file = st.file_uploader("📤 Upload Electricity Bill (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded file
    if uploaded_file.type == "application/pdf":
        st.info(f"📄 PDF Uploaded: {uploaded_file.name}")
    else:
        st.image(uploaded_file, caption="Uploaded Bill", use_column_width=True)

    # Initialize session state for extracted data
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None

    if st.button("🚀 Process Bill"):
        if not api_key:
            st.error("Please provide a Gemini API Key in the sidebar or .env file.")
        else:
            with st.spinner("Analyzing bill with AI..."):
                try:
                    extractor = BillExtractor(api_key)
                    file_content = uploaded_file.read()
                    mime_type = uploaded_file.type
                    data = extractor.extract(file_content, mime_type)
                    
                    if data:
                        st.session_state.extracted_data = data
                        st.success("✅ Data Extracted Successfully! Please verify below.")
                    else:
                        st.error("Failed to extract data. Please try again.")
                except Exception as e:
                    if "429" in str(e):
                        st.error("❌ Quota Exceeded: Your API key has hit its limit.")
                    else:
                        st.error(f"An error occurred: {e}")

    # Show verification UI if data is in session state
    if st.session_state.extracted_data:
        data = st.session_state.extracted_data
        st.write("---")
        st.subheader("📝 Verify Extracted Data")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Consumer Name", data.get("consumer_name", ""))
            c_num = st.text_input("Consumer Number", data.get("consumer_number", ""))
            month = st.text_input("Billing Month", data.get("billing_month", ""))
            load = st.text_input("Sanctioned Load", data.get("sanctioned_load", ""))
        
        with col2:
            units = st.number_input("Units Consumed", value=float(data.get("units_consumed", 0)) if data.get("units_consumed") else 0.0)
            amount = st.number_input("Bill Amount", value=float(data.get("bill_amount", 0)) if data.get("bill_amount") else 0.0)
            fixed = st.number_input("Fixed Charges", value=float(data.get("fixed_charges", 0)) if data.get("fixed_charges") else 0.0)
            conn = st.text_input("Connection Type", data.get("connection_type", ""))

        final_data = {
            "consumer_name": name,
            "consumer_number": c_num,
            "billing_month": month,
            "units_consumed": units,
            "bill_amount": amount,
            "sanctioned_load": load,
            "fixed_charges": fixed,
            "connection_type": conn
        }

        if st.button("📊 Generate Solar Calculation Report"):
            with st.spinner("Populating Excel template..."):
                template_path = "templates/solar_template.xlsx"
                if not os.path.exists(template_path):
                    template_path = "C:/Users/penum/.gemini/antigravity/scratch/ai/SolarLoadCalculator/templates/solar_template.xlsx"
                
                filler = ExcelFiller(template_path)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                    output_path = tmp.name
                
                filler.fill_bill_data(final_data, output_path)
                
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Final Excel Report",
                        data=f,
                        file_name=f"Solar_Report_{name.replace(' ', '_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                st.success("✨ Report ready for download!")


st.markdown("---")
st.markdown("Developed by **Penumudi Venkata Sai** for EnergyBae AI Intern Task.")
