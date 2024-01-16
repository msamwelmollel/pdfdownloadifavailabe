# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 19:18:27 2024

@author: msamwelmollel
"""

import requests
from bs4 import BeautifulSoup
import os

def find_pdf_links(url):
    # Send a request to the URL
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <a> tags
    a_tags = soup.find_all('a')
    
    # Filter out links to PDF files
    pdf_links = [link.get('href') for link in a_tags if link.get('href') and link.get('href').endswith('.pdf')]
    return pdf_links

def download_files(base_url, links):
    for link in links:
        # Create the full URL to download
        full_url = base_url + link if not link.startswith('http') else link
        # Get the file name
        file_name = os.path.basename(full_url)
        # Send a request to download the file
        response = requests.get(full_url)
        # Save the file
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded {file_name}')

# The base URL of the website (change this to the website you're interested in)
base_url = 'https://www.ppra.go.tz/publications/tanzania-procurement-journal?page=3'

# Find PDF links on the website
pdf_links = find_pdf_links(base_url)

# Download the PDF files
download_files(base_url, pdf_links)
