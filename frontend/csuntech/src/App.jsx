import React from "react";
import { Routes, Route } from 'react-router-dom';
import "./App.css";
import Navbar from "./components/Navbar";
import Login from './pages/Login'
import ErrorPage from "./pages/ErrorPage"
import Signup from "./pages/Signup"
import Home from "./pages/Home"


function App() {
  return (
    <div className="App">
          <Navbar/>
      <Routes>
            <Route exact path="/" element={<Home />} />
            <Route
              path="/login"
              element={ <Login />}
            />
            <Route
              path="/signup"
              element={ <Signup />}
            />
            <Route path="*" element={<ErrorPage />} />
      </Routes>
    </div>
  );
}

export default App;
