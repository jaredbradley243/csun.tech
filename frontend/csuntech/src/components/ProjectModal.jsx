/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable react/no-array-index-key */
import React, { useEffect } from "react";
import PropTypes from "prop-types";
import "./ProjectModal.css";

export default function ProjectModal(props) {
  const { project, closeProjectModal } = props;

  function closeModalWithEsc(e) {
    if (e.key === "Escape") closeProjectModal();
  }

  useEffect(() => {
    document.addEventListener("keyup", closeModalWithEsc);
    return () => {
      document.removeEventListener("keyup", closeModalWithEsc);
    };
  }, []);

  function closeModalWithClickOutside(e) {
    if (e.target.id === "projectModal") closeProjectModal();
  }

  return (
    <div
      id="projectModal"
      className="projectModal"
      onClick={closeModalWithClickOutside}
      tabIndex={0}
    >
      <div className="projectModal_content">
        <button type="button" className="close" onClick={closeProjectModal}>
          X
        </button>
        <h2>{project.name}</h2>
        <p>
          <strong>Professor: </strong>
          {project.professor}
        </p>
        <p className={project.openSpots < 5 ? "redAlert" : ""}>
          <strong>Open Spots: </strong>
          {project.openSpots}
        </p>
        <p>
          <strong>Total Spots: </strong>
          {project.totalSpots}
        </p>
        <h3>Description</h3>
        <p>{project.description}</p>
        <h3>Necessary Skills</h3>
        <ul>
          {project.skills.map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>
        <h3>Meeting Times</h3>
        <p>{project.meetingTimes}</p>
      </div>
    </div>
  );
}

ProjectModal.propTypes = {
  project: PropTypes.shape({
    name: PropTypes.string.isRequired,
    professor: PropTypes.string.isRequired,
    openSpots: PropTypes.number.isRequired,
    totalSpots: PropTypes.number.isRequired,
    description: PropTypes.string.isRequired,
    skills: PropTypes.arrayOf(PropTypes.string).isRequired,
    meetingTimes: PropTypes.string.isRequired,
  }).isRequired,
  closeProjectModal: PropTypes.func.isRequired,
};
