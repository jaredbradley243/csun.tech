/* eslint-disable no-underscore-dangle */
import React, { useState } from "react";
import SeniorDesignTable from "../components/SeniorDesignTable";
import "./HomePage.css";
import ProjectModal from "../components/ProjectModal";
import ProfessorModal from "../components/ProfessorModal";
import Footer from "../layouts/Footer";

export default function HomePage() {
  // the current project saved in this prop will be opened in the project Modal
  // setting it to null will close the Modal
  const [projectToOpen, setProjectToOpen] = useState(null);
  // Projects Mock Data from Backend
  const projects = [
    {
      _id: 1,
      name: "Project1",
      professor: "professor1",
      openSpots: 10,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 2,
      name: "Project2",
      professor: "professor2",
      openSpots: 4,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 3,
      name: "Project3",
      professor: "professor3",
      openSpots: 16,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 4,
      name: "Project4",
      professor: "professor4",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
  ];
  // the current professor in this prop will be opened in the porfessor Modal
  const [professorToOpen, setProfessorToOpen] = useState(null);
  // Professor Mock Data from Backend
  const professors = [
    {
      _id: 1,
      name: "professor1",
      email: "sample@gmail.com",
      photoURL: "/samplePhoto.jpg",
      rateMyProfessorURL: "sample.com",
      csunPage: "sample.com",
    },
    {
      _id: 2,
      name: "professor2",
      email: "sample@gmail.com",
      photoURL: "/samplePhoto.jpg",
      rateMyProfessorURL: "sample.com",
      csunPage: "sample.com",
    },
    {
      _id: 3,
      name: "professor3",
      email: "sample@gmail.com",
      photoURL: "/samplePhoto.jpg",
      rateMyProfessorURL: "sample.com",
      csunPage: "sample.com",
    },
    {
      _id: 4,
      name: "professor4",
      email: "sample@gmail.com",
      photoURL: "/samplePhoto.jpg",
      rateMyProfessorURL: "sample.com",
      csunPage: "sample.com",
    },
  ];

  const closeProjectModal = () => {
    setProjectToOpen(null);
  };

  const closeProfessorModal = () => {
    setProfessorToOpen(null);
  };

  const openProjectModal = (e) => {
    // eslint-disable-next-line radix
    const projectId = parseInt(e.target.id);
    const project = projects.find((p) => p._id === projectId);
    setProjectToOpen(project);
  };

  const openProfessorModal = (e) => {
    const professorName = e.target.getAttribute("data-professor-name");
    const professor = professors.find((p) => p.name === professorName);
    setProfessorToOpen(professor);
  };

  return (
    <div className="homePage_container">
      <div className="designTable_container">
        <SeniorDesignTable
          projects={projects}
          openProjectModal={openProjectModal}
          openProfessorModal={openProfessorModal}
        />
      </div>
      {projectToOpen && (
        <ProjectModal
          project={projectToOpen}
          closeProjectModal={closeProjectModal}
        />
      )}
      {professorToOpen && (
        <ProfessorModal
          professor={professorToOpen}
          closeProfessorModal={closeProfessorModal}
        />
      )}
      <Footer />
    </div>
  );
}
