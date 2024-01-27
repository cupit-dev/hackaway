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
            "target_danceability": "a score from 0 to 1 of how danceable the user is feeling, with higher scores indicating a greater desire to dance",
            "target_energy": "a measure from 0 to 1 of the intensity and activity of the music, where higher values represent more energetic tracks",
            # "target_tempo": "the speed of the track measured in Beats Per Minute (BPM), where higher values represent faster tempo",
            "min_acousticness": "a measure from 0 to 1 of the likelihood a track is acoustic, with higher values representing more acoustic (less electronic) sounds",
            # More parameters can be added here
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



# # Usage
# generator = EmotionalPlaylistGenerator()
# emotion_summary = generator.analyse_emotion("Spent the afternoon reorganizing my bookshelf and dusting off old photo albums.")
# music_parameters = generator.get_music_parameters(emotion_summary)
# print(music_parameters)
