/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable import/no-extraneous-dependencies */
import React, { useState } from "react";
import { Link } from "react-router-dom";
import "boxicons/css/boxicons.min.css";
import "./Login.css";
import lunaLogo from "../images/luna-logo-alt.png";
import githubLogo from "../images/github-logo.jpg";
import googleLogo from "../images/google-logo.jpg";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showUsernameTitle, setShowUsernameTitle] = useState(false);
  const [showPasswordTitle, setShowPasswordTitle] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  function handleUsername(e) {
    setUsername(e.target.value);
    if (e.target.value.length > 0) setShowUsernameTitle(true);
    else setShowUsernameTitle(false);
  }

  function handlePassword(e) {
    setPassword(e.target.value);
    if (e.target.value.length > 0) setShowPasswordTitle(true);
    else setShowPasswordTitle(false);
  }

  function togglePasswordHide() {
    setShowPassword(!showPassword);
  }

  // Stop the form from submitting.
  // TODO: Change after backend inplemented login url
  function handleSubmit(e) {
    e.preventDefault();
  }

  return (
    <div className="login_container">
      <form className="login_form" onSubmit={handleSubmit}>
        <img className="login_lunaLogo" src={lunaLogo} alt="" />
        <h1>Login</h1>
        <span
          className={
            showUsernameTitle
              ? "login_usernameTitle show"
              : "login_usernameTitle"
          }
        >
          Username
        </span>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={handleUsername}
        />
        <span
          className={
            showPasswordTitle
              ? "login_passwordTitle show"
              : "login_passwordTitle"
          }
        >
          Password
        </span>
        <div className="login_passwordContainer">
          <Link to="#" className="login_forgotPassword login_links">
            Forgot Password?
          </Link>
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={handlePassword}
          />
          <button
            type="button"
            className="login_icon"
            onClick={togglePasswordHide}
          >
            <i className={showPassword ? "bx bx-hide" : "bx bx-show"} />
          </button>
        </div>

        <input type="submit" value="Log In" />
        <p>
          Don&apos;t have an account?{" "}
          <Link to="#" className="login_links">
            SignUp Here.
          </Link>
        </p>
        <div className="login_divider">
          <span className="login_line" />
          <span>or</span>
          <span className="login_line" />
        </div>
        <div className="login_socialButtonContainer">
          <button type="button" className="login_socialButton">
            <div>
              <img src={githubLogo} alt="" />
              Github
            </div>
          </button>
          <button type="button" className="login_socialButton">
            <div>
              <img src={googleLogo} alt="" />
              Google
            </div>
          </button>
        </div>
      </form>
    </div>
  );
}
