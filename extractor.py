import google.generativeai as genai
import json
import os
from PIL import Image
import pdfplumber
import io

class BillExtractor:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # Using gemini-flash-latest to maximize availability and quota
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def extract(self, file_content, mime_type):
        """
        Extracts data from a bill (image or PDF).
        file_content: bytes
        mime_type: string (e.g., 'application/pdf', 'image/jpeg')
        """
        
        prompt = """
        Extract the following details from this electricity bill. 
        If a field is not found, return null.
        Return the data in a strict JSON format.
        
        Fields to extract:
        - consumer_name: The name of the customer
        - consumer_number: The unique consumer number
        - billing_month: The month and year of the bill (e.g., "January 2026")
        - units_consumed: Total units (kWh) consumed in this month
        - bill_amount: Total amount to be paid
        - sanctioned_load: Sanctioned load in kW
        - fixed_charges: Monthly fixed charges or demand charges
        - connection_type: The tariff category or connection type (e.g., "90/ LT I Res 1-Phase")
        
        Example JSON output:
        {
          "consumer_name": "John Doe",
          "consumer_number": "123456789",
          "billing_month": "January 2026",
          "units_consumed": 150.5,
          "bill_amount": 1200.0,
          "sanctioned_load": "3.3 kW",
          "fixed_charges": 130.0,
          "connection_type": "LT-1 Residential"
        }
        """

        # Prepare the content for Gemini
        if 'pdf' in mime_type:
            response = self.model.generate_content([prompt, {"mime_type": "application/pdf", "data": file_content}])
        else:
            # For images
            img = Image.open(io.BytesIO(file_content))
            response = self.model.generate_content([prompt, img])

        try:
            # Extract JSON from response
            text = response.text
            # Remove markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            print(f"Raw response: {response.text}")
            return None
