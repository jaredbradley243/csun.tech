/* eslint-disable no-underscore-dangle */
import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import "./SeniorDesignTable.css";

export default function SeniorDesignTable(props) {
  const { projects, openProjectModal, openProfessorModal } = props;
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);

  // Color set for mobile-project-header
  const colorSet = ["#73BBC9", "#4942E4", "#374259", "#DEA704"];

  function pickColor(index) {
    const colorIndex = index % 4;
    return colorSet[colorIndex];
  }

  function handleScreenWidth() {
    setScreenWidth(window.innerWidth);
  }

  useEffect(() => {
    window.addEventListener("resize", handleScreenWidth);
    return () => {
      window.removeEventListener("resize", handleScreenWidth);
    };
  }, []);

  // Desktop Table-Version
  if (screenWidth >= 700) {
    return (
      <div className="designTable">
        <div className="designTable_cell designTable_header">Join Project</div>
        <div className="designTable_cell designTable_header">Project Name</div>
        <div className="designTable_cell designTable_header">Professor</div>
        <div className="designTable_cell designTable_header">Open Slots</div>
        <div className="designTable_cell designTable_header">Meeting Times</div>

        {projects.map((project) => (
          <React.Fragment key={project._id}>
            <div className="designTable_cell">
              <button type="button" className="designTable_joinBtn">
                Join
              </button>
            </div>
            <button
              id={project._id}
              type="button"
              className="designTable_cell designTable_btn"
              onClick={openProjectModal}
            >
              {project.name}
            </button>
            <button
              type="button"
              className="designTable_cell designTable_btn"
              data-professor-name={project.professor}
              onClick={openProfessorModal}
            >
              {project.professor}
            </button>
            <div
              className={
                project.openSpots <= 5
                  ? "designTable_cell designTable_redAlert"
                  : "designTable_cell"
              }
            >
              {project.openSpots}
            </div>
            <div className="designTable_cell">{project.meetingTimes}</div>
          </React.Fragment>
        ))}
      </div>
    );
  }

  // Mobile Table-Version
  return (
    <div className="designTable">
      {projects.map((project, index) => (
        <div className="designTable_project" key={project._id}>
          <div className="designTable_gridContainer">
            <div className="designTable_firstColumn">
              <div
                className="designTable_cell designTable_header"
                style={{ backgroundColor: pickColor(index) }}
              >
                Project Name
              </div>
              <div className="designTable_cell">Professor</div>
              <div className="designTable_cell">Open Slots</div>
              <div className="designTable_cell">Meeting Times</div>
            </div>
            <div className="designTable_secondColumn">
              <button
                id={project._id}
                type="button"
                className="designTable_cell designTable_btn designTable_header"
                onClick={openProjectModal}
                style={{ backgroundColor: pickColor(index) }}
              >
                {project.name}
              </button>
              <button
                type="button"
                className="designTable_cell designTable_btn"
                data-professor-name={project.professor}
                onClick={openProfessorModal}
              >
                {project.professor}
              </button>
              <div
                className={
                  project.openSpots <= 5
                    ? "designTable_cell designTable_redAlert"
                    : "designTable_cell"
                }
              >
                {project.openSpots}
              </div>
              <div className="designTable_cell">{project.meetingTimes}</div>
            </div>
          </div>
          <button
            className="designTable_joinBtn"
            style={{ backgroundColor: pickColor(index) }}
            type="button"
          >
            Join {project.name}
          </button>
        </div>
      ))}
    </div>
  );
}

SeniorDesignTable.propTypes = {
  projects: PropTypes.arrayOf(
    PropTypes.shape({
      _id: PropTypes.number.isRequired,
    })
  ).isRequired,
  openProjectModal: PropTypes.func.isRequired,
  openProfessorModal: PropTypes.func.isRequired,
};
