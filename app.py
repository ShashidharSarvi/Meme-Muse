# ===============================================================
# AI BUSINESS TREND MEME GENERATOR
# ===============================================================

import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
import textwrap
import io
import gradio as gr

# Load environment variables from a .env file
load_dotenv()

# --- 1. CONFIGURE GEMINI API ---
def setup_gemini():
    """Initializes the Gemini model with the API key."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        print("❌ Gemini API Key not found in .env file.")
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("✅ Gemini API configured successfully.")
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        print(f"❌ Error configuring Gemini: {e}")
        return None


# --- 2. DEFINE MEME TEMPLATES & FONT HELPERS ---
MEME_TEMPLATES = [
    {
        "name": "Woman Yelling at a Cat",
        "url": "https://i.imgflip.com/345v97.jpg",
        "text_positions": [
            {"x": 20, "y": 200, "width": 500, "height": 300},
            {"x": 600, "y": 250, "width": 500, "height": 250}
        ],
        "description": "A two-panel meme. The first panel shows a woman yelling or upset. The second panel shows a confused-looking white cat sitting at a dinner table."
    },
    {
        "name": "Drake Hotline Bling",
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "text_positions": [
            {"x": 650, "y": 200, "width": 500, "height": 350},
            {"x": 650, "y": 750, "width": 500, "height": 350}
        ],
        "description": "A two-panel meme. Top panel: Drake looks displeased, rejecting something. Bottom panel: Drake looks pleased, approving of something."
    },
    {
        "name": "Distracted Boyfriend",
        "url": "https://i.imgflip.com/1ur9b0.jpg",
        "text_positions": [
            {"x": 800, "y": 450, "width": 350, "height": 200},
            {"x": 450, "y": 250, "width": 350, "height": 200},
            {"x": 150, "y": 350, "width": 300, "height": 200}
        ],
        "description": "A man is walking with his girlfriend but is looking back admiringly at another woman. The girlfriend looks on in disgust."
    }
]

def get_optimal_font_size(text, font_name, box_width, box_height):
    font_size = 100
    try:
        font = ImageFont.truetype(font_name, font_size)
        while font.getbbox(text)[2] > box_width or font.getbbox(text)[3] > box_height:
            font_size -= 2
            if font_size <= 5:
                font_size = 5
                break
            font = ImageFont.truetype(font_name, font_size)
        return font
    except IOError:
        print(f"Warning: Font '{font_name}' not found. Using default font.")
        return ImageFont.load_default()

# --- 3. CORE AI AND IMAGE FUNCTIONS ---
model = setup_gemini()

def generate_meme_caption(template, situation, brand_context="Our Brand"):
    box_count = len(template["text_positions"])
    template_name, template_desc = template["name"], template["description"]
    prompt = f"""You are a witty marketing assistant creating viral memes. Your task is to make a funny meme caption for the '{template_name}' template.
    **The Situation:** "{situation}"
    **The Brand:** "{brand_context}"
    **Template Description:** {template_desc}
    This template has {box_count} text boxes. Map the situation to the text boxes to make a hilarious meme.
    **Instructions:**
    - Create exactly {box_count} lines of text.
    - Format as:
      Box 1: [Text]
      Box 2: [Text]
      ...
    - Keep captions short (max 5 words)."""
    try:
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.9, max_output_tokens=150))
        return response.text
    except Exception as e:
        print(f"❌ Caption generation failed: {e}")
        return None

def create_meme_image(template, captions, index):
    try:
        response = requests.get(template["url"])
        img = Image.open(io.BytesIO(response.content)).convert('RGB')
        draw = ImageDraw.Draw(img)
        font_name = "DejaVuSans-Bold.ttf"

        caption_lines = [line.split(':', 1)[1].strip() for line in captions.strip().split('\n') if ':' in line]

        for i, position in enumerate(template["text_positions"]):
            if i < len(caption_lines):
                text = caption_lines[i].upper()
                box_width, box_height = position["width"], position["height"]

                font = get_optimal_font_size(text, font_name, box_width, box_height)
                
                avg_char_width = font.getlength("A")
                wrap_width = int(box_width / avg_char_width) if avg_char_width > 0 else 15
                wrapped_text = textwrap.fill(text, width=wrap_width)

                text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
                text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
                
                x = position["x"] + (box_width - text_width) / 2
                y = position["y"] + (box_height - text_height) / 2

                draw.text((x, y), wrapped_text, fill="white", font=font, stroke_width=5, stroke_fill="black", align="center")
        
        meme_path = f"generated_meme_{index}.jpg"
        img.save(meme_path)
        return meme_path
    except Exception as e:
        print(f"❌ Image creation failed: {e}")
        return None

# --- 4. GRADIO INTERFACE FUNCTION ---
def generate_memes_for_trend(situation):
    if not model:
        raise gr.Error("Gemini model is not initialized. Check your .env file and API key.")
    if not situation:
        raise gr.Error("Please enter a business trend or situation.")

    print(f"🔥 Generating memes for: '{situation}'")
    generated_image_paths = []
    
    for i, template in enumerate(MEME_TEMPLATES):
        print(f"🖼️ Using template: {template['name']}")
        caption = generate_meme_caption(template, situation, brand_context="The Team")
        if caption:
            meme_path = create_meme_image(template, caption, i)
            if meme_path:
                generated_image_paths.append(meme_path)
    
    if not generated_image_paths:
        raise gr.Error("Sorry, failed to generate any memes. Please try a different trend or check the logs.")
        
    return generated_image_paths

# --- 5. LAUNCH THE GRADIO APP ---
with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown("# 📈 Business Trend Meme Generator")
    gr.Markdown("Enter a business trend, a competitor's move, or any workplace situation, and let the AI create a batch of relevant memes for you.")
    
    text_input = gr.Textbox(
        label="Enter a business trend or situation:",
        placeholder="e.g., 'Everyone is talking about AI, but we haven't started using it yet.'"
    )
    submit_btn = gr.Button("Generate Memes", variant="primary")
    output_gallery = gr.Gallery(
        label="Generated Memes",
        show_label=True,
        columns=2,
        object_fit="contain",
        height="auto"
    )
    
    submit_btn.click(
        fn=generate_memes_for_trend,
        inputs=text_input,
        outputs=output_gallery
    )

print("🚀 Launching Gradio App...")
iface.launch()
