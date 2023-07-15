/* eslint-disable no-use-before-define */
/* eslint-disable no-underscore-dangle */
import React, { useState, useEffect, useRef } from "react";
import SeniorDesignTable from "../components/SeniorDesignTable";
import "./HomePage.css";
import ProjectModal from "../components/ProjectModal";
import ProfessorModal from "../components/ProfessorModal";
import Footer from "../layouts/Footer";
import {
  computeProjectsInCurrPage,
  computeTotalPages,
  makePageBtnActive,
  generatePageBtns,
} from "../utils/paginationFunc";

export default function HomePage() {
  // the current project saved in this prop will be opened in the project Modal
  // setting it to null will close the Modal
  const [projectToOpen, setProjectToOpen] = useState(null);
  // the current professor in this prop will be opened in the porfessor Modal
  const [professorToOpen, setProfessorToOpen] = useState(null);
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);
  const currPage = useRef(1);
  const [totalPages, setTotalPages] = useState(0);
  const [projectsInCurrPage, setProjectsInCurrPage] = useState([]);
  const [pageBtns, setPageBtns] = useState([]);
  const pageBtnContainer = useRef();
  // Change this number to increase or decrease the num of projects displayed per page
  const projectPerPage = 6;
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
      openSpots: 5,
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
    {
      _id: 5,
      name: "Project5",
      professor: "professor5",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 6,
      name: "Project6",
      professor: "professor6",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 7,
      name: "Project7",
      professor: "professor7",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 8,
      name: "Project8",
      professor: "professor8",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 9,
      name: "Project9",
      professor: "professor9",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 10,
      name: "Project10",
      professor: "professor10",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 11,
      name: "Project11",
      professor: "professor11",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 12,
      name: "Project12",
      professor: "professor12",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 13,
      name: "Project13",
      professor: "professor13",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 14,
      name: "Project14",
      professor: "professor14",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 15,
      name: "Project15",
      professor: "professor15",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 16,
      name: "Project16",
      professor: "professor16",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 17,
      name: "Project17",
      professor: "professor17",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 18,
      name: "Project18",
      professor: "professor18",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 19,
      name: "Project19",
      professor: "professor19",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 20,
      name: "Project20",
      professor: "professor20",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 21,
      name: "Project21",
      professor: "professor21",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 22,
      name: "Project22",
      professor: "professor22",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 23,
      name: "Project23",
      professor: "professor23",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 24,
      name: "Project24",
      professor: "professor24",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 25,
      name: "Project25",
      professor: "professor25",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 26,
      name: "Project26",
      professor: "professor26",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 27,
      name: "Project27",
      professor: "professor27",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 28,
      name: "Project28",
      professor: "professor28",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 29,
      name: "Project29",
      professor: "professor29",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 30,
      name: "Project30",
      professor: "professor30",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
    {
      _id: 31,
      name: "Project31",
      professor: "professor31",
      openSpots: 3,
      totalSpots: 30,
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, modi. Adconsequatur facere sed!",
      skills: ["HTML", "CSS", "Javascript"],
      meetingTimes: "Tue, Wed 2-4pm",
    },
  ];
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
    const projectId = parseInt(e.target.id, 10);
    const project = projects.find((p) => p._id === projectId);
    setProjectToOpen(project);
  };

  const openProfessorModal = (e) => {
    const professorName = e.target.getAttribute("data-professor-name");
    const professor = professors.find((p) => p.name === professorName);
    setProfessorToOpen(professor);
  };

  function handleScreenWidth() {
    setScreenWidth(window.innerWidth);
  }

  // TODO: Use media query instead of listening for resize event
  useEffect(() => {
    window.addEventListener("resize", handleScreenWidth);
    return () => {
      window.removeEventListener("resize", handleScreenWidth);
    };
  }, []);

  useEffect(() => {
    const pages = computeTotalPages(projects.length, projectPerPage);
    setTotalPages(pages);
    const list = computeProjectsInCurrPage(
      projects,
      currPage.current,
      projectPerPage
    );
    setProjectsInCurrPage(list);
  }, []);

  useEffect(() => {
    makePageBtnActive(pageBtnContainer, currPage.current);
  }, [pageBtns]);

  useEffect(() => {
    const buttons = generatePageBtns(totalPages, currPage.current, changePage);
    setPageBtns(buttons);
  }, [totalPages]);

  function changePage(e) {
    const page = e.target.getAttribute("data-btn-value");
    if (
      (page === "prev" && currPage.current === 1) ||
      (page === "next" && currPage.current === totalPages)
    )
      return;
    if (page === "prev") currPage.current -= 1;
    else if (page === "next") currPage.current += 1;
    else currPage.current = parseInt(page, 10);
    const list = computeProjectsInCurrPage(
      projects,
      currPage.current,
      projectPerPage
    );
    setProjectsInCurrPage(list);
    const buttons = generatePageBtns(totalPages, currPage.current, changePage);
    setPageBtns(buttons);
  }

  return (
    <div className="homePage_container">
      <div className="designTable_container">
        <SeniorDesignTable
          projects={projectsInCurrPage}
          openProjectModal={openProjectModal}
          openProfessorModal={openProfessorModal}
        />
      </div>
      <div className="homePage_pagination" ref={pageBtnContainer}>
        {screenWidth > 400 && (
          <button data-btn-value="prev" type="button" onClick={changePage}>
            &laquo;
          </button>
        )}
        {pageBtns}
        {screenWidth > 400 && (
          <button data-btn-value="next" type="button" onClick={changePage}>
            &raquo;
          </button>
        )}
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
