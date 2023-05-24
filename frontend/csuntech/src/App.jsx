import React, { useState } from "react";
import "./App.css";
import HomePage from "./pages/HomePage";

function App() {
  //  Pass down the isDarkMode variable to the components
  //  that needs to access it
  const [isDarkMode, setIsDarkMode] = useState(
    localStorage.getItem("isDarkMode") === "true"
  );

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    localStorage.setItem("isDarkMode", !isDarkMode);
  };

  return <HomePage isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />;
}

export default App;
