
The AI Business Trend Meme Generator is a Python-based application that combines the power of Google Gemini AI with Gradio to create fun, engaging, and context-aware memes based on current business trends or situations. This is a Python application that uses the Google Gemini API to generate a variety of relevant, humorous memes based on a user-provided business trend or situation. It features a simple web interface built with Gradio.


*(Suggestion: After running the app, take a screenshot of the interface and replace the line above with it.)*

---

##  Features

* **AI-Powered Captions**: Leverages the Gemini Pro model to understand context and generate witty captions.
* **Multiple Templates**: Automatically creates different memes for the same trend using a variety of popular templates.
* **Dynamic Font Sizing**: Intelligently calculates the best font size to make text readable and centered.
* **Simple Web Interface**: Built with Gradio for easy, interactive use in a browser.

---

##  Setup and Installation

Follow these steps to get the meme generator running on your local machine.

### **1. Clone the Repository**

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

### **2. Create a Virtual Environment**

It's highly recommended to use a virtual environment to keep dependencies organized.

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### **3. Install Dependencies**

Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### **4. Add Your API Key**

You need a Google Gemini API key to run this project.

1.  Create a file named `.env` in the main project directory.
2.  Add your API key to this file in the following format:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
3.  You can get a key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### **5. Download the Font**

The application uses the "DejaVu Sans Bold" font.

1.  Download the font file from a trusted source like [DejaVu Fonts](https://dejavu-fonts.github.io/).
2.  Find the `DejaVuSans-Bold.ttf` file and place it in the same directory as `app.py`.

---
<img width="1440" height="768" alt="2" src="https://github.com/user-attachments/assets/8501c3df-d626-4975-8be3-0d1a3958551e" />

##  How to Run

Once you have completed the setup, run the following command in your terminal:

```bash
python app.py
```

This will start the Gradio server. Open the local URL provided in the terminal (e.g., `http://127.0.0.1:7860`) in your web browser to use the app.

---

##  How to Add New Meme Templates

You can easily add more templates:

1.  **Find a Template**: Go to a site like [Imgflip](https://imgflip.com/memetemplates) and find a blank template. Right-click the image and "Copy Image Address" to get the URL.
2.  **Find Coordinates**: Use an online "image coordinate finder" tool to draw boxes over the text areas and get their `x`, `y`, `width`, and `height`.
3.  **Update `app.py`**: Open the `app.py` file and add a new dictionary to the `MEME_TEMPLATES` list with the information you collected.
