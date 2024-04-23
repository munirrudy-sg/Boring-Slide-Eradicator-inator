import json
from pptx import Presentation
from pptx.util import Pt,Inches

# text = '''
# "- **Reverse engineering** in software involves dissecting a program to understand its inner workings. This often leads to legal disputes, as companies try to protect their intellectual property.\n
# - **Landmark Cases:**\n    * **Atari v. Nintendo (1992):** Atari reverse-engineered Nintendo's lockout chip to create compatible games. The court ruled in favor of Atari, establishing the principle of fair use for reverse engineering when necessary to access an interoperable system. [Citation: Atari Games Corp. v. Nintendo of America Inc., 975 F.2d 832 (Fed. Cir. 1992)]\n    * **Sega v. Accolade (1992
# ):** Similar to the Atari case, Accolade reverse-engineered Sega's console to develop compatible games. The court ruled in favor of Accolade, reinforcing the right to reverse engineer for interoperability purposes. [Citation: Sega Enterprises Ltd. v. Accolade, Inc., 977 F.2d 1510 (9th Cir. 1992)]\n    * **P
# hoenix Technologies v. IBM (1988):** Phoenix reverse-engineered IBM's BIOS to create a compatible version. The court found that Phoenix had infringed on IBM's copyright, highlighting the limitations of fair use when direct copying is involved. [Citation: Phoenix Technologies, Ltd. v. International Business 
# Machines Corp., 896 F.2d 1265 (9th Cir. 1988)]\n    * **Connectix v. Sony (2000):** Connectix reverse-engineered Sony's PlayStation BIOS to develop a PlayStation emulator for Macintosh computers. The court ruled in favor of Connectix, emphasizing the legality of reverse engineering for interoperability even
#  when involving copyrighted material. [Citation: Sony Computer Entertainment, Inc. v. Connectix Corp., 203 F.3d 596 (9th Cir. 2000)]\n- **Challenges in Legal Battles:** Proving infringement in reverse engineering cases is often difficult due to the technical complexity and the application of fair use principles.\n- **Chinese Wall Method:** To mitigate legal risks, companies may employ a \"Chinese wall\" approach, where a separate team conducts reverse engineering without access to the original source code, aiming to demonstrate independent creation.
# '''


def apply_bold_format(word, r,bolded_mode):
    if word.startswith("**") and (word.endswith(":**") or word.endswith("**:")):
        bold_word = word[2:-3]
        r.text = bold_word + ": "
        r.font.bold = True
    elif word.startswith("**"):
        bold_word = word[2:]
        r.text = bold_word + " "
        r.font.bold = True
        bolded_mode=True
    elif word == "*":
        r.text = "•" + " "  # Replace asterisk with bullet point
    elif bolded_mode:
        if word.endswith("**:") or word.endswith(":**"):
            bold_word = word[:-3]
            r.text = bold_word + ":"
            r.font.bold = True
            bolded_mode = False
        else:
            r.text = word + " "
            r.font.bold = True
    else:
        r.text = word + " "
    return bolded_mode  # Return the updated bolded_mode value
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

    # Split content into lines
    lines = content.split('\n')

    # Loop through each line
    for line in lines:
        # Check if the line starts with "##" indicating a heading
        if line.startswith("##"):
            # Create a new paragraph for heading
            p = content_text_frame.add_paragraph()
            # Add the heading text
            p.text = line[2:].strip()  # Remove the "##" and any leading/trailing whitespace
            # Set font size, bold, and center alignment for heading
            p.font.size = Pt(20)
            p.font.bold = True
            p.alignment = 1  # 0 for left alignment, 1 for center, 2 for right
        elif line.startswith("*"):
            # Create a new paragraph for smaller font size text
            p = content_text_frame.add_paragraph()
            # Add the text without the starting asterisk and leading/trailing whitespace
            words = line.split()
            bolded_mode = False
            for word in words:
                r = p.add_run()
                bolded_mode = apply_bold_format(word, r, bolded_mode)  # Update bolded_mode
            # Set font size for smaller text
            for run in p.runs:
                run.font.size = Pt(12)  # Adjust font size as needed
        else:
            # Create a new paragraph for regular text
            p = content_text_frame.add_paragraph()
            words = line.split()

            bolded_mode = False
            for word in words:
                r = p.add_run()
                apply_bold_format(word, r,bolded_mode)


    # Exclude font size adjustment for lines starting with asterisk
    for shape in slide.shapes:
        for paragraph in shape.text_frame.paragraphs:
            if not paragraph.text.startswith("*"):
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
data=[
    {
        "slide_number": 1,
        "title": "Android Reverse Engineering",
        "content": "## Android Reverse Engineering: A Deep Dive\n\nThis course, ICT 2215 Mobile Security, delves into the intricate world of Android app analysis. Led by A/Prof. Vivek Balachandran (Vivek.b@singaporetech.edu.sg), we will explore techniques to understand app functionality, identify vulnerabilities, and potentially modify their behavior. Get ready to unravel the secrets behind Android applications!"
    },
    {
        "slide_number": 2,
        "title": "Overview",
        "content": "## Course Roadmap\n\n* **Android Reverse Engineering:** Understanding the core principles and methodologies.\n* **Android Code Structure:** Exploring the organization of an Android app's codebase.\n* **Components in Manifest file:** Decoding the essential app metadata within the manifest.\n* **Dex to Smali:** Disassembling DEX bytecode into human-readable Smali code.\n* **Dex to Source code:** Converting DEX bytecode back into Java or Kotlin source code.\n* **Native code analysis:** Examining native code components written in languages like C.\n* **Design a dummy machine language:** A practical exercise to solidify your understanding of low-level code and assembly language."
    },
    {
        "slide_number": 3,
        "title": "Administrative Matters",
        "content": "## Mark Your Calendars!\n\n* **Guest Lecture:** We'll have a special session led by DarkNavy, a renowned security expert from China.\n* **Date & Time:** 19th March 2024, 9 AM – 11 AM\n* **Format:** Hybrid - Attend in person or join via Zoom (classroom details will be on LMS).\n* **CTF Session:** Get hands-on experience with a Capture the Flag challenge to hone your skills and identify your strengths."
    },
    {
        "slide_number": 4,
        "title": "Introduction to Android Reverse Engineering",
        "content": "## Demystifying Android Apps\n\nReverse engineering is like taking apart a complex machine to understand its inner workings. In the context of Android apps, it involves analyzing the compiled code and resources to:\n\n* **Comprehend App Behavior:** Discover how the app functions at a deeper level.\n* **Identify Security Flaws:** Uncover vulnerabilities that could be exploited by malicious actors.\n* **Customize and Modify:**  Potentially create modifications or enhancements to the app (always respecting ethical and legal boundaries)."
    },
    {
        "slide_number": 5,
        "title": "Android App Structure",
        "content": "## Inside the APK\n\nAndroid apps are packaged as APK (Android Package) files, which are essentially zip archives containing everything needed to run the app. Key components include:\n\n* **AndroidManifest.xml:** Defines the app's structure, components, permissions, and other essential information.\n* **res/ (Resources):** Stores images, layouts, strings, and other resources used by the app.\n* **assets/ (Assets):** Contains raw asset files, such as fonts or game data.\n* **DEX files:** Holds the compiled Java/Kotlin code (Dalvik Executable format)."
    },
    {
        "slide_number": 6,
        "title": "Android Manifest",
        "content": "## The App Blueprint\n\nThe AndroidManifest.xml file serves as the app's blueprint, declaring its core components and capabilities:\n\n* **Activities:** The building blocks of the user interface, representing individual screens.\n* **Services:** Background processes that perform long-running operations.\n* **Content Providers:** Manage shared data and facilitate data access between apps.\n* **Broadcast Receivers:** Respond to system-wide events or broadcasts.\n* **Intent Filters:** Define how activities, services, and receivers handle specific intents.\n* **Permissions:** Specify the app's access to system resources and user data."
    },
    {
        "slide_number": 7,
        "title": "Android Manifest components",
        "content": "## Manifest Essentials\n\nHere's a breakdown of key elements within the manifest:\n\n* **manifest:** The root element, defining the package name and namespace declarations.\n* **uses-sdk:** Specifies the minimum and target SDK versions supported by the app.\n* **uses-permission:** Declares the permissions required by the app, such as access to the camera or internet."
    },
    {
        "slide_number": 8,
        "title": "Android Manifest components",
        "content": "## Application Attributes\n\nThe application element houses app-level settings:\n\n* **android:name:** Specifies the application class name.\n* **android:allowBackup:** Controls whether backups are allowed.\n* **android:icon and android:label:** Define the app's icon and name.\n* **android:debuggable:** Enables debugging during development."
    },
    {
        "slide_number": 9,
        "title": "Android Manifest components",
        "content": "## Activities and Intents\n\n* **activity:** Declares an activity within the app. Activities must be declared to be functional.\n* **intent-filter:** Specifies the type of intents the component can respond to. The `MAIN` action and `LAUNCHER` category designate the app's entry point."
    },
    {
        "slide_number": 10,
        "title": "What to look for?",
        "content": "## Exported Activities: A Potential Entry Point\n\nPay close attention to the `android:exported` attribute within activity declarations. If set to `true`, the activity can be launched from outside the app, potentially exposing sensitive functionality. Use tools like `adb shell` to explore and interact with such activities."
    },
    {
        "slide_number": 11,
        "title": "Reverse Engineering",
        "content": "## Decoding the Code\n\nAndroid apps typically use Java or Kotlin, which are compiled into DEX (Dalvik Executable) bytecode. Reverse engineering involves:\n\n* **Dex to Smali:** Converting DEX into Smali, a human-readable intermediate language, using tools like apktool.\n* **Native Code Analysis:** If the app contains native code (C/C++), it needs to be analyzed at the assembly level using disassemblers and debuggers."
    },
    {
        "slide_number": 12,
        "title": "Native Code Analysis",
        "content": "## Bridging the Gap\n\nNative code is often found in libraries within the app's resources directory. To understand its interaction with the Java/Kotlin code, look for methods like `loadLibrary` or `load` that indicate native function calls. While the native code itself requires separate analysis, identifying these calls provides valuable insights."
    },
    {
        "slide_number": 13,
        "title": "Understanding code logic (Dex to Java)",
        "content": "## Recreating the Source\n\nTools like JADX, dex2jar, and online services like https://decompiler.com can attempt to convert DEX bytecode back into Java source code. However, the process isn't perfect and may not always produce compilable code. Despite limitations, decompilation can provide valuable insights into the app's logic and algorithms.\n\nFor Kotlin-based apps, consider using Fernflower for decompilation."
    },
    {
        "slide_number": 14,
        "title": "Modifying and Patching App",
        "content": "## App Modification: Tread Carefully\n\nModifying an app involves several steps:\n\n1. **Reverse to Smali:** Convert the DEX code into Smali format.\n2. **Edit Smali Code:** Make the desired changes directly within the Smali files.\n3. **Modify Resources (Optional):** Alter resources like images or layouts as needed.\n4. **Recompile and Re-sign:** Rebuild the APK and sign it with a valid certificate.\n\n**Important:** Always respect the app's End User License Agreement (EULA) and copyright laws. Modifying apps without permission can have legal consequences."
    },
    {
        "slide_number": 15,
        "title": "Crash Course on Programming Language",
        "content": "## Building Blocks of Code\n\nTo solidify your understanding of low-level code and assembly language, we'll embark on a practical journey:\n\n* **Designing a Dummy Assembly Language:** We'll create a simplified assembly language with its own set of instructions.\n* **Binary Code Representation:** We'll define how these instructions are represented in binary form.\n* **Assembly to Binary Conversion:** Learn how to convert assembly code into its corresponding binary representation."
    }
]
presentation = create_presentation(data)
presentation.save("presentation.pptx")