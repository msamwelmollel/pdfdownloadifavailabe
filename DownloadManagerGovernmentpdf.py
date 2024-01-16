# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 19:18:27 2024

@author: msamwelmollel
"""

import tkinter as tk
import requests
from bs4 import BeautifulSoup
import os, sys, subprocess
from tkinter import messagebox
import re
from packaging import version
import webbrowser
from tkinter import ttk
import threading



folder_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'Government Documents')


def check_for_update(current_version):
    try: 
        response = requests.get("https://github.com/msamwelmollel/pdfdownloadifavailabe/releases/latest")
        
        match = re.search(r'/tag/v(\d+\.\d+\.\d+)', response.text)
        if match:
            latest_version = match.group(1)
        else:
            latest_version = "No version found"
        
        if version.parse(latest_version) > version.parse(current_version):
            return latest_version
        return None
    
    except:
        pass
    
def notify_user(new_version):
    # print(new_version)
    def download():
        webbrowser.open(f'https://github.com/msamwelmollel/pdfdownloadifavailabe/releases/download/v{new_version}/PPRA.PDF.Download.Manager.exe')
        
        notification_window.destroy()

    def ignore():
        notification_window.destroy()

    notification_window = tk.Toplevel(root)
    notification_window.title("New Version Available")
    notification_window.geometry("300x150")
    
    tk.Label(notification_window, text=f"Version {new_version} is available for download.", font=("Arial", 10)).pack(pady=10)
    
    tk.Button(notification_window, text="Download", command=download).pack(side=tk.LEFT, padx=20, pady=10)
    tk.Button(notification_window, text="Ignore", command=ignore).pack(side=tk.RIGHT, padx=20, pady=10)

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


def download_files(base_url, links, progress_bar):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    total_files = len(links)
    progress_bar['maximum'] = total_files
    replace_all = False

    for index, link in enumerate(links):
        full_url = base_url + link if not link.startswith('http') else link
        file_name = os.path.basename(full_url)
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path) and not replace_all:
            response = messagebox.askyesnocancel("File Exists", 
                                                 f"The file {file_name} already exists. Replace it?", 
                                                 parent=root)
            if response is None:  # User chose to cancel
                break
            if response:  # User chose Yes
                download_and_save(full_url, file_path)
            elif response is False and index == 0:  # User chose No on the first file
                replace_all_ask = messagebox.askyesno("Replace All", 
                                                      "Do you want to skip all existing files?", 
                                                      parent=root)
                if replace_all_ask:
                    replace_all = True
        else:
            download_and_save(full_url, file_path)

        progress_bar['value'] = index + 1
        root.update_idletasks()

def download_and_save(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print(f'Downloaded {file_path}')
    
    
        
# Functions for each button click
def on_open():
    # #The base URL of the website (change this to the website you're interested in)
    # base_url= address_link.get()
    # # # Find PDF links on the website
    # pdf_links = find_pdf_links(base_url)

    # # # Download the PDF files
    # download_files(base_url, pdf_links, progress)
    # # Implement the action for "Open"
    # print("Open clicked")
    
    base_url = address_link.get()
    pdf_links = find_pdf_links(base_url)
    
    # Start the download process in a new thread
    download_thread = threading.Thread(target=download_files, args=(base_url, pdf_links, progress))
    download_thread.start()

def on_open_with():
    # Implement the action for "Open with..."
    print("Open with... clicked")

def on_open_folder():
    # Implement the action for "Open folder"
    try:
        if sys.platform == "win32":
            os.startfile(folder_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", folder_path])
        else:
            subprocess.run(["xdg-open", folder_path])
        print("Opened folder:", folder_path)
    except Exception as e:
        print(e)

def on_close():
    # Close the application
    print("Close clicked")
    root.destroy()
        

root = tk.Tk()


# app_version.py
APP_VERSION = "1.0.5"
new_version = check_for_update(APP_VERSION)
if new_version:
    root.after(1000, notify_user, new_version)  # Call notify_user after the mainloop starts
    
root.title(f"PPRA PDF Download Manager v{APP_VERSION}")

# Set the default size of the window to 600x400 pixels
root.geometry("460x210")
root.iconbitmap('logo_ppra.ico')



root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Label for the address
address_label = tk.Label(root, text="Address")
address_label.config(font=('Segoe UI', 9))  # 9 is a typical size for interface fonts like Segoe UI
address_label.grid(row=2, column=0, sticky="w")


address_link = tk.Entry(root)
address_link.grid(row=3, column=0, columnspan=3, sticky="we", padx=10,)
address_link.config(font=('Segoe UI', 9))


# Label for the address
address_label = tk.Label(root, text="The file saved in Folder")
address_label.config(font=('Segoe UI', 9))  # 9 is a typical size for interface fonts like Segoe UI
address_label.grid(row=4, column=0, sticky="w")


# Create the Entry widget
output_link = tk.Entry(root)
output_link.grid(row=5, column=0, columnspan=3, sticky="we", padx=10)
output_link.config(font=('Segoe UI', 9))

# Set the default value in the Entry widget
output_link.insert(0, folder_path)

# Set the state to 'readonly' to prevent user from changing the text
output_link.config(state='readonly')



# Buttons
open_button = tk.Button(root, text="Download", command=on_open)
open_button.grid(row=8, column=0, sticky='ew', padx=5, pady=5)

open_folder_button = tk.Button(root, text="Open folder", command=on_open_folder)
open_folder_button.grid(row=8, column=1, sticky='ew', padx=5, pady=5)

close_button = tk.Button(root, text="Close", command=on_close)
close_button.grid(row=8, column=2, sticky='ew', padx=5, pady=5)


# Set up the progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress.grid(row=7, column=0, columnspan=3, sticky='ew', padx=10, pady=5)








# Authorship label
author_label = tk.Label(root, text="© 2024 by Mollel(MasaiiTech - msamwelmollel@gmail.com). All rights reserved.")
author_label.grid(row=10, column=0, columnspan=3, pady=(10, 0))

# Make the grid cells expandable
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)


root.mainloop()
