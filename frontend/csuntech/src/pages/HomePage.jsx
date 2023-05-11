import React from "react";
import PropTypes from "prop-types";
import SeniorDesignTable from "../components/SeniorDesignTable";
import "./HomePage.css";
import Header from "../layouts/Header";
import Footer from "../layouts/Footer";

export default function HomePage(props) {
  const { isDarkMode, toggleDarkMode } = props;
  return (
    <div
      className={
        isDarkMode ? "homePage_container darkMode" : "homePage_container"
      }
    >
      <Header isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
      <div className="designTable_container">
        <SeniorDesignTable />
      </div>
      <Footer />
    </div>
  );
}

HomePage.propTypes = {
  isDarkMode: PropTypes.bool.isRequired,
  toggleDarkMode: PropTypes.func.isRequired,
};
