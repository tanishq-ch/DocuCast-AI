# import os
# import torch
# from pydub import AudioSegment
# import soundfile as sf  # KittenTTS requires soundfile to save output
# from kittentts import KittenTTS

# # --- Model Loading (Singleton Pattern) ---
# tts_model = None

# def get_tts_model():
#     """Initializes and returns the KittenTTS model, loading it if not already in memory."""
#     # FIX IS ON THE NEXT LINE
#     global tts_model
#     if tts_model is None:
#         print("--- LOADING KittenTTS MODEL INTO MEMORY (this will be quick) ---")
#         try:
#             # Initialize the model as per the official documentation
#             # This will automatically download the small model file on first run.
#             tts_model = KittenTTS("KittenML/kitten-tts-nano-0.2")
#             print("--- KittenTTS MODEL LOADED SUCCESSFULLY ---")
#         except Exception as e:
#             print(f"!!! FAILED TO LOAD KittenTTS MODEL: {e} !!!")
#             raise e
#     return tts_model

# def generate_audio_from_script(script_text, output_path):
#     """
#     Converts a formatted script into a multi-speaker MP3 audio file using
#     the lightweight KittenTTS model.
#     """
#     print(f"--- INITIATING KittenTTS AUDIO GENERATION for {os.path.basename(output_path)} ---")
    
#     try:
#         model = get_tts_model()
        
#         # --- Define the built-in speaker voices to use ---
#         # As per the README, these are the available voice names.
#         HOST_VOICE = "expr-voice-2-f"    # A female voice
#         EXPERT_VOICE = "expr-voice-2-m"   # A male voice

#         temp_dir = "temp_audio_clips"
#         os.makedirs(temp_dir, exist_ok=True)

#         lines = script_text.strip().split('\n')
#         generated_clips = []

#         for i, line in enumerate(lines):
#             line = line.strip()
#             if not line:
#                 continue

#             voice = None
#             text_to_speak = ""

#             if line.lower().startswith("host:"):
#                 voice = HOST_VOICE
#                 text_to_speak = line[5:].strip()
#             elif line.lower().startswith("expert:"):
#                 voice = EXPERT_VOICE
#                 text_to_speak = line[7:].strip()
#             else:
#                 continue

#             if not text_to_speak:
#                 continue

#             clip_path = os.path.join(temp_dir, f"clip_{i}.wav")
#             print(f"Generating clip {i} for voice '{voice}'...")
            
#             # --- Core KittenTTS function calls ---
#             # 1. Generate the audio data (numpy array)
#             audio_data = model.generate(text_to_speak, voice=voice)
            
#             # 2. Save the audio data to a file using soundfile
#             # Note: KittenTTS uses a sample rate of 24000
#             sf.write(clip_path, audio_data, 24000)
            
#             generated_clips.append(clip_path)

#         # Stitch the clips together using pydub
#         print("--- Stitching audio clips together... ---")
#         final_podcast = AudioSegment.silent(duration=500)

#         for clip_path in generated_clips:
#             segment = AudioSegment.from_wav(clip_path)
#             final_podcast += segment
#             final_podcast += AudioSegment.silent(duration=750)
        
#         print(f"--- Exporting final MP3 to {output_path} ---")
#         final_podcast.export(output_path, format="mp3")

#         # --- Cleanup ---
#         print("--- Cleaning up temporary files... ---")
#         for clip_path in generated_clips:
#             os.remove(clip_path)
#         os.rmdir(temp_dir)
        
#         print(f"--- AUDIO GENERATION SUCCESSFUL for {os.path.basename(output_path)} ---")
#         return True

#     except Exception as e:
#         print(f"!!! AUDIO GENERATION FAILED: {e} !!!")
#         if 'temp_dir' in locals() and os.path.exists(temp_dir):
#             for f in os.listdir(temp_dir):
#                 os.remove(os.path.join(temp_dir, f))
#             os.rmdir(temp_dir)
#         return False


import os
import torch
from pydub import AudioSegment
import soundfile as sf
from kittentts import KittenTTS
import nltk # --- NEW: Import the Natural Language Toolkit

# Download the sentence tokenizer data if it doesn't exist
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    print("--- First time setup: Downloading NLTK sentence tokenizer data ('punkt') ---")
    nltk.download('punkt')

# --- Model Loading (Singleton Pattern) ---
tts_model = None

def get_tts_model():
    """Initializes and returns the KittenTTS model, loading it if not already in memory."""
    global tts_model
    if tts_model is None:
        print("--- LOADING KittenTTS MODEL INTO MEMORY (this will be quick) ---")
        try:
            tts_model = KittenTTS("KittenML/kitten-tts-nano-0.2")
            print("--- KittenTTS MODEL LOADED SUCCESSFULLY ---")
        except Exception as e:
            print(f"!!! FAILED TO LOAD KittenTTS MODEL: {e} !!!")
            raise e
    return tts_model

def generate_audio_from_script(script_text, output_path):
    """
    Converts a formatted script into a multi-speaker MP3 audio file using
    the lightweight KittenTTS model with sentence splitting for robustness.
    """
    print(f"--- INITIATING KittenTTS AUDIO GENERATION for {os.path.basename(output_path)} ---")
    
    try:
        model = get_tts_model()
        
        HOST_VOICE = "expr-voice-2-f"
        EXPERT_VOICE = "expr-voice-2-m"

        temp_dir = "temp_audio_clips"
        os.makedirs(temp_dir, exist_ok=True)

        lines = script_text.strip().split('\n')
        generated_clips = []
        clip_counter = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            voice = None
            text_to_process = ""

            if line.lower().startswith("host:"):
                voice = HOST_VOICE
                text_to_process = line[5:].strip()
            elif line.lower().startswith("expert:"):
                voice = EXPERT_VOICE
                text_to_process = line[7:].strip()
            else:
                continue

            if not text_to_process:
                continue
            
            # --- NEW: Split the paragraph into individual sentences ---
            sentences = nltk.sent_tokenize(text_to_process)
            
            # --- NEW: Loop through each sentence and generate a clip ---
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue

                clip_path = os.path.join(temp_dir, f"clip_{clip_counter}.wav")
                print(f"Generating clip {clip_counter} for voice '{voice}'...")
                
                audio_data = model.generate(sentence, voice=voice)
                sf.write(clip_path, audio_data, 24000)
                
                generated_clips.append(clip_path)
                clip_counter += 1

        print("--- Stitching audio clips together... ---")
        final_podcast = AudioSegment.silent(duration=500)

        for clip_path in generated_clips:
            segment = AudioSegment.from_wav(clip_path)
            final_podcast += segment
            # Use a slightly shorter pause after each sentence
            final_podcast += AudioSegment.silent(duration=400) 
        
        print(f"--- Exporting final MP3 to {output_path} ---")
        final_podcast.export(output_path, format="mp3")

        print("--- Cleaning up temporary files... ---")
        for clip_path in generated_clips:
            os.remove(clip_path)
        os.rmdir(temp_dir)
        
        print(f"--- AUDIO GENERATION SUCCESSFUL for {os.path.basename(output_path)} ---")
        return True

    except Exception as e:
        print(f"!!! AUDIO GENERATION FAILED: {e} !!!")
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)
        return False