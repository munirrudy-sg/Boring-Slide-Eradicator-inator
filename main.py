import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import fitz  # PyMuPDF
from pptx import Presentation
from pptx.util import Pt
import io

def calculate_paragraph_height(paragraph):
    # Approximate the height of the paragraph based on the number of lines and font size
    font_size = 14  # Default font size
    line_spacing = 1.2  # Default line spacing factor
    num_lines = len(paragraph.runs)  # Number of lines in the paragraph
    return num_lines * font_size * line_spacing

def create_presentation(prs, text):
    text=text.strip()
    lines = text.split('\n')

    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)
    title_shape = slide.shapes.title
    slide.shapes._spTree.remove(title_shape._element)

    text_frame = slide.shapes.add_textbox(left=0, top=0, width=prs.slide_width, height=prs.slide_height).text_frame

    max_paragraph_width = 0
    total_text_frame_height = 0

    for line in lines:
        if line == "**Slide:**":
            continue
        if "Citations" in line or "References" in line:
            break
        if line.startswith("* "):
            line = line[2:]
            p = text_frame.add_paragraph()
            p.space_after = Pt(0)
            p.space_before = Pt(0)
            p.level = 0

            line = line.strip()
            if line.startswith("* "):
                line = line[2:]

            words = line.split()

            for word in words:
                if word.startswith("**") and word.endswith("**"):
                    bold_word = word[2:-2]
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                    r.font.size = Pt(12)
                elif word.startswith("**"):
                    bold_text = True
                    bold_word = word[2:]
                    r = p.add_run()
                    r.text = bold_word + " "
                    r.font.bold = True
                    r.font.size = Pt(12)
                elif bold_text and word.endswith("**"):
                    bold_text = False
                    bold_word = word[:-2]
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                    r.font.size = Pt(12)
                elif bold_text:
                    r = p.add_run()
                    r.text = word + " "
                    r.font.bold = True
                    r.font.size = Pt(12)
                else:
                    r = p.add_run()
                    r.text = word + " "
            for run in p.runs:
                run.font.size = Pt(12)
        else:
            p = text_frame.add_paragraph()

            bold_text = False
            words = line.split()

            for word in words:
                if word.startswith("**") and word.endswith("**"):
                    bold_word = word[2:-2]
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                elif word.startswith("**"):
                    bold_text = True
                    bold_word = word[2:]
                    r = p.add_run()
                    r.text = bold_word + " "  #
                    r.font.bold = True
                elif bold_text and word.endswith("**"):
                    bold_text = False
                    bold_word = word[:-2]
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                elif bold_text:
                    r = p.add_run()
                    r.text = word + " "
                    r.font.bold = True
                else:
                    r = p.add_run()
                    r.text = word + " "

                r.font.size = Pt(14)

            paragraph_width = sum(run.font.size for run in p.runs)
            if paragraph_width > max_paragraph_width:
                max_paragraph_width = paragraph_width

            paragraph_height = calculate_paragraph_height(p)
            total_text_frame_height += paragraph_height

    text_frame.width = max_paragraph_width

    text_frame.height = total_text_frame_height

    # Calculate the center of the slide
    center_x = prs.slide_width // 2
    center_y = prs.slide_height // 2

    # Center align the text frame
    text_frame.left = center_x - text_frame.width // 2
    text_frame.top = center_y - text_frame.height // 2

    return prs

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
    prs = Presentation()
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
        if hasattr(ai_response, 'parts') and ai_response.parts:
            for part in ai_response.parts:
                st.text(part.text)
        else:
            st.text("No enhanced content available")
        create_presentation(prs,
                            ai_response.parts[0].text if hasattr(ai_response, 'parts') and ai_response.parts else "")
    prs.save("output.pptx")
    output_data = io.BytesIO()
    prs.save(output_data)
    output_data.seek(0)
    st.download_button(label="Download PowerPoint", data=output_data, file_name="output.pptx",
                       mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")


