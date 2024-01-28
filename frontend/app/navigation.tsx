// Navigation.js

import React from 'react';
import './navigation.css'; // Importing the CSS file for styling
import sentimentLogo from "./images/sentimentLogo.png";
import Image from "next/image";

function Navigation() {
    return (
        <nav className="navbar">
            <a href="/" style={{marginRight: '10px'}}><Image
                  src={sentimentLogo}
                  alt="Logo"
                  width={50}
                  height={50}
                /></a>
            <a href="/" className="nav-link1">SENTIMENT</a>
            <a href="http://127.0.0.1:5000/" className="nav-link2">Trends</a>
            <a href="/login" className="nav-link-right">Log in to Spotify</a>
        </nav>
    );
}

export default Navigation;
