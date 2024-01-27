"use client"; // Add this line to mark this component as a Client Component

// Importing modules
import React, { useState, useEffect } from "react";
// import "./App.css";
import Navigation from "./navigation";
import trackCover from "./images/mockPlaylist1.webp";
import playlistCover from "./images/playlistCover2.jpeg";
import plus from "./images/plus.png";

import Image from "next/image";
function App() {
  // usestate for setting a javascript
  // object for storing and using data
  const [inputValue, setInputValue] = useState(""); // State to hold the input value

  // const [data, setdata] = useState({
  // 	name: "",
  // 	age: 0,
  // 	date: "",
  // 	programming: "",
  // });

  const [data, setdata] = useState({
    description: "",
    title: "",
    tracks: [
      {
        artists: [],
        title: "",
        track_id: "",
      },
    ],
  });

  // Function to handle input changes and update state
  const handleInputChange = (e: any) => {
    setInputValue(e.target.value);
  };

  // Function to handle form submission
  const handleSubmit = async (e: any) => {
    e.preventDefault(); // Prevent default form submission behavior
    try {
      const response = await fetch("http://localhost:5000/feeling", {
        // Replace with your Flask endpoint
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: inputValue }), // Send the state value as JSON
      });
      if (response.ok) {
        // Handle successful submission here
        const jsonResponse = await response.json();
        console.log("Response from Flask:", jsonResponse);
      } else {
        // Handle errors here
        console.error("Failed to send data to Flask");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  // Using useEffect for single rendering
  // useEffect(() => {
  //   fetch('http://localhost:5000/data')
  //   .then((res) =>
  // 		res.json().then((data) => {
  // 			// Setting a data from api
  // 			setdata({
  // 				name: data.Name,
  // 				age: data.Age,
  // 				date: data.Date,
  // 				programming: data.programming,
  // 			});
  // 		})
  // 	);
  // }, []);

  useEffect(() => {
    fetch("http://localhost:5000/playlist").then((res) =>
      res.json().then((data) => {
        var arr: any[] = [];
        Object.keys(data.tracks).forEach(function (key) {
          arr.push(data.tracks[key]);
        });
        // Setting a data from api
        setdata({
          description: data.description,
          title: data.title,
          tracks: arr,
        });

        // var json = {"active":{"label":"Active","value":"12"},"automatic":{"label":"Automatic","value":"8"},"waiting":{"label":"Waiting","value":"1"},"manual":{"label":"Manual","value":"3"}};
      })
    );
  }, []);

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
                  width: "75%",
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
                style={{ marginLeft: "10px", marginTop: "23px" }}
                className="child group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                type="submit"
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
          </form>

          <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-full sm:before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-full sm:after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]"></div>

          <div className="playlistContainer">
            <Image
              className="child2"
              src={playlistCover}
              alt="Logo"
              width={100}
              height={100}
              style={{ marginRight: "10px" }}
            />

            <div className="child2">
              <p className="playlistTitle">{data.title}</p>

              <p className="playlistDescription">{data.description}</p>
            </div>
            <button
                style={{ float: "right"}}
                className="child2 group rounded-lg border border-transparent px-5 py-4 transition-colors hover:bg-gray-100 hover:dark:bg-neutral-800/30"
                type="submit"
              >
                <Image
                
                src={plus}
                alt="Logo"
                width={100}
                height={100}
              />
              </button>
            <br></br>
            {data.tracks.map((item) => (
              <div className="trackContainer">
                <Image
                  className="child2"
                  src={trackCover}
                  alt="Logo"
                  width={50}
                  height={50}
                />

                <p className="child2">{item.title}</p>
              </div>
            ))}
          </div>
        </main>
      </header>
    </div>
  );
}

export default App;
