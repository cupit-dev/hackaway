import json
from openai import OpenAI
import time
import openai
import os
from PIL import Image
from io import BytesIO
import base64

class EmotionalPlaylistGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=(api_key if api_key else os.environ['OPENAI_API_KEY']))
        self.last_request_time = None
        self.request_interval = 1  # seconds between requests

        # Dictionary of Spotify parameters with descriptions
        self.spotify_parameters = {
            "target_valence": "a happiness score from 0 to 1, where higher values represent more positive mood",
            "target_danceability": "a score from 0 to 1 of how danceable the user is feeling, with higher scores indicating a greater desire to dance",
            "target_energy": "a measure from 0 to 1 of the intensity and activity of the music, where higher values represent more energetic tracks",
            "target_acousticness": "a measure from 0 to 1 of the likelihood a track is acoustic, with higher values representing more acoustic sounds",
            "target_instrumentalness": "a measure from 0 to 1 indicating the extent to which a track contains no vocals, with higher values representing more instrumental tracks",
            "target_liveness": "a score from 0 to 1 indicating the presence of an audience in the recording, where higher values represent more live-sounding tracks",
            "target_speechiness": "a measure from 0 to 1 indicating the presence of spoken words in a track, with higher values representing more speech-like tracks",
            "target_tempo": "the speed of the track measured in Beats Per Minute (BPM), where higher values represent faster tempo",
        }

    def _rate_limit_check(self):
        if self.last_request_time is not None:
            elapsed_time = time.time() - self.last_request_time
            if elapsed_time < self.request_interval:
                time.sleep(self.request_interval - elapsed_time)
        self.last_request_time = time.time()

    def _make_request(self, messages):
        try:
            self._rate_limit_check()
            return self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            # return self.client.chat.completions.create(model="gpt-4", messages=messages)
        except openai.Error as e:  # Catching the general OpenAI error
            print(f"An error occurred: {e}")
            return None
    
    def transcribe_audio(self, audio_file_path):
        if not os.path.exists(audio_file_path):
            return "Error: Audio file not found."

        with open(audio_file_path, "rb") as audio_file:
            try:
                self._rate_limit_check()
                response = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )

                # Accessing the transcribed text correctly
                if hasattr(response, 'text'):
                    return response.text
                else:
                    return "Error: Transcription text not found in the response."

            except Exception as e:  # Catching general exceptions
                print(f"An error occurred: {e}")
                return None
        

    def analyse_emotion(self, journal_entry):
        completion = self._make_request([
            {"role": "system", "content": "You are a sentiment analysis assistant. Your purpose is to provide a short, two-sentence summary of how a user is feeling/their current emotional state based on an input of their journal entry or social media post."},
            {"role": "user", "content": journal_entry}
        ])

        if completion:
            return completion.choices[0].message.content
        else:
            return "Error: Unable to analyse emotion."
        
    def playlist_description_generator(self, journal_entry):
        completion = self._make_request([
            {"role": "system", "content": f"AI Summary Bot, your task is to create a Spotify playlist description based on a user's journal entry. Analyse the emotional nuances within the journal to understand the user's current mood. Your goal is to craft a short, emotive summary that encapsulates the mood of the music and connects deeply with the feelings expressed in the journal. The summary should be concise - no more than one sentence - capturing the essence of the playlist in a way that resonates with the user's emotional state as revealed in their journal. Output nothing but the playlist summary. User’s journal entry: {journal_entry}"},
            {"role": "user", "content": journal_entry}
        ])

        if completion:
            return completion.choices[0].message.content
        else:
            return "Error: Unable to provide playlist description."

    def get_music_parameters(self, emotion_summary):
        # Dynamically create a list of parameter names for the prompt
        parameter_names = ", ".join(self.spotify_parameters.keys())

        # Construct the prompt dynamically
        system_prompt = f"Based on the emotional state: '{emotion_summary}', please provide values for the following Spotify parameters: {parameter_names}. Format your response as 'parameter = score' TO 2 decimal places for each."
        # system_prompt = f"Based on the emotional state: '{emotion_summary}', please provide a one word description of the emotional state of the user."

        completion = self._make_request([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Provide values for the parameters."}
            # {"role": "user", "content": "Provide description of emotional state of user."}
        ])

        if completion:
            return completion.choices[0].message.content
        else:
            return "Error: Unable to get music parameters."

    def get_playlist_name(self, message):
        # Generate a title for the playlist
        system_prompt = f"You are a playlist title generating bot - given a journal entry summarising a user's day or feelings, generate a short title for a Spotify playlist inspired by their current mood. Exclude any punctuation."
        completion = self._make_request([
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': message}
        ])
        if completion:
            return completion.choices[0].message.content
        else:
            return "My playlist"

    def get_playlist_cover(self, message):
        prompt = "Generate an album cover for an album designed to reflect a user's mood. Avoid adding text, and show just the art itself as if it was ready to be printed. Make it as relevant as possible to the following prompt, with specific details where possible: "
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt + message,
            size="1024x1024",
            quality="standard",
            response_format='b64_json',
            n=1
        )
        raw = response.data[0].b64_json
        ###### DALLE is expensive, develop with this mess
        # raw = {'data': response.data[0].b64_json}
        # with open('data.json', 'w', encoding='utf-8') as f:
        #     json.dump(raw, f, ensure_ascii=False, indent=4)
        # with open('data.json', 'r', encoding='utf-8') as f:
        #     raw = json.load(f)['data']
        im = Image.open(BytesIO(base64.b64decode(raw)))
        im = im.resize((400, 400))
        buff = BytesIO()
        im.save(buff, format="JPEG", optimize=True)
        # with open('out.json', 'w', encoding='utf-8') as f:
        #     json.dump(base64.b64encode(buff.getvalue()).decode(), f, ensure_ascii=False, indent=4)
        return base64.b64encode(buff.getvalue()).decode()
        

# # Usage
# generator = EmotionalPlaylistGenerator()
# emotion_summary = generator.analyse_emotion("Spent the afternoon reorganizing my bookshelf and dusting off old photo albums.")
# music_parameters = generator.get_music_parameters(emotion_summary)
# print(music_parameters)
