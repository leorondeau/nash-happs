import pytesseract
from PIL import Image
import re
import glob
from datetime import datetime

date_language_pattern = re.compile(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|AM|PM|am|pm|o\'clock)\b', re.IGNORECASE)

def extract_text_from_image(post):
    try:
        image_files = glob.glob(f'temp/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC*.jpg')

        if image_files:
            image_path = image_files[0]
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)

            current_date_str = datetime.now().strftime('%Y-%m-%d')
            return current_date_str in text, text
        else:
            print(f"Image for post {post.shortcode} was not found.")
            return False, None
    except Exception as e:
        print(f"Error processing post {post.shortcode}: {e}")
        return False, None