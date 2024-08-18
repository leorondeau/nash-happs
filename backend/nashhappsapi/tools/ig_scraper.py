import instaloader

def scrape_ig(ig_account):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, ig_account)
    
    posts = []
    for post in profile.get_posts():
        posts.append(post)
        # For now, we're collecting all posts for the agent to check# If you want to limit the number of posts, you can add a condition herereturn posts



# import instaloader
# import pytesseract
# from PIL import Image
# from datetime import datetime, timedelta
# import json
# import re
# import os
# import glob

# # Step 1: Download the latest Instagram post
# L = instaloader.Instaloader()
# username = 'bobbysidlehourtavern'  # replace with the actual Instagram account name
# profile = instaloader.Profile.from_username(L.context, username)

# # Regex pattern to identify date language (e.g., days of the week, times)
# date_language_pattern = re.compile(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|AM|PM|am|pm|o\'clock)\b', re.IGNORECASE)

# # Ensure temp directory exists
# os.makedirs('temp', exist_ok=True)


# # Function to extract text from image and check for date language
# def has_date_language(post):
#     try:
#         # Download the post
#         L.download_post(post, target='temp')
#         # post = (r'/Users/admin/workspace/instascraper/temp/2024-06-10_23-21-14_UTC.jpg')
#         # Find the downloaded image file
#         image_files = glob.glob(f'temp/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC*.jpg')

#         if image_files:
#             image_path = image_files[0]
#             image = Image.open(image_path)
#             text = pytesseract.image_to_string(image)
#         else:
#             print(f"Image for post {post.shortcode} was not found.")
#             return False
#     except Exception as e:
#         print(f"Error processing post {post.shortcode}: {e}")
#         return False

# # Iterate through posts
# for post in profile.get_posts():
#     if has_date_language(post):
#         # Extract post details
#         post_data = {
#             'shortcode': post.shortcode,
#             'date': post.date.strftime('%Y-%m-%d %H:%M:%S'),
#             'caption': post.caption
#         }

#         # Save post details to JSON
#         with open('post_data.json', 'w') as json_file:
#             json.dump(post_data, json_file, indent=4)

#         print(f"Post from {post.date} with shortcode {post.shortcode} saved to JSON.")
#         break  # Stop after finding the post

