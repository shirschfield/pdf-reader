import tkinter as tk
from tkinter import filedialog
import threading
import PyPDF2
from gtts import gTTS
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    print(f"Warning: Empty content on page {reader.pages.index(page)}")
            return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

# Function to convert text to speech
def text_to_speech(text, lang='en'):
    try:
        # Define the folder path for saving the MP3 file
        folder_path = '/Users/sarah.w.hirschfield/projects/repos/pdf-reader'
        output_file = os.path.join(folder_path, "output.mp3")
        
        tts = gTTS(text=text, lang=lang)
        tts.save(output_file)
        print(f"Saved speech to {output_file}, now playing...")
        os.system(f"afplay {output_file}")
        print("Playback finished.")
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

# Function to handle PDF reading in a separate thread
def read_pdf(file_path):
    print("Reading PDF:", file_path)
    pdf_text = extract_text_from_pdf(file_path)

    if pdf_text:
        # Define the size of each text chunk
        chunk_size = 5000

        # Break the text into smaller chunks
        chunks = [pdf_text[i:i + chunk_size] for i in range(0, len(pdf_text), chunk_size)]

        for index, chunk in enumerate(chunks):
            print(f"Starting text-to-speech for chunk {index + 1}/{len(chunks)}...")
            text_to_speech(chunk)
            print(f"Chunk {index + 1} playback finished.")
    else:
        print("No text extracted from PDF.")

# Function to open and read a PDF file
def open_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        print(f"File selected: {file_path}")
        thread = threading.Thread(target=read_pdf, args=(file_path,))
        thread.start()
    else:
        print("No file selected.")

# Create the main window
root = tk.Tk()
root.title("PDF Reader App")
root.geometry("400x200")

# Add a button to open PDF
open_button = tk.Button(root, text="Open PDF", command=open_pdf_file)
open_button.pack(pady=20)

# Run the application
root.mainloop()
