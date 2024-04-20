import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import fitz  # PyMuPDF
from pptx import Presentation
from pptx.util import Pt, Inches
import io

def calculate_paragraph_height(paragraph):
    # Approximate the height of the paragraph based on the number of lines and font size
    font_size = 14  # Default font size
    line_spacing = 1.2  # Default line spacing factor
    num_lines = len(paragraph.runs)  # Number of lines in the paragraph
    return num_lines * font_size * line_spacing


def create_presentation(prs, title, text):
    text = text.strip()
    lines = text.split('\n')

    slide_layout = prs.slide_layouts[5]  # title and content layout
    slide = prs.slides.add_slide(slide_layout)

    # Set the slide width and height to 16:9 aspect ratio
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)  # Height is calculated as width * 9/16

    title_shape = slide.shapes.title
    title_shape.text = title  # Add title text to the title shape
    title_width = prs.slide_width  # Set the title to the full width of the slide

    # Set the height and top position of the title
    title_height = Inches(0.5) 
    title_top = Inches(0.5)  
    title_shape.height = title_height
    title_shape.width = title_width
    title_shape.top = title_top

    # Directly access the title shape's text frame and adjust the font size
    title_text_frame = title_shape.text_frame
    for paragraph in title_text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(24)  # Set a smaller font size for the title

    # Calculate where the content should start, below the title
    content_top = title_top + title_height

    # Calculate the content text frame size
    text_frame_width = prs.slide_width - Inches(1)  # Adjust for margins
    text_frame_height = prs.slide_height - content_top - Inches(0.5)  # Adjust for bottom margin
    text_frame = slide.shapes.add_textbox(Inches(0.5), content_top, text_frame_width, text_frame_height).text_frame
    text_frame.word_wrap = True  # Ensure text wraps within the text frame

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
                    r.text = bold_word + " "  
                    r.font.bold = True
                elif bold_text and word.endswith("**"):
                    bold_text = False
                    bold_word = word[:-2]
                    r = p.add_run()
                    r.text = bold_word + " "
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
    status_message = st.empty()
    with st.spinner('Processing your slides...'):
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

        total_slides = len(slides_data)
        # Process each slide through Gemini-Pro AI model
        for i, (page_number, title, content) in enumerate(slides_data, start=1):
            # Update the status message with the number of slides left
            status_message.text(f'Processing slide {page_number} of {total_slides}...')
            # Construct the prompt for the AI model
            prompt = f"Explain this slide in greater detail with citations: {content}. Just enhance the slide content with greater explanation. Don't need to add titles to the slide."

            # Send the prompt to the Gemini-Pro AI model
            ai_response = model.generate_content([prompt])

            # Display the enhanced content
            st.subheader(f"Page {page_number}: {title}")
            if hasattr(ai_response, 'parts') and ai_response.parts:
                for part in ai_response.parts:
                    st.text(part.text)
            else:
                st.text("No enhanced content available")
            create_presentation(prs, title,
                                ai_response.parts[0].text if hasattr(ai_response, 'parts') and ai_response.parts else "")
        prs.save("output.pptx")
        output_data = io.BytesIO()
        prs.save(output_data)
        output_data.seek(0)

    # Clear the status message once done processing
    status_message.empty()

    st.success('Processing complete!')
    st.download_button(label="Download PowerPoint", data=output_data, file_name="output.pptx",
                       mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")


