import React, { useState } from "react";
import TimeKeeper from "react-timekeeper";

export default function Test() {
  const [time, setTime] = useState("12:00pm");
  const [isClockShown, setIsClockShown] = useState(true);

  const handleTimeChange = (e) => {
    setTime(e.formatted12);
  };

  const handleHideClock = () => {
    setIsClockShown(false);
  };

  const handleShowClock = () => {
    setIsClockShown(true);
  };

  return (
    <>
      {isClockShown && (
        <div>
          <TimeKeeper
            time={time}
            onChange={handleTimeChange}
            onDoneClick={handleHideClock}
            coarseMinutes={5}
            forceCoarseMinutes
            switchToMinuteOnHourSelect
            switchToMinuteOnHourDropdownSelect
          />
        </div>
      )}
      <button type="button" onClick={handleShowClock}>
        Show Clock
      </button>
      <div>Current time: {time}</div>
    </>
  );
}
