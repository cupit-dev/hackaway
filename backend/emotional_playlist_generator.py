from openai import OpenAI
import time
import openai
import os

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

        self.emotions = [
            "Anxiety", 
            "Gratitude",
            "Pessimism",
            "Contentment",
            "Positivity",
        ]

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
        except Exception as e:  # Catching general exceptions
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
            {"role": "system", "content": "You are a sentiment analysis assistant. Your purpose is to provide a short, two-sentence summary of how a user is feeling/their current emotional state based on an input of their journal entry or random thoughts they have."},
            {"role": "user", "content": journal_entry}
        ])

        if completion:
            return completion.choices[0].message.content
        else:
            return "Error: Unable to analyse emotion."

    def get_music_parameters(self, emotion_summary):
        # Dynamically create a list of parameter names for the prompt
        parameter_names = ", ".join(self.spotify_parameters.keys())

        # Construct the prompt dynamically
        system_prompt = f"Based on the emotional state: '{emotion_summary}', please provide values for the following Spotify parameters: {parameter_names}. Format your response as 'parameter = score' TO 2 decimal places for each."
        # system_prompt = f"Based on the emotional state: '{emotion_summary}', please provide a one word description of the emotional state of the user."

        completion = self._make_request([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Provide a value for the parameter."}
            # {"role": "user", "content": "Provide description of emotional state of user."}
        ])

        if completion:
            return completion.choices[0].message.content
        else:
            return "Error: Unable to get music parameters."

    def get_emotions(self, emotion, journal_entry):
        # Construct the prompt dynamically
        # system_prompt = f"Based on the emotional state: '{emotion_summary}', please provide values for the following Spotify parameters: {parameter_names}. Format your response as 'parameter = score' TO 2 decimal places for each."
        system_prompt = f"You are a sentiment analysis assistant. You will always output a metric. Your purpose is to understand the emotional state of the user and quantify their mood with respect to the following metric: {emotion}. Here is the user's input: {journal_entry}. This should be scored from 0 to 100, with 0 meaning the user is displaying no signs of {emotion} and 100 meaning the user is displaying maximum {emotion}. If you are unsure or there is not enough information, provide your best guess, or provide a neutral score of 50. Your answer should be in the format 'parameter = score'. You must be able to do this even for very short or difficult to judge inputs. Do not refuse to provide a metric."

        completion = self._make_request([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Provide a value for the emotion metric."}
            # {"role": "user", "content": "Provide description of emotional state of user."}
        ])

        if completion:
            return completion.choices[0].message.content
        else:
            return "Error: Unable to get emotion metric."


# # Usage
# generator = EmotionalPlaylistGenerator()
# emotion_summary = generator.analyse_emotion("Spent the afternoon reorganizing my bookshelf and dusting off old photo albums.")
# music_parameters = generator.get_music_parameters(emotion_summary)
# print(music_parameters)


#take journal entry, output about 4 emotion metrics