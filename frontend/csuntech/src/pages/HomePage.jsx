import React from "react";
import PropTypes from "prop-types";
import SeniorDesignTable from "../components/SeniorDesignTable";
import "./HomePage.css";
// TODO: Remove header import - Jared
// import Header from "../layouts/Header";
import Footer from "../layouts/Footer";

export default function HomePage(props) {
  const { isDarkMode } = props;
  return (
    <div
      className={
        isDarkMode ? "homePage_container darkMode" : "homePage_container"
      }
    >
      {/* // TODO: Remove Header. It will be used across the app in App.jsx */}
      {/* <Header isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} /> */}
      <div className="designTable_container">
        <SeniorDesignTable />
      </div>
      <Footer />
    </div>
  );
}

HomePage.propTypes = {
  isDarkMode: PropTypes.bool.isRequired,
  // TODO: Remove toggle - Jared
  // toggleDarkMode: PropTypes.func.isRequired,
};
