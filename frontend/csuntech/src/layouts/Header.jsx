/* eslint-disable no-unused-vars */
import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import "./Header.css";
import gsap from "gsap";
import lunaLogo from "../images/luna-logo.png";

export default function Header(props) {
  const { isDarkMode, toggleDarkMode } = props;
  // Change isLoggedIn to true when user is logged in
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [openMobileNav, setOpenMobileNav] = useState(false);
  const tl = useRef(
    gsap
      .timeline({ defaults: { duration: 0.17, ease: "power2.inOut" } })
      .reverse()
  );

  // Function that return log in / log out btn depending on user's status
  function authButtons() {
    if (isLoggedIn)
      return (
        <li>
          <button
            type="button"
            className="navbar_btn navbar_icon"
            aria-label="Log Out"
          >
            <i className="fa-solid fa-right-from-bracket" />
          </button>
        </li>
      );
    return (
      <li>
        <Link
          to="/login"
          type="button"
          className="navbar_btn navbar_icon"
          aria-label="Log In"
        >
          <i className="fa-solid fa-right-to-bracket" />
        </Link>
      </li>
    );
  }

  function handleOpenMobileNav() {
    setOpenMobileNav(!openMobileNav);
  }

  // burger-menu nav animation
  useEffect(() => {
    tl.current
      .to(".bar1", { y: "6px" }, "merge")
      .to(".bar3", { y: "-7px" }, "merge")
      .to(".bar2", { opacity: 0, duration: 0 })
      .to(".bar1", { rotation: "45deg" }, "rotate")
      .to(".bar3", { rotation: "135deg" }, "rotate");
  }, []);

  useEffect(() => {
    tl.current.reversed(!openMobileNav);
  }, [openMobileNav]);

  return (
    <>
      <header>
        <Link
          to="/"
          aria-label="LunaTech Logo"
          className="header_logoContainer"
        >
          <img src={lunaLogo} className="header_lunaLogo" alt="LunaTech Logo" />
        </Link>
        <button
          type="button"
          onClick={handleOpenMobileNav}
          className="navbar_burgerMenu"
        >
          <span className="bar1" />
          <span className="bar2" />
          <span className="bar3" />
        </button>
        <nav className="desktop_nav">
          <ul className="navbar">
            {/* Home Button */}
            <li>
              <Link to="/" className="navbar_icon">
                <i className="fa-solid fa-house" />
              </Link>
            </li>

            {/* Show user icon if logged in */}
            {isLoggedIn && (
              <li>
                <Link to="/setting" className="navbar_icon">
                  <i className="fa-solid fa-user" />
                </Link>
              </li>
            )}

            {/* Light/Dark Mode button */}
            <li>
              <button
                type="button"
                className="navbar_btn navbar_icon"
                onClick={toggleDarkMode}
                aria-label={
                  isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"
                }
              >
                <i
                  className={
                    isDarkMode ? "fa-solid fa-sun" : "fa-solid fa-moon"
                  }
                />
              </button>
            </li>

            {/* Log In / Log Out button */}
            {authButtons()}
          </ul>
        </nav>
      </header>
      <nav className="mobile_nav">
        <ul className={openMobileNav ? "navbar open" : "navbar"}>
          {/* Home Button */}
          <li>
            <Link to="/" className="navbar_icon">
              <i className="fa-solid fa-house" />
            </Link>
          </li>

          {/* Show user icon if logged in */}
          {isLoggedIn && (
            <li>
              <Link to="/setting" className="navbar_icon">
                <i className="fa-solid fa-user" />
              </Link>
            </li>
          )}

          {/* Light/Dark Mode button */}
          <li>
            <button
              type="button"
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
    </>
  );
}

Header.propTypes = {
  isDarkMode: PropTypes.bool.isRequired,
  toggleDarkMode: PropTypes.func.isRequired,
};
