/* eslint-disable prettier/prettier */
import React, { useState } from 'react';
import './DayPicker.css';

const daysOfTheWeek = [
    {
        key: 'Sunday',
        label: 'Sun',
    },
    {
        key: 'Monday',
        label: 'Mon',
    },
    {
        key: 'Tuesday',
        label: 'Tue',
    },
    {
        key: 'Wednesday',
        label: 'Wed',
    },
    {
        key: 'Thursday',
        label: 'Thu',
    },
    {
        key: 'Friday',
        label: 'Fri',
    },
    {
        key: 'Saturday',
        label: 'Sat',
    },
];

function DayPicker() {
    const [days, setDays] = useState([]);

    const handleChange = (day) => {
        if (days.includes(day)) {
            setDays(days.filter((selected) => selected !== day));
        } else {
            setDays([...days, day]);
        }
    };

    return (
        <div className="dayPicker_dayContainer">
            {daysOfTheWeek.map((day) => (
                <div
                    className={
                        days.includes(day)
                            ? 'dayPicker_dayTrue'
                            : 'dayPicker_day'
                    }
                >
                    <input
                        type="checkbox"
                        id={day.key}
                        className="dayPicker_btnCheckbox"
                        name={day.key}
                        checked={days.includes(day)}
                        onChange={() => handleChange(day)}
                    />
                    <label htmlFor={day.key} className="dayPicker_btnLabel">
                        <span className="dayPicker_btnText">{day.label}</span>
                    </label>
                </div>
            ))}
        </div>
    );
}

export default DayPicker;
