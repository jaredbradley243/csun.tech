/* eslint-disable no-underscore-dangle */
import React from "react";
import PropTypes from "prop-types";
import "./SeniorDesignTable.css";

export default function SeniorDesignTable(props) {
  const { projects, openProjectModal, openProfessorModal } = props;
  return (
    <div className="designTable">
      <div className="designTable_cell designTable_Header">Project Name</div>
      <div className="designTable_cell designTable_Header">Professor Name</div>
      <div className="designTable_cell designTable_Header">Open Slots</div>
      <div className="designTable_cell designTable_Header">Meeting Times</div>

      {projects.map((project) => (
        <React.Fragment key={project._id}>
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
              project.openSpots < 5
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

SeniorDesignTable.propTypes = {
  projects: PropTypes.arrayOf(
    PropTypes.shape({
      _id: PropTypes.number.isRequired,
    })
  ).isRequired,
  openProjectModal: PropTypes.func.isRequired,
  openProfessorModal: PropTypes.func.isRequired,
};
