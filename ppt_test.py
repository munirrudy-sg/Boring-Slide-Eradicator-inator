from pptx import Presentation
from pptx.util import Pt

text = '''
**Cellular Network Security**

**Basic Cellular Network Architecture**

* **Base Transceiver Station (BTS):** Communicates with mobile devices and connects them to the core network.
* **Radio Network Controller (RNC):** Manages radio resources and handovers between BTSs.
* **Mobile Switching Center (MSC):** Establishes and terminates calls, and authenticates users.
* **Home Location Register (HLR):** Stores user subscription data and location information.
* **Visitor Location Register (VLR):** Stores user data and location information for users roaming from other networks.

**Authentication and Encryption**

* **Subscriber Identity Module (SIM) card:** Stores user authentication keys.
* **Authentication Center (AuC):** Stores authentication keys and verifies user identity.
* **Ciphering Key Generation (CKG) algorithm:** Generates encryption keys for secure communication between the device and the BTS.
* **Kasumi algorithm:** Used for encrypting user data.

**Vulnerabilities in Cellular Network Security**

* **Interception and eavesdropping:** Malicious actors can listen to unencrypted communications.
* **Impersonation:** Attackers can spoof or clone SIM cards to impersonate legitimate users.
* **Interception and modification:** Attackers can intercept and modify data packets to obtain sensitive information or compromise the network.
* **Man-in-the-middle (MITM) attacks:** Attackers can intercept and manipulate communication between devices and the network.

**Mitigation Techniques**

* **Strong authentication mechanisms:** Using advanced encryption algorithms and multi-factor authentication.
* **Secure network protocols:** Implementing secure protocols such as IPsec to protect data transmissions.
* **Regular security updates:** Patching vulnerabilities in network infrastructure and devices.
* **Network intrusion detection and prevention systems (IDS/IPS):** Monitoring network traffic for suspicious activities.

**References:**

* International Telecommunication Union (ITU): "Security in Cellular Networks" (https://www.itu.int/en/ITU-T/studygroups/Documents/sec/201203-WTSA12-Cellular-network-security.docx)
* European Telecommunications Standards Institute (ETSI): "Security Requirements for Cellular Networks" (https://www.etsi.org/deliver/etsi_tr/102200_102299/102203/02.02.01_60/tr_102203v020201p.pdf)
* National Institute of Standards and Technology (NIST): "Security Considerations for Cellular Networks" (https://csrc.nist.gov/publications/detail/sp/800-121r1/final)
'''

def calculate_paragraph_height(paragraph):
    # Approximate the height of the paragraph based on the number of lines and font size
    font_size = 14  # Default font size
    line_spacing = 1.2  # Default line spacing factor
    num_lines = len(paragraph.runs)  # Number of lines in the paragraph
    return num_lines * font_size * line_spacing

def create_presentation(prs, text):
    text=text.strip()
    # Split text into lines
    lines = text.split('\n')

    slide_layout = prs.slide_layouts[5]  # Use index 5 for a blank slide layout
    slide = prs.slides.add_slide(slide_layout)
    title_shape = slide.shapes.title
    slide.shapes._spTree.remove(title_shape._element)

    # Create a new text frame on the slide
    text_frame = slide.shapes.add_textbox(left=0, top=0, width=prs.slide_width, height=prs.slide_height).text_frame

    max_paragraph_width = 0
    total_text_frame_height = 0

    for line in lines:
        if line == "**Slide:**":
            continue
        if "Citations" in line or "References" in line:
            break
        # Check if the line starts with four spaces to indicate a bullet point
        if line.startswith("* "):
            line = line[2:]
            # Create a new paragraph in the text frame
            p = text_frame.add_paragraph()
            # Set the bullet style
            p.space_after = Pt(0)
            p.space_before = Pt(0)
            p.level = 0  # Set bullet level

            line = line.strip()
            if line.startswith("* "):
                line = line[2:]

            words = line.split()

            for word in words:
                if word.startswith("**") and word.endswith("**"):
                    # Remove the "**" characters
                    bold_word = word[2:-2]
                    # Add the word as bold with font size 12
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                    r.font.size = Pt(12)
                # Check if the word should be bold
                elif word.startswith("**"):
                    # Start of bold text
                    bold_text = True
                    # Remove the leading "**" characters
                    bold_word = word[2:]
                    # Add the word as bold with font size 12
                    r = p.add_run()
                    r.text = bold_word + " "  # Add a space after each word
                    r.font.bold = True
                    r.font.size = Pt(12)
                elif bold_text and word.endswith("**"):
                    # End of bold text
                    bold_text = False
                    # Remove the trailing "**" characters
                    bold_word = word[:-2]
                    # Add the word as bold with font size 12
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                    r.font.size = Pt(12)
                elif bold_text:
                    # Word inside bold text
                    r = p.add_run()
                    r.text = word + " "  # Add a space after each word
                    r.font.bold = True
                    r.font.size = Pt(12)
                else:
                    # Regular text
                    r = p.add_run()
                    r.text = word + " "  # Add a space after each word

                # Set the font size to smaller than 14 points for the entire paragraph
            for run in p.runs:
                run.font.size = Pt(12)
        else:
            # Create a new paragraph in the text frame
            p = text_frame.add_paragraph()

            bold_text = False
            # Split the line into words
            words = line.split()

            for word in words:
                if word.startswith("**") and word.endswith("**"):
                    # Remove the "**" characters
                    bold_word = word[2:-2]
                    # Add the word as bold
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                # Check if the word should be bold
                elif word.startswith("**"):
                    # Start of bold text
                    bold_text = True
                    # Remove the leading "**" characters
                    bold_word = word[2:]
                    # Add the word as bold
                    r = p.add_run()
                    r.text = bold_word + " "  # Add a space after each word
                    r.font.bold = True
                elif bold_text and word.endswith("**"):
                    # End of bold text
                    bold_text = False
                    # Remove the trailing "**" characters
                    bold_word = word[:-2]
                    # Add the word as bold
                    r = p.add_run()
                    r.text = bold_word
                    r.font.bold = True
                elif bold_text:
                    # Word inside bold text
                    r = p.add_run()
                    r.text = word + " "  # Add a space after each word
                    r.font.bold = True
                else:
                    # Regular text
                    r = p.add_run()
                    r.text = word + " "  # Add a space after each word

                # Set the font size to 14 points
                r.font.size = Pt(14)

            # Calculate the width of the paragraph and update max_paragraph_width
            paragraph_width = sum(run.font.size for run in p.runs)
            if paragraph_width > max_paragraph_width:
                max_paragraph_width = paragraph_width

            # Calculate the height of the paragraph and update total_text_frame_height
            paragraph_height = calculate_paragraph_height(p)
            total_text_frame_height += paragraph_height

    # Set the text frame width to the maximum paragraph width
    text_frame.width = max_paragraph_width

    # Set the text frame height to the total height of all paragraphs
    text_frame.height = total_text_frame_height

    # Calculate the center of the slide
    center_x = prs.slide_width // 2
    center_y = prs.slide_height // 2

    # Center align the text frame
    text_frame.left = center_x - text_frame.width // 2
    text_frame.top = center_y - text_frame.height // 2

    for paragraph in text_frame.paragraphs:
        print(paragraph.text)

    return prs


prs = Presentation()
create_presentation(prs,text)
prs.save("output.pptx")
