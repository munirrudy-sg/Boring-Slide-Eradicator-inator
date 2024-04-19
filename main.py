import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="AI PDF Processor",
    page_icon=":file_folder:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Display the app's title on the page
st.title("📄 Upload and Process Your PDF")

# File upload section
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
if uploaded_file is not None:
    doc = fitz.open("pdf", uploaded_file.read())  # Load the PDF file
    slides_data = []

    # Process each page
    for i, page in enumerate(doc):
        text = page.get_text()
        # Since PDFs don't have explicit titles like PPT, you might need to parse the first line as a title
        lines = text.split('\n')
        title = lines[0] if lines else "No Title"
        content = "\n".join(lines[1:]) if len(lines) > 1 else "No Content"

        # Append the extracted data to slides_data
        slides_data.append((i+1, title, content))

    # Process each slide through Gemini-Pro AI model
    for page_number, title, content in slides_data:
        # Construct the prompt for the AI model
        prompt = f"Explain this slide in greater detail with citations: {content}. Just enhance the slide content with greater explaination. Don't need to add titles to the slide"

        # Send the prompt to the Gemini-Pro AI model
        ai_response = model.generate_content([prompt])

        # Display the enhanced content
        st.subheader(f"Page {page_number}: {title}")
        st.text(ai_response.text)  

