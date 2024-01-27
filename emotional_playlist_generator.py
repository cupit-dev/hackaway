from openai import OpenAI
import time
import openai

class EmotionalPlaylistGenerator:
    def __init__(self):
        self.client = OpenAI()
        self.last_request_time = None
        self.request_interval = 1  # seconds between requests

        # Dictionary of Spotify parameters with descriptions
        self.spotify_parameters = {
            "target_valence": "a happiness score from 0 to 1, where higher values represent more positive mood",
            "target_danceability": "a score from 0 to 1 of how danceable the user is feeling, with higher scores indicating a greater desire to dance"
            # Add more parameters and their descriptions here in the future
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
        except openai.Error as e:  # Catching the general OpenAI error
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

    def get_music_parameters(self, emotion_summary):
        # Dynamically create the system prompt using the parameter dictionary
        parameter_descriptions = ", ".join([f"{param}, which is {desc}" for param, desc in self.spotify_parameters.items()])
        system_prompt = f"Your goal is to convert a description of a person’s emotional state into key parameters: {parameter_descriptions}. Output just these metrics based on their emotional state. Provide your response in the format: '" + ", ".join([f"{param} = [score]" for param in self.spotify_parameters.keys()]) + "', with no other text."

        completion = self._make_request([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": emotion_summary}
        ])

        if completion:
            return completion.choices[0].message.content
        else:
            return "Error: Unable to get music parameters."

# # Usage
# generator = EmotionalPlaylistGenerator()
# emotion_summary = generator.analyse_emotion("Spent the afternoon reorganizing my bookshelf and dusting off old photo albums.")
# music_parameters = generator.get_music_parameters(emotion_summary)
# print(music_parameters)
