"use client"; // Add this line to mark this component as a Client Component

// Importing modules
import React, { useState, useEffect } from "react";
// import "./App.css";
import Navigation from "./navigation";
import trackCover from "./images/mockPlaylist1.webp";
import playlistCover from "./images/playlistCover2.jpeg";
import plus from "./images/plus.png";
import saveLogo from "./images/saveLogo.png";
import micIcon from "./images/micButton.png";

import Image from "next/image";
import { Fascinate_Inline } from "next/font/google";
function App() {
  // usestate for setting a javascript
  // object for storing and using data
  const [inputValue, setInputValue] = useState(""); // State to hold the input value
  const [checkboxValue, setCheckboxValue] = useState("");
  const [loading, setLoading] = useState(false);
  const backend_url = "http://localhost:5001";

  const [data, setdata] = useState({
    summary: "",
    title: "",
    uuid: "",
    artwork: "", //base64 encoded jpg
    tracks: [
      {
        name: "",
        album: {
          images: [
            {
              height: "",
              width: "",
              url: "",
            },
          ],
        },
        external_urls: {
          spotify: ''
        },
        artists: [
          {
            name: "",
          },
        ],
      },
    ],
  });

  // Function to handle input changes and update state
  const handleInputChange = (e: any) => {
    setInputValue(e.target.value);
  };

  const handleCheckboxChange = (e: any) => {
    setCheckboxValue(e.target.checked);
  };

  // Function to trigger upload of playlist to Spotify
  const handleUploadPlaylist = (uuid: any) => {
    fetch(backend_url + "/playlist/" + uuid + "/upload");
    alert("Playlist has been added to your Spotify!");
  };

  // Function to handle form submission
  const handleSubmit = async (e: any) => {
    e.preventDefault(); // Prevent default form submission behavior
    try {
      setLoading(true)
      const response = await fetch(backend_url + "/new_playlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: inputValue,
          generate_artwork: checkboxValue,
        }), // Send the state value as JSON
      });
      setLoading(false)
      if (response.ok) {
        // Handle successful submission here
        const jsonResponse = await response.json();
        console.log("Response from Flask:", jsonResponse);

        var tracks: any[] = [];
        var artists: any[] = [];

        Object.keys(jsonResponse.tracks).forEach(function (key) {
          tracks.push(jsonResponse.tracks[key]);
          // artists.push((jsonResponse.tracks[key])[artists[0]])

          console.log("UUID:", jsonResponse.tracks[key]);
        });

        setdata({
          summary: jsonResponse.summary,
          title: jsonResponse.title,
          uuid: jsonResponse.uuid,
          artwork: jsonResponse.artwork,
          tracks: tracks,
        });
      } else {
        // Handle errors here
        console.error("Failed to send data to Flask");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <Navigation /> {/* Include the Navigation component */}
        <main
          style={{ marginTop: "50px" }}
          className="flex min-h-screen flex-col items-center p-24"
        >
          <p style={{ fontSize: "xx-large", fontStyle: "bold" }}>
            How are you feeling today?{" "}
          </p>
          <form style={{ width: "100%" }} onSubmit={handleSubmit}>
            <div>
              <input
                style={{
                  color: "black",
                  width: "65%",
                  padding: "0.5rem 0.8rem 0.5rem 0.8rem",
                  marginTop: "30px",
                  border: "0",
                  borderRadius: "5px",
                  fontSize: "20px",
                  height: "97px",
                }}
                className="child"
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                placeholder="Enter your thoughts ..."
              />
              <button
                className="child2 group rounded-lg border border-transparent px-5 py-4 transition-colors hover:bg-gray-100 hover:dark:bg-neutral-800/30"
                type="submit"
                style={{ marginTop: "18px", marginLeft: "10px" }}
                disabled={loading}
              >
                <Image src={micIcon} alt="Logo" width={80} height={80} />
              </button>
              <button
                style={{ marginLeft: "10px", marginTop: "23px" }}
                className="child group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                type="submit"
                disabled={loading}
              >
                <p style={{ fontWeight: "bold", paddingBottom: "5px" }}>
                  Create Playlist{" "}
                  <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                    -&gt;
                  </span>
                </p>
                <p
                  className={`m-0 max-w-[30ch] text-sm opacity-50 text-balance`}
                >
                  Create a Spotify playlist based off of your current mood.
                </p>
              </button>
            </div>
            <input
              className="messageCheckbox scale-[1.75] mx-1 my-3"
              type="checkbox"
              name="generateArtwork"
              value={checkboxValue}
              onChange={handleCheckboxChange}
            ></input>
            <label htmlFor="generateArtwork" className="ml-2 font-semibold">
              Generate cover art (this can be slow!)
            </label>
          </form>

          <p className="playlistTitle" hidden={!loading}>Now generating...</p>
        
          <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-full sm:before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-full sm:after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]"></div>

          { data.summary ? <div className="playlistContainer">
            <Image
              className="child2"
              src={
                data.artwork
                  ? "data:image/jpeg;base64," + data.artwork
                  : playlistCover
              }
              alt="Logo"
              width={100}
              height={100}
              style={{ marginRight: "12px" }}
            />

            <div className="child2" style={{ width: '80%'}}>
              <p className="playlistTitle">{data.title}</p>
              <p className="playlistDescription">{data.summary}</p>
            </div>
            <button
              style={{ float: "right" }}
              className="child2 group rounded-lg border border-transparent px-5 py-4 transition-colors hover:bg-gray-100 hover:dark:bg-neutral-800/30"
              type="submit"
              onClick={() => handleUploadPlaylist(data.uuid)}
            >
              <Image src={saveLogo} alt="Logo" width={100} height={100} />
            </button>
            <br></br>
            <br></br>

            {data.tracks.map((item) => (
              <div className="trackContainer">
                <Image
                  className="child2"
                  src={item.album.images[0].url}
                  alt="Logo"
                  width={50}
                  height={50}
                  style={{marginRight: '8px'}}
                />
                <div className="child2">
                  <a href={item.external_urls.spotify} target="_blank">
                  <p className="hover">
                    <b>{item.name}</b>
                  </p>
                  </a>
                  <p>{item.artists[0].name}</p>
                </div>
              </div>
            ))}
          </div> : null }
        </main>
      </header>
    </div>
  );
}

export default App;
