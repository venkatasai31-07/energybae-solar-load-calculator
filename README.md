# EnergyBae Solar Load Calculator — Automation Task

## 1. Project Overview
This project automates the manual process of analyzing electricity bills for solar system sizing. It bridges the gap between raw customer bills (PDF/Images) and the technical Excel templates used by the sales team to calculate ROI and solar capacity.

## 2. Features
- **AI-Powered OCR**: Uses Google Gemini 1.5 Flash to extract high-precision data (Consumer Name, Units, Load, etc.).
- **Smart Excel Integration**: Automatically identifies the correct monthly row and updates input cells while **preserving all formulas**.
- **User Verification UI**: A Streamlit interface that allows users to review and correct AI-extracted data before finalizing the report.
- **Support for MSEDCL Bills**: Specifically optimized for Maharashtra State Electricity bills.

## 3. Tech Stack
| Component | Technology |
| :--- | :--- |
| **Frontend/UI** | Streamlit |
| **AI/Extraction** | Google Gemini 1.5 Flash API |
| **Excel Handling** | openpyxl |
| **Environment** | Python 3.x |

## 4. Installation
1. Clone the repository:
   ```bash
   git clone <github-link>
   cd SolarLoadCalculator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 5. How To Run
1. Obtain a Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
2. Run the application:
   ```bash
   streamlit run app.py
   ```
3. Enter your API key in the sidebar.

## 6. Demo Workflow
1. **Upload**: Drop a bill image or PDF into the uploader.
2. **Extract**: The system sends the file to Gemini for structured extraction.
3. **Verify**: Review the extracted data in the UI and make any manual corrections.
4. **Download**: Click "Download Filled Excel Report" to get the final `.xlsx` file.

## 7. Future Improvements
- **Multi-Utility Support**: Expand extraction logic for other state electricity boards.
- **Batch Processing**: Allow uploading multiple bills at once.
- **History Tracking**: Store extracted data in a database (SQLite/PostgreSQL) for lead management.
- **Cloud Deployment**: Deploy the app on Streamlit Cloud or AWS for remote team access.

## 8. Developed By
**Penumudi Venkata Sai**
AI Intern / AI Engineer (Automation & Product Development)
EnergyBae Task Submission
