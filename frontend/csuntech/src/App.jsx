import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Login from "./pages/Login";
import ErrorPage from "./pages/ErrorPage";
import Signup from "./pages/Signup";
import HomePage from "./pages/HomePage";
import Header from "./layouts/Header";

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

  return (
    <div className="App">
      <Header isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
      <Routes>
        <Route exact path="/" element={<HomePage isDarkMode={isDarkMode} />} />
        <Route path="/login" element={<Login isDarkMode={isDarkMode} />} />
        <Route path="/signup" element={<Signup isDarkMode={isDarkMode} />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </div>
  );
}

export default App;
