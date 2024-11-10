import os
import glob
from instaloader import Instaloader, Profile
from azure_api_test import extract_text_from_image  # Import your extraction function
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure temp directory exists
os.makedirs('temp', exist_ok=True)

class ExtractTextTool:
    def __init__(self):
        """Initialize the tool with Instaloader setup."""
        self.loader = Instaloader()

    def fetch_and_extract_text(self, username):
        """
        Fetches Instagram posts for a user, extracts text from the images, and returns the text.
        
        Args:
            username (str): The Instagram username.

        Returns:
            list: A list of text lines extracted from the images.
        """
        profile = Profile.from_username(self.loader.context, username)

        extracted_texts = []

        for post in profile.get_posts():
            print(f"Processing post: {post.shortcode}")

            # Download the post's image to a temporary directory
            self.loader.download_post(post, target='temp')

            # Find the downloaded image file
            image_files = glob.glob(f'temp/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC*.jpg')

            if not image_files:
                print(f"No image found for post {post.shortcode}.")
                continue

            image_path = image_files[0]

            # Extract text from the image
            extracted_text_lines = extract_text_from_image(image_path)
            extracted_texts.append(extracted_text_lines)

        return extracted_texts
