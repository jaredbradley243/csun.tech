import React, { useEffect } from "react";
import PropTypes from "prop-types";
import "./EditProjectModal.css";

export default function EditProjectModal(props) {
  const { currProjectToEdit, setCurrProjectToEdit, closeEditProjectModal } =
    props;

  function closeModalWithEsc(e) {
    if (e.key === "Escape") closeEditProjectModal();
  }

  function closeModalWithOutsideClick(e) {
    if (e.target.id === "edit-project-modal-wrapper") closeEditProjectModal();
  }

  useEffect(() => {
    document.addEventListener("keyup", closeModalWithEsc);
    document.addEventListener("click", closeModalWithOutsideClick);
    return () => {
      document.removeEventListener("keyup", closeModalWithEsc);
      document.removeEventListener("click", closeModalWithOutsideClick);
    };
  }, []);

  // eslint-disable-next-line no-unused-vars
  function saveEditedProject(e) {
    // const projectId = e.target.getAttribute("data-project-id");
    // edited project is in currProjectToEdit
    // TODO: Send new project's data to backend to save
    closeEditProjectModal();
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

  return (
    <div className="editProjectModalWrapper" id="edit-project-modal-wrapper">
      <form className="editProjectModal">
        <h3>Edit Project</h3>
        <label htmlFor="edit-project-name">
          <div>Project Name:</div>
          <input
            id="edit-project-name"
            type="text"
            onChange={handleEditProjectName}
            value={currProjectToEdit.name}
          />
        </label>
        <label htmlFor="edit-project-capacity">
          <div>Capacity:</div>
          <input
            id="edit-project-capacity"
            type="text"
            onChange={handleEditProjectCapacity}
            value={currProjectToEdit.capacity}
          />
        </label>
        <label htmlFor="edit-project-necessary-skills">
          <div>Skills:</div>
          <textarea
            id="edit-project-necessary-skills"
            onChange={handleEditProjectSkills}
            value={currProjectToEdit.skills.join(", ")}
          />
        </label>
        <label htmlFor="edit-project-meeting-schedules">
          <div>Meeting Schedules:</div>
          <input
            id="edit-project-meeting-schedules"
            type="text"
            onChange={handleEditProjectMeetingSchedule}
            value={currProjectToEdit.meetingSchedule}
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
    </div>
  );
}

EditProjectModal.propTypes = {
  currProjectToEdit: PropTypes.shape({
    name: PropTypes.string.isRequired,
    openSpots: PropTypes.number.isRequired,
    capacity: PropTypes.number.isRequired,
    description: PropTypes.string.isRequired,
    skills: PropTypes.arrayOf(PropTypes.string).isRequired,
    meetingSchedule: PropTypes.string.isRequired,
  }).isRequired,
  setCurrProjectToEdit: PropTypes.func.isRequired,
  closeEditProjectModal: PropTypes.func.isRequired,
};
