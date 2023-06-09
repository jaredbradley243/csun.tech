/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useEffect } from "react";
import PropTypes from "prop-types";
import "./ProfessorModal.css";

export default function ProfessorModal(props) {
  const { professor, closeProfessorModal } = props;

  function closeModalWithEsc(e) {
    if (e.key === "Escape") closeProfessorModal();
  }

  useEffect(() => {
    document.addEventListener("keyup", closeModalWithEsc);
    return () => {
      document.removeEventListener("keyup", closeModalWithEsc);
    };
  }, []);

  function closeModalWithClickOutside(e) {
    if (e.target.id === "professorModal") closeProfessorModal();
  }

  return (
    <div
      id="professorModal"
      className="professorModal"
      onClick={closeModalWithClickOutside}
      tabIndex={0}
    >
      <div className="professorModal_content">
        <button type="button" className="close" onClick={closeProfessorModal}>
          X
        </button>
        <h2>{professor.name}</h2>
        <img src={professor.photoURL} alt="Professor" />
        <p>
          <strong>Email: </strong>
          {professor.email}
        </p>
        <div className="professorModal_linkContainer">
          <a href="#">Rate my professor Link</a>
          <a href="#">CSUN Page</a>
        </div>
      </div>
    </div>
  );
}

ProfessorModal.propTypes = {
  professor: PropTypes.shape({
    name: PropTypes.string.isRequired,
    photoURL: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
  }).isRequired,
  closeProfessorModal: PropTypes.func.isRequired,
};
