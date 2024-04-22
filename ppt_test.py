from pptx import Presentation
from pptx.util import Pt,Inches

text = '''
"- **Reverse engineering** in software involves dissecting a program to understand its inner workings. This often leads to legal disputes, as companies try to protect their intellectual property.\n
- **Landmark Cases:**\n    * **Atari v. Nintendo (1992):** Atari reverse-engineered Nintendo's lockout chip to create compatible games. The court ruled in favor of Atari, establishing the principle of fair use for reverse engineering when necessary to access an interoperable system. [Citation: Atari Games Corp. v. Nintendo of America Inc., 975 F.2d 832 (Fed. Cir. 1992)]\n    * **Sega v. Accolade (1992
):** Similar to the Atari case, Accolade reverse-engineered Sega's console to develop compatible games. The court ruled in favor of Accolade, reinforcing the right to reverse engineer for interoperability purposes. [Citation: Sega Enterprises Ltd. v. Accolade, Inc., 977 F.2d 1510 (9th Cir. 1992)]\n    * **P
hoenix Technologies v. IBM (1988):** Phoenix reverse-engineered IBM's BIOS to create a compatible version. The court found that Phoenix had infringed on IBM's copyright, highlighting the limitations of fair use when direct copying is involved. [Citation: Phoenix Technologies, Ltd. v. International Business 
Machines Corp., 896 F.2d 1265 (9th Cir. 1988)]\n    * **Connectix v. Sony (2000):** Connectix reverse-engineered Sony's PlayStation BIOS to develop a PlayStation emulator for Macintosh computers. The court ruled in favor of Connectix, emphasizing the legality of reverse engineering for interoperability even
 when involving copyrighted material. [Citation: Sony Computer Entertainment, Inc. v. Connectix Corp., 203 F.3d 596 (9th Cir. 2000)]\n- **Challenges in Legal Battles:** Proving infringement in reverse engineering cases is often difficult due to the technical complexity and the application of fair use principles.\n- **Chinese Wall Method:** To mitigate legal risks, companies may employ a \"Chinese wall\" approach, where a separate team conducts reverse engineering without access to the original source code, aiming to demonstrate independent creation.
'''
def create_slide(prs, title, content):
    # Create a blank slide with custom placeholders
    slide_layout = prs.slide_layouts[6]  # Choose an appropriate layout index

    slide = prs.slides.add_slide(slide_layout)

    # Set the title
    title_shape = slide.shapes.add_textbox(Inches(0.25), Inches(0.25), Inches(9), Inches(0.5))
    title_text_frame = title_shape.text_frame
    title_text_frame.word_wrap = True
    title_text_frame.text = title

    # Set the content
    content_shape = slide.shapes.add_textbox(Inches(0.25), Inches(0.75), Inches(9), Inches(4))
    content_text_frame = content_shape.text_frame
    content_text_frame.word_wrap = True

    print(content)
    # Replace visible newline characters with a placeholder
    text = content.replace('\n', '$$$')
    print(text)
    # Join the lines using the newline character (\n)
    combined_text = ''.join(text.split('\\n'))

    #print(combined_text)

    # Split text using hard '\n'
    lines = content.split('\\n')

    # Filter out empty lines
    filtered_lines = [line.strip() for line in lines if line.strip()]

    # Print filtered lines




    # Set content paragraphs
    for line in lines:
        p = content_text_frame.add_paragraph()
        words = line.split()

        bolded_mode=False
        for word in words:
            if bolded_mode:
                if word.endswith("**:"):
                    bold_word = word[:-3]
                    r = p.add_run()
                    r.text = bold_word+":"
                    r.font.bold = True
                    bolded_mode = False
                else:
                    r = p.add_run()
                    r.text = word + " "
                    r.font.bold = True
            elif word.startswith("**"):
                bold_word = word[2:]
                r = p.add_run()
                r.text = bold_word+" "
                r.font.bold = True
                bolded_mode=True
            else:
                r = p.add_run()
                r.text = word + " "

        # Add a new paragraph for the next line
       # content_text_frame.add_paragraph()

    # Adjust font size
    for shape in slide.shapes:
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(14)  # Adjust font size as needed


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

# Example usage:
data = [
    {
        "title": "Software Reverse Engineering: Legal Battles and the Chinese Wall Method",
        "content": '''- **Reverse engineering** in software involves dissecting a program to understand its inner workings. This often leads to legal disputes, as companies try to protect their intellectual property.\n
- **Landmark Cases:**\n    * **Atari v. Nintendo (1992):** Atari reverse-engineered Nintendo's lockout chip to create compatible games. The court ruled in favor of Atari, establishing the principle of fair use for reverse engineering when necessary to access an interoperable system. [Citation: Atari Games Corp. v. Nintendo of America Inc., 975 F.2d 832 (Fed. Cir. 1992)]\n    * **Sega v. Accolade (1992
):** Similar to the Atari case, Accolade reverse-engineered Sega's console to develop compatible games. The court ruled in favor of Accolade, reinforcing the right to reverse engineer for interoperability purposes. [Citation: Sega Enterprises Ltd. v. Accolade, Inc., 977 F.2d 1510 (9th Cir. 1992)]\n    * **P
hoenix Technologies v. IBM (1988):** Phoenix reverse-engineered IBM's BIOS to create a compatible version. The court found that Phoenix had infringed on IBM's copyright, highlighting the limitations of fair use when direct copying is involved. [Citation: Phoenix Technologies, Ltd. v. International Business 
Machines Corp., 896 F.2d 1265 (9th Cir. 1988)]\n    * **Connectix v. Sony (2000):** Connectix reverse-engineered Sony's PlayStation BIOS to develop a PlayStation emulator for Macintosh computers. The court ruled in favor of Connectix, emphasizing the legality of reverse engineering for interoperability even
 when involving copyrighted material. [Citation: Sony Computer Entertainment, Inc. v. Connectix Corp., 203 F.3d 596 (9th Cir. 2000)]\n- **Challenges in Legal Battles:** Proving infringement in reverse engineering cases is often difficult due to the technical complexity and the application of fair use principles.\n- **Chinese Wall Method:** To mitigate legal risks, companies may employ a \"Chinese wall\" approach, where a separate team conducts reverse engineering without access to the original source code, aiming to demonstrate independent creation.
'''
    }
]

presentation = create_presentation(data)
presentation.save("presentation.pptx")
