import time
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import fitz  # pip install PyMuPDF
from pptx import Presentation  # pip install python-pptx
from pptx.util import Pt, Inches
import io
import json
import re


def convert_slides_data_to_text(slides_data):
    # Create a plain text representation of slides_data
    slides_text = ""
    for slide in slides_data:
        slide_number, title, content = slide
        slides_text += f"Slide {slide_number}:\n"
        slides_text += f"Title: {title}\n"
        slides_text += "Content:\n"
        slides_text += content + "\n"  # Adding a new line for separation
        slides_text += "\n" + "-" * 40 + "\n"  # Separator between slides
    return slides_text


def apply_bold_format(word, r, bolded_mode):
    # Check if the word starts and ends with double asterisks
    if word.startswith("**") and word.endswith("**"):
        r.text = word[2:-2]  # Remove outer asterisks
        r.font.bold = True
    elif word.startswith("**"):
        r.text = word[2:] + " "  # Remove leading asterisks
        r.font.bold = True
        bolded_mode = True  # Switch to bolded mode
    elif word.endswith("**"):
        r.text = word[:-2] + " "  # Remove trailing asterisks
        r.font.bold = True
        bolded_mode = False  # Exit bolded mode
    elif bolded_mode:
        r.text = word + " "  # Apply bolded mode to other words
        r.font.bold = True
    else:
        r.text = word + " "  # Normal text, no bold
    return bolded_mode


def create_slide(prs, title, content):
    # Create a new slide with appropriate layout
    slide_layout = prs.slide_layouts[5]  # Title and content layout
    slide = prs.slides.add_slide(slide_layout)

    # Set the title text box
    title_shape = slide.shapes.title
    title_shape.text = title  # Assign the title

    # Create the content text box
    content_shape = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(8), Inches(4))
    content_text_frame = content_shape.text_frame
    content_text_frame.word_wrap = True  # Ensure proper word wrapping

    # Split content into lines based on newline character
    lines = content.replace("\\n", "\n").split("\n")  # Convert escaped newlines

    for line in lines:
        if line.startswith("##"):
            # Heading line
            p = content_text_frame.add_paragraph()
            p.text = line[2:].strip()  # Remove "##"
            p.font.size = Pt(20)  # Larger font for headings
            p.font.bold = True
        elif line.startswith("*"):
            # Bullet point
            p = content_text_frame.add_paragraph()
            words = line.split()
            bolded_mode = False
            for word in words:
                r = p.add_run()
                bolded_mode = apply_bold_format(word, r, bolded_mode)  # Apply bolding
            for run in p.runs:
                run.font.size = Pt(12)  # Smaller font for bullet points
        else:
            # Normal text
            p = content_text_frame.add_paragraph()
            words = line.split()
            bolded_mode = False
            for word in words:
                r = p.add_run()
                bolded_mode = apply_bold_format(word, r, bolded_mode)  # Apply bold if needed
                r.font.size = Pt(14)  # Standard font size for regular text


def create_presentation(data):
    prs = Presentation()

    # Set slide width and height for 16:9 aspect ratio
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    for slide_data in data:
        title = slide_data.get("title", "")
        content = slide_data.get("content", "")
        create_slide(prs, title, content)

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

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 200000,
    "response_mime_type": "application/json",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                               generation_config=generation_config,
                               safety_settings=safety_settings)

# Display the app's title on the page
st.title("📄 Upload and Process Your PDF")

# Check if the session state already has a 'processed' flag
if 'processed' not in st.session_state:
    st.session_state.processed = False

if 'slides_data' not in st.session_state:
    st.session_state.slides_data = []
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

# Text input for custom prompt
custom_prompt_text = st.text_input("Enter materials to refer from (optional):")

# Check if file was removed
if uploaded_file is None:  # If file is removed or not uploaded
    st.session_state.processed = False  # Reset the processed flag
    st.session_state.slides_data = []  # Reset slides data if needed
    st.session_state.output_data = None  # Reset output data
else:  # File has been uploaded
    if not st.session_state.processed:
        status_message = st.empty()
        progress_text = "Initialising..."
        my_progress = st.progress(0, text=progress_text)

        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(5.625)

        doc = fitz.open("pdf", uploaded_file.read())  # Load the PDF file
        slides_data = []

        # List to store titles extracted from PDF
        titles = []

        # Process each page
        total_pages = len(doc)
        for i, page in enumerate(doc):
            text = page.get_text()
            # Since PDFs don't have explicit titles like PPT, you might need to parse the first line as a title
            lines = text.split('\n')
            title = lines[0] if lines else "No Title"
            content = "\n".join(lines[1:]) if len(lines) > 1 else "No Content"

            # Append the extracted data to slides_data
            slides_data.append((i + 1, title, content))

            # Store the title in the titles list
            titles.append(title)

            # Update progress
            progress = (i + 1) / total_pages * 25
            my_progress.progress(int(progress), "Processing slides")
            time.sleep(1)  # Add a delay of 1 second for the progress update

        st.session_state.slides_data = slides_data

        # Convert slides_data to plain text
        slides_text = convert_slides_data_to_text(slides_data)

        # Construct the prompt for the AI model

        if custom_prompt_text:
            prompt = f"The below text is extracted text from lecture slides. Based on the input text '{custom_prompt_text}', prioritize knowledge accordingly. Currently, the slides are bad and I want you to replace each slide content with your more well-explained version. Don't just explain it point by point. I want you to understand what the slide is trying to say then explain it in a way that can be easily understood by a university student. Include citations. Don't just write in plain text, use bullet points or anything that makes the student read and understand the slide easily. Do this for every slide but don't add new slides. Your output should be the slide number, title and slide content. Each slide separated by comma and text in markdown.\n\n{slides_text}."
        else:
            prompt = f"The below text is extracted text from lecture slides. Currently, the slides are bad and I want you to replace each slide content with your more well-explained version. Don't just explain it point by point. I want you to understand what the slide is trying to say then explain it in a way that can be easily understood by a university student. Include citations. Don't just write in plain text, use bullet points or anything that makes the student read and understand the slide easily. Do this for every slide but don't add new slides. Your output should be the slide number, title and slide content. Each slide separated by comma and text in markdown.\n\n{slides_text}."

        for i in range(25, 80):
            my_progress.progress(i, "Adding a hint of ai magic~")
            time.sleep(1)  # Add a delay of 1 second for the progress update

        # Send the prompt to the Gemini-Pro AI model
        response = model.generate_content(prompt, request_options={"timeout": 600000})  # 10 minutes timeout
        st.text(response.text)
        # print(response.text)
        # slides_content=json.loads(response.text)

        content_pattern = r'"content":\s*"([^"]+)"'  # Matches the content within "content": "..."
        content_matches = re.findall(content_pattern, response.text,
                                     re.DOTALL)  # Extract all matches, including newlines

        # Create a new list with PDF slide titles and AI response slide content
        PPT_data = []

        # Combining both PDF slide titles and AI response slide content
        if len(titles) == len(content_matches):
            for i, content in enumerate(content_matches):
                slide_number = i + 1
                title = titles[i]  # Get the corresponding title from Data A
                PPT_data.append({
                    "slide_number": slide_number,
                    "title": title,
                    "content": content
                })
        else:
            print("Mismatch in the number of titles and content elements.")
            print(titles)
            val = 0
            for content in content_matches:
                val = +1
                print(f'START {val}')
                print(content)

        print(PPT_data)

        presentation = create_presentation(PPT_data)
        presentation.save("output.pptx")
        output_data = io.BytesIO()
        presentation.save(output_data)
        output_data.seek(0)
        st.session_state.processed = True
        st.session_state.output_data = output_data

        # Clear the status message once done processing
        status_message.empty()
        my_progress.progress(100, "Finished!!!!")

    if st.session_state.processed:
        st.success('Processing complete!')
        st.download_button(label="Download PowerPoint", data=st.session_state.output_data, file_name="output.pptx",
                           mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
