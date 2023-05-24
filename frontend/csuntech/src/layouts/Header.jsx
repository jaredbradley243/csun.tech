import React from "react";
import PropTypes from "prop-types";
import Navbar from "../components/Navbar";
import "./Header.css";
import lunaLogo from "../images/luna-logo.png";

export default function Header(props) {
  const { isDarkMode, toggleDarkMode } = props;
  return (
    <header>
      <a href="/" aria-label="LunaTech Logo" className="header_logoContainer">
        <img src={lunaLogo} className="header_lunaLogo" alt="LunaTech Logo" />
      </a>
      <Navbar isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
    </header>
  );
}

Header.propTypes = {
  isDarkMode: PropTypes.bool.isRequired,
  toggleDarkMode: PropTypes.func.isRequired,
};
