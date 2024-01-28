# %%
import os
import yaml

if not os.path.isfile('./secrets.yaml'):
    print('No secrets file - aborting')
    exit(1)

with open("./secrets.yaml", "r") as f:
    try:
        data = yaml.safe_load(f)
        spotify_auth = data['spotify']
        openai_key = data['openai']['secret']
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

# %%
journal_entries = [
    "I had an awful day at work. I want to cry.",
    "Managed to catch the sunset after a long day at work. It was quite a view.",
    "I spent the evening browsing through some old recipes. Might try cooking something new this weekend.",
    "It's been raining all day, and the sound of raindrops is kind of soothing.",
    "Another routine day, nothing much to report.",
    "Had an interesting chat with an old friend, brought back lots of memories.",
    "The coffee shop was unusually crowded today, had to wait a long time for my order.",
    "Woke up feeling refreshed after a good night's sleep. Ready to tackle the day ahead.",
    "Spent some quality time with my family this evening. It's moments like these that I cherish.",
    "Had a challenging workout session today, but feeling energized and accomplished.",
    "Got caught in a downpour on my way home, but it somehow lifted my spirits.",
    "Tried a new restaurant for lunch; the food was amazing and I'll definitely be going back.",
    "My garden is blooming, and it's such a delight to see all the colors.",
    "Finished a book I've been reading for a while. It left me with a lot to ponder.",
    "Watched an old movie that I used to love. It brought back a wave of nostalgia.",
    "The city was buzzing with energy today, made me feel more alive.",
    "Had a deep conversation with my colleague. It's nice to connect on a personal level.",
]

# journal_entries = [
    # "@FoodieFran: Made my first homemade sourdough bread today! It's not perfect, but the smell in my kitchen is amazing. 🍞 #BakingAdventures",
    # "@NatureLoverNick: Caught the sunrise on my morning hike. There's nothing like the peace of the great outdoors. 🌅 #HikingDiaries",
    # "@BookwormBeth: Finished reading 'The Labyrinth of Spirits' last night. What a breathtaking story! Any recommendations for my next read? 📚 #BookLover",
    # "@FitnessFreakFiona: Hit a new personal best in my half marathon training today! Feeling unstoppable. 💪 #MarathonTraining #HealthyLiving",
    # "@ArtisticAlex: Spent the weekend experimenting with watercolors. Not my usual medium, but loving the process of learning something new. 🎨 #ArtJourney",
    # "@GadgetGeekGary: Just got the latest smartwatch. Time to test out all these features they claim to have! #TechTrends",
    # "@TravelTalesTina: Just booked my flight to Japan! Can't wait to explore the culture and cuisine. ✈️🌏 #Wanderlust #TravelDiaries",
    # "@GreenThumbGina: My garden is finally starting to bloom! There's something so rewarding about growing your own food. 🌱 #GardeningLife",
    # "@ComedyKingCarl: Why don't scientists trust atoms? Because they make up everything! 😂 #DadJokes #ComedyGold"
# ]


# %%
# # Import the class from the file
# from emotional_playlist_generator import EmotionalPlaylistGenerator

# # Create an instance of the class
# generator = EmotionalPlaylistGenerator()

# # Process each journal entry
# for entry in journal_entries:
#     emotion_summary = generator.analyse_emotion(entry)
#     music_parameters = generator.get_music_parameters(emotion_summary)
#     emotion_metric = generator.get_emotions(generator.emotions, entry)
    
#     print(f"Journal Entry: {entry}")
#     print(f"Emotion Summary: {emotion_summary}\n")
#     print(f"Music Parameters: \n{music_parameters}\n")
#     print(f"Emotion metric: \n{emotion_metric}\n")


# %%
# Import the class from the file
import datetime
from emotional_playlist_generator import EmotionalPlaylistGenerator

# Create an instance of the class
# generator = EmotionalPlaylistGenerator()
generator = EmotionalPlaylistGenerator(api_key=openai_key)

# # Process each journal entry
# for entry in journal_entries:
#     emotion_summary = generator.analyse_emotion(entry)
#     music_parameters = generator.get_music_parameters(emotion_summary)
    
#     print(f"Journal Entry: {entry}")
#     print(f"Emotion Summary: {emotion_summary}\n")
#     print(f"Music Parameters: \n{music_parameters}\n")

#     # Process each emotion for the journal entry
#     print("Emotion metrics:")
#     for emotion in generator.emotions:
#         emotion_metric = generator.get_emotions(emotion, entry)
#         print(f"{emotion}: {emotion_metric}")
#     print("\n")

# %%
# from emotional_playlist_generator import EmotionalPlaylistGenerator

# # Create an instance of the class
# generator = EmotionalPlaylistGenerator(api_key="your-openai-api-key")  # Make sure to pass the correct API key

# journal_entries = [
#     "I had an awful day at work. I want to cry.",
#     # ... [other journal entries]
# ]

# Dictionary to store the emotion metrics
emotion_metrics_over_time = {}

# Start date for the entries (for example, a week ago)
start_date = datetime.datetime.now() - datetime.timedelta(days=len(journal_entries))

# Process each journal entry
for i, entry in enumerate(journal_entries):
    # Create a dummy date for the entry
    entry_date = start_date + datetime.timedelta(days=i)
    date_str = entry_date.strftime("%Y-%m-%d")

    emotion_summary = generator.analyse_emotion(entry)
    music_parameters = generator.get_music_parameters(emotion_summary)

    # print(f"Date: {date_str}")
    # print(f"Journal Entry: {entry}")
    # print(f"Emotion Summary: {emotion_summary}\n")
    # print(f"Music Parameters: \n{music_parameters}\n")

    # Process each emotion for the journal entry
    emotion_metrics = {}
    for emotion in generator.emotions:
        emotion_metric = generator.get_emotions(emotion, entry)
        emotion_metrics[emotion] = emotion_metric
    #     print(f"{emotion}: {emotion_metric}")
    # print("\n")

    # Store the emotion metrics for this date
    emotion_metrics_over_time[date_str] = emotion_metrics

# Print the emotion metrics dictionary to check its contents
# print("Emotion Metrics Over Time:")
# for date, metrics in emotion_metrics_over_time.items():
    # print(f"{date}: {metrics}")


# %%
import pickle

with open('toms_test2.pkl', 'wb') as file:
    pickle.dump(emotion_metrics_over_time, file)




