/* eslint-disable no-underscore-dangle */
import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import "./EditProjectModal.css";

export default function EditProjectModal(props) {
  const {
    projectId,
    currProjectToEdit,
    setCurrProjectToEdit,
    closeEditProjectModal,
  } = props;
  const [project, setProject] = useState(null);

  useEffect(() => {
    if (currProjectToEdit === null) {
      // Prefill the edit modal with default values if there's no data
      setProject({ name: "", capacity: 1, skills: "", meetingSchedule: "" });
    } else {
      // Convert project's skills property from array to string
      const tempProject = { ...currProjectToEdit };
      tempProject.skills = tempProject.skills.join(", ");
      setProject(tempProject);
    }
  }, []);

  // eslint-disable-next-line no-unused-vars
  function saveEditedProject(e) {
    // const projectId = e.target.getAttribute("data-project-id");
    // edited project is in currProjectToEdit
    // TODO: Send new project's data to backend to save
  }

  function handleEditProjectName(e) {
    const tempProject = { ...currProjectToEdit };
    tempProject.name = e.target.value;
    setCurrProjectToEdit(tempProject);
  }

  function handleEditProjectCapacity(e) {
    const tempProject = { ...currProjectToEdit };
    tempProject.capacity = e.target.value;
    setCurrProjectToEdit(tempProject);
  }

  function handleEditProjectSkills(e) {
    // convert s from string to array before saving
    let skills = e.target.value.split(",");
    skills = skills.map((skill) => skill.trim());

    const tempProject = { ...currProjectToEdit };
    tempProject.skills = skills;
    setCurrProjectToEdit(tempProject);
  }

  // TODO: Use React Timepicker and Weekpicker
  function handleEditProjectMeetingSchedule(e) {
    const tempProject = { ...currProjectToEdit };
    tempProject.meetingSchedule = e.target.value;
    setCurrProjectToEdit(tempProject);
  }

  // Only return one modal at a time
  if (projectId !== currProjectToEdit._id || project === null) return null;

  return (
    <form className="editProjectModal">
      <h3>Edit Project</h3>
      <label htmlFor="edit-project-name">
        <div>Project Name:</div>
        <input
          id="edit-project-name"
          type="text"
          onChange={handleEditProjectName}
          value={project.name}
        />
      </label>
      <label htmlFor="edit-project-capacity">
        <div>Capacity:</div>
        <input
          id="edit-project-capacity"
          type="text"
          onChange={handleEditProjectCapacity}
          value={project.capacity}
        />
      </label>
      <label htmlFor="edit-project-necessary-skills">
        <div>Skills:</div>
        <textarea
          id="edit-project-necessary-skills"
          onChange={handleEditProjectSkills}
          value={project.skills}
        />
      </label>
      <label htmlFor="edit-project-meeting-schedules">
        <div>Meeting Schedules:</div>
        <input
          id="edit-project-meeting-schedules"
          type="text"
          onChange={handleEditProjectMeetingSchedule}
          value={project.meetingSchedule}
        />
      </label>
      <div className="editProjectModal_btnContainer">
        <button
          type="button"
          className="editProjectModal_editCancelBtn"
          onClick={closeEditProjectModal}
        >
          Cancel
        </button>
        <button
          type="button"
          className="editProjectModal_editSaveBtn"
          onClick={saveEditedProject}
        >
          Save
        </button>
      </div>
    </form>
  );
}

EditProjectModal.propTypes = {
  projectId: PropTypes.number.isRequired,
  currProjectToEdit: PropTypes.shape({
    _id: PropTypes.number,
    name: PropTypes.string,
    capacity: PropTypes.number,
    skills: PropTypes.arrayOf(PropTypes.string),
    meetingSchedule: PropTypes.string,
  }),
  setCurrProjectToEdit: PropTypes.func.isRequired,
  closeEditProjectModal: PropTypes.func.isRequired,
};

EditProjectModal.defaultProps = {
  currProjectToEdit: null,
};
