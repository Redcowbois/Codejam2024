import fitz
import io
import os
from PIL import Image
import moviepy
from gtts import gTTS


def extract_images_from_pdf(pdf_path, output_folder):
    # Create the output directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        # Iterate through each image
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))

            # Save the image
            image_filename = (
                f"{output_folder}/image_page{page_number+1}_{image_index+1}.{image_ext}"
            )
            image.save(image_filename)
            print(f"Saved image: {image_filename}")


def extract_text_from_pdf(pdf_path, output_text_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Open the output text file
    with open(output_text_file, "wb+", encoding="utf-8") as text_file:
        # Iterate through each page
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            text = page.get_text()

            # Write the text to the file
            text_file.write(f"Page {page_number + 1}\n")
            text_file.write(text)
            text_file.write("\n\n")
            print(f"Extracted text from page {page_number + 1}")


def convert_mp4_to_mp3(mp4_path, mp3_path):
    # Load the video file
    video_clip = moviepy.VideoFileClip(mp4_path)

    # Extract the audio and save it as an MP3 file
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3_path)

    # Close the clips
    audio_clip.close()
    video_clip.close()
    print(f"Converted {mp4_path} to {mp3_path}")


from gtts import gTTS
from pydub import AudioSegment


def text_to_speech(text, accent, lang="en", temp_file="temp.mp3"):
    """
    Converts text to speech and returns an AudioSegment object.
    """
    try:
        # Generate gTTS MP3 audio in memory
        tts = gTTS(text=text, lang=lang, slow=False, tld=accent)
        tts.save(temp_file)
        # Load and speed up the audio (1.3x faster)
        audio = AudioSegment.from_file(temp_file, format="mp3")
        audio = audio.speedup(playback_speed=1.3)
        audio.export(temp_file, format="mp3")
        tts.save(temp_file)
        # Convert the MP3 to an AudioSegment object
        audio_segment = AudioSegment.from_file(temp_file, format="mp3")
        return audio_segment
    finally:
        if os.path.exists(temp_file):
            os.remove(
                temp_file
            )  # Remove the temporary file after loading it into AudioSegment


def podcast(podcast_script, output_podcast_file="final_podcast.mp3"):
    """
    Generates a podcast from a script with accents for different speakers.
    """
    # Split the script into individual lines
    lines = podcast_script.split("\n")

    # Initialize list to store audio segments
    audio_segments = []
    silence = AudioSegment.silent(duration=500)  # 500ms silence

    for i, line in enumerate(lines):
        if not line.strip():  # Skip empty lines
            continue

        # Identify the speaker and assign an accent
        if line.startswith("P1:"):
            accent = "com"  # US English
        elif line.startswith("P2:"):
            accent = "co.uk"  # British English
        else:
            continue

        # Extract the text after "P1:" or "P2:"
        text = line[3:].strip()

        # Generate the audio for this line
        temp_file = f"temp_{i}.mp3"
        line_audio = text_to_speech(text, accent, temp_file=temp_file)

        # Add silence between segments
        audio_segments.append(line_audio)
        audio_segments.append(silence)

    # Concatenate all segments
    podcast_audio = sum(audio_segments, AudioSegment.empty())

    # Export the final combined audio as an MP3 file
    podcast_audio.export(
        output_podcast_file, format="mp3", bitrate="192k", parameters=["-ar", "44100"]
    )
    print(f"Podcast saved as {output_podcast_file}")
