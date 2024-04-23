import re

# Example AI response text
response_text = """
[
  {
    "slide_number": 1,
    "title": "Android Reverse Engineering",
    "content": "## Android Reverse Engineering: A Deep Dive\n\nThis lecture series delves into the fascinating world of Android Reverse Engineering, exploring the techniques and tools used to analyze and understand the inner workings of Android applications. We'll navigate through the complexities of Android app structure, delve into the manifest file and its components, and explore the conversion of dex code to smali and source code. Additionally, we'll shed light on native code analysis and equip you with the knowledge to design your own dummy machine language. Buckle up for an exciting journey into the realm of mobile security!\n\n**Instructor:** A/Prof. Vivek Balachandran\n**Email:** Vivek.b@singaporetech.edu.sg\n**Course:** ICT 2215 Mobile Security"
  },
  {
    "slide_number": 2,
    "title": "Overview",
    "content": "## Course Roadmap:\n\n* **Demystifying Android Reverse Engineering:** We'll begin by understanding the fundamental concepts and methodologies behind reverse engineering Android applications.  
* **Dissecting Android Code Structure:** We'll explore the organization of an Android app, from the high-level components to the intricate details of the file system.
* **Unveiling the Manifest File:** The manifest file serves as the blueprint of an app. We'll examine its components, including activities, services, content providers, and broadcast receivers, and understand their roles in the application's functionality.
* **From Dex to Smali:** We'll delve into the process of converting Dalvik Executable (DEX) bytecode, the format used by Android apps, into Smali code, a human-readable representation that facilitates analysis.
* **Decoding Dex to Source Code:**  We'll explore techniques and tools to convert DEX bytecode back into its original source code, such as Java or Kotlin, providing valuable insights into the app's logic and behavior.
* **Navigating Native Code Analysis:** We'll explore the analysis of native code, typically written in C/C++, which is often used for performance-critical or platform-specific tasks.
* **Building a Dummy Machine Language:**  We'll embark on a hands-on project to design a simplified machine language, gaining a deeper understanding of low-level programming concepts."
  }
]
"""

# Regular expression to extract text in quotations from `"content": "..."` to `"\n}`
# This pattern captures multiline content, handling both escaped quotes and newline characters
content_pattern = r'"content":\s*"([^"]+)"'  # Matches the content within "content": "..."
content_matches = re.findall(content_pattern, response_text, re.DOTALL)  # Extract all matches, including newlines

# Display the extracted content
print("Extracted content:")
for content in content_matches:
    print("START")
    print(content)
