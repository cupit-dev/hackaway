# Sentiment - Royal Hackaway v7

Throw your thoughts and feelings into Sentiment, and it'll spit out a personalised playlist based on your mood and listening habits. Using the power of GPT4 for sentiment analysis, the Spotify Recommendations API for musical knowledge, and DALL-E 3 for pretty pictures, Sentiment always knows exactly what you need to hear. 

Furthermore, Sentiment also keeps track of your journal entries, and leverages the wonderful Taipy framework to provide a fascinating and easy-to-digest statistical insight into how your mood changes over time.


## Installation and usage
Notes:
 - Everything you need to run Sentiment is in the `frontend` folder - any other random scripts are historical artefacts and can be safely ignored. Yes the repo is a mess - all part of the charm.
 - There'll be a script to simplify this at some point, maybe...

### Manual
You will need recent versions of NodeJS and Python installed to run Sentiment.

 1. Create a new Spotify application following the instructions at https://developer.spotify.com/documentation/web-api
 2. Sign up for an OpenAI developer account (https://platform.openai.com/docs/overview), and add some credit (you don't need much!)
 3. Create a new file `frontend/flask/secrets.yaml`, and populate it with your API keys as shown:
	```yaml
	---
	spotify:
	    client_id: XXXXXXXXXXXXXXXXXXXXXXXXXX
	    secret: XXXXXXXXXXXXXXXXXXXXXXXXXX
	openai:
	    secret: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	 ```

4. Create a Python virtual environment, install the requirements, and launch the server:
	```bash
	# In frontend/flask
	$ python -m venv venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt
	$ python main.py
	```
	You may be greeted with a pop-up browser requesting you sign in to Spotify, and authorise access to your acccount - you'll want to go ahead and do that.
5. Install the requirements for the UI, then launch that too
	```bash
	# In the frontend folder
	$ npm install
	$ npm run dev
	```
6. Navigate to http://localhost:3000 in your browser, and you're good to go!