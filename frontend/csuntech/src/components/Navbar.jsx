/* eslint-disable react/button-has-type */
/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import PropTypes from "prop-types";
import "./Navbar.css";

export default function Navbar(props) {
  // Change isLoggedIn to true when user is logged in
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const { isDarkMode, toggleDarkMode } = props;

  // Function that return log in / log out btn depending on user's status
  function authButtons() {
    if (isLoggedIn)
      return (
        <li>
          <button className="navbar_btn navbar_icon" aria-label="Log Out">
            <i className="fa-solid fa-right-from-bracket" />
          </button>
        </li>
      );
    return (
      <li>
        <button className="navbar_btn navbar_icon" aria-label="Log In">
          <i className="fa-solid fa-right-to-bracket" />
        </button>
      </li>
    );
  }

  return (
    <nav>
      <ul className="navbar">
        {/* Home Button */}
        <li>
          <a href="/" className="navbar_icon">
            <i className="fa-solid fa-house" />
          </a>
        </li>

        {/* Show user icon if logged in */}
        {isLoggedIn && (
          <li>
            <a href="/setting" className="navbar_icon">
              <i className="fa-solid fa-user" />
            </a>
          </li>
        )}

        {/* Light/Dark Mode button */}
        <li>
          <button
            className="navbar_btn navbar_icon"
            onClick={toggleDarkMode}
            aria-label={
              isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"
            }
          >
            <i
              className={isDarkMode ? "fa-solid fa-sun" : "fa-solid fa-moon"}
            />
          </button>
        </li>

        {/* Log In / Log Out button */}
        {authButtons()}
      </ul>
    </nav>
  );
}

Navbar.propTypes = {
  isDarkMode: PropTypes.bool.isRequired,
  toggleDarkMode: PropTypes.func.isRequired,
};
