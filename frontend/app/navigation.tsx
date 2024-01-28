// Navigation.js

import React from 'react';
import './navigation.css'; // Importing the CSS file for styling

function Navigation() {
    return (
        <nav className="navbar">
            <a href="/" className="nav-link1">MoodTune</a>
            <a href="/trends" className="nav-link2">Trends</a>
            <a href="/login" className="nav-link-right">Log in to Spotify</a>
        </nav>
    );
}

export default Navigation;
