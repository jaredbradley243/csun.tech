import React, { useState } from "react";
import "./TimePicker.css";

export default function TimePicker() {
  const [hour, setHour] = useState("00");
  const [min, setMin] = useState("00");
  const [meridiem, setMeridiem] = useState("AM");

  function handleHourChange(e) {
    const userInput = e.target.value;

    // Ensure hour is <= 12
    let inputHour = parseInt(userInput, 10);
    if (inputHour > 12) {
      inputHour %= 10;
    }
    if (inputHour < 10) {
      inputHour = `0${inputHour}`;
    }
    setHour(inputHour);
  }

  function handleMinChange(e) {
    const userInput = e.target.value;

    // Ensure min is <= 59
    let inputMin = parseInt(userInput, 10);
    if (inputMin > 59) {
      inputMin %= 10;
    }
    if (inputMin < 10) {
      inputMin = `0${inputMin}`;
    }
    setMin(inputMin);
  }

  function handleMeridiemChange(e) {
    if (e.target.id === "AM") setMeridiem("AM");
    else setMeridiem("PM");
  }

  return (
    <div className="timePicker_container">
      <p>Enter Time</p>
      <div className="timePicker">
        <label htmlFor="hour" className="timePicker_hourLabel">
          <input
            type="text"
            className="timePicker_hour"
            value={hour}
            onChange={handleHourChange}
          />
        </label>
        <div className="timePicker_dot">
          <span />
          <span />
        </div>
        <label htmlFor="minute" className="timePicker_minLabel">
          <input
            type="text"
            className="timePicker_min"
            value={min}
            onChange={handleMinChange}
          />
        </label>
        <div className="timePicker_meridiem">
          <button
            type="button"
            id="AM"
            className={meridiem === "AM" ? "active" : ""}
            onClick={handleMeridiemChange}
          >
            AM
          </button>
          <button
            type="button"
            id="PM"
            className={meridiem === "PM" ? "active" : ""}
            onClick={handleMeridiemChange}
          >
            PM
          </button>
        </div>
      </div>
      <button type="button">OK</button>
    </div>
  );
}
