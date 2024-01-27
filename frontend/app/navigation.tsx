// Navigation.js

import React from 'react';
import './Navigation.css'; // Importing the CSS file for styling

function Navigation() {
    return (
        <nav className="navbar">
            <a href="/" className="nav-link1">MoodTune</a>
            <a href="/trends" className="nav-link2">Trends</a>
            {/* <a href="/contact" className="nav-link">Contact</a> */}
        </nav>
    );
}

export default Navigation;
