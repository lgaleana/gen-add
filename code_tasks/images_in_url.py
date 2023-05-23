"""
ChatGPT-4 prompt: write a python function that given an url returns all images in the website
"""

import requests
from bs4 import BeautifulSoup

def get_images_from_url(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find all image tags
        images = soup.find_all('img')

        # Create a list to store the URLs of the images
        image_urls = []

        # For each image tag, get the URL of the image
        for image in images:
            # If the tag has the 'src' attribute
            if image.has_attr('src'):
                image_url = image['src']
                
                # If URL is relative, convert it to absolute
                if image_url.startswith('/'):
                    image_url = url + image_url

                image_urls.append(image_url)

        return image_urls

    # If the GET request is not successful, return None
    else:
        return None