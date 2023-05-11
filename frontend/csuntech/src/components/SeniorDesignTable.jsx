/* eslint-disable react/button-has-type */
import React from "react";
import "./SeniorDesignTable.css";

export default function SeniorDesignTable() {
  return (
    <div className="designTable">
      <div className="designTable_cell designTable_Header">Project Name</div>
      <div className="designTable_cell designTable_Header">Professor Name</div>
      <div className="designTable_cell designTable_Header">Open Slots</div>
      <div className="designTable_cell designTable_Header">Meeting Times</div>

      <button className="designTable_cell designTable_btn">E-Commerce</button>
      <div className="designTable_cell">John Doe</div>
      <div className="designTable_cell">14</div>
      <div className="designTable_cell">2-4pm</div>

      <button className="designTable_cell designTable_btn">E-Commerce</button>
      <div className="designTable_cell">John Doe</div>
      <div className="designTable_cell">14</div>
      <div className="designTable_cell">2-4pm</div>

      <button className="designTable_cell designTable_btn">E-Commerce</button>
      <div className="designTable_cell">John Doe</div>
      <div className="designTable_cell">14</div>
      <div className="designTable_cell">2-4pm</div>

      <button className="designTable_cell designTable_btn">E-Commerce</button>
      <div className="designTable_cell">John Doe</div>
      <div className="designTable_cell">14</div>
      <div className="designTable_cell">2-4pm</div>

      <button className="designTable_cell designTable_btn">E-Commerce</button>
      <div className="designTable_cell">John Doe</div>
      <div className="designTable_cell">14</div>
      <div className="designTable_cell">2-4pm</div>
    </div>
  );
}
