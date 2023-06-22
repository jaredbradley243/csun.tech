/* eslint-disable no-underscore-dangle */
/* eslint-disable react/no-array-index-key */
/* eslint-disable no-param-reassign */

// TODO: Delete below after implementing all functions
/* eslint-disable no-unused-vars */
import React, { useState, useEffect, useRef } from "react";
import "./ProfessorDashboard.css";

export default function ProfessorDashboard() {
  const [displayedStudents, setDisplayedStudents] = useState([]);
  const [displayedProjects, setDisplayedProjects] = useState([]);
  const [isStudentTable, setIsStudentTable] = useState(true);
  const currSortOrders = useRef({
    studentTable: { column: "name", order: "ascending" },
    projectTable: { column: "name", order: "ascending" },
  });
  const [selectAll, setSelectAll] = useState(false);
  const checkboxes = [];
  const [openFilterDropdown, setOpenFilterDropdown] = useState(false);
  const [currFilters, setCurrFilters] = useState([]);
  // currFilters become active only when save button is clicked
  const [activeFilters, setActiveFilters] = useState([]);
  const filterForm = useRef();

  // Mock data for students table
  const students = [
    {
      name: "Sara Dorathy",
      email: "sara.dorathy@my.csun.edu",
      _id: 202069975,
      project: "Test Project 1",
      class: "COMP 492",
      teamLead: true,
      volunteer: false,
    },
    {
      name: "Adam Chester",
      email: "sara.dorathy@my.csun.edu",
      _id: 202069976,
      project: "Test Project 3",
      class: "COMP 493",
      teamLead: false,
      volunteer: false,
    },
    {
      name: "Brian Wooster",
      email: "sara.dorathy@my.csun.edu",
      _id: 202069977,
      project: "Test Project 1",
      class: "COMP 493",
      teamLead: true,
      volunteer: true,
    },
    {
      name: "Grace Winchester",
      email: "sara.dorathy@my.csun.edu",
      _id: 202069978,
      project: "Test Project 2",
      class: "COMP 492",
      teamLead: true,
      volunteer: false,
    },
    {
      name: "Irene Stone",
      email: "sara.dorathy@my.csun.edu",
      _id: 202069979,
      project: "Test Project 1",
      class: "COMP 493",
      teamLead: true,
      volunteer: true,
    },
    {
      name: "Jack Amber",
      email: "sara.dorathy@my.csun.edu",
      _id: 202069980,
      project: "Test Project 2",
      class: "COMP 492",
      teamLead: false,
      volunteer: false,
    },
    {
      name: "Timothy Potter",
      email: "sara.dorathy@my.csun.edu",
      _id: 202069981,
      project: "Test Project 1",
      class: "COMP 492",
      teamLead: true,
      volunteer: true,
    },
  ];

  // Mock data for projects table
  const projects = [
    {
      name: "Test Project 1",
      _id: 1,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 2",
      _id: 2,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 3",
      _id: 3,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 4",
      _id: 4,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 5",
      _id: 5,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 6",
      _id: 6,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 7",
      _id: 7,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 8",
      _id: 8,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
    {
      name: "Test Project 9",
      _id: 9,
      professors: ["Professor One", "Professor Two"],
      openSpots: 5,
      capacity: 10,
      skills: ["HTML", "CSS", "Javascript", "Problem Solving"],
      meetingSchedule: "Tues Thur 2-4pm",
    },
  ];

  // Helper function of handleColumnSort()
  function sortBy(tableName, column, sortOrder) {
    const currTable = tableName === "studentTable" ? students : projects;
    const sortedTable = currTable.toSorted((itemA, itemB) => {
      if (sortOrder === "ascending") {
        if (itemA[column] > itemB[column]) return 1;
        if (itemA[column] < itemB[column]) return -1;
        return 0;
      }
      if (itemA[column] > itemB[column]) return -1;
      if (itemA[column] < itemB[column]) return 1;
      return 0;
    });
    return sortedTable;
  }

  // Fetch data for tables from backend, and sort them by name
  // TODO: Implement fetching from backend
  useEffect(() => {
    const studentTable = sortBy("studentTable", "name", "ascending");
    setDisplayedStudents(studentTable);

    const projectTable = sortBy("projectTable", "name", "ascending");
    setDisplayedProjects(projectTable);
  }, []);

  // Change table from student to project or vice visa
  function toggleTables(e) {
    if (e.target.id === "studentTable") setIsStudentTable(true);
    else setIsStudentTable(false);
  }

  function handleFilterDropdown() {
    setOpenFilterDropdown(!openFilterDropdown);
  }

  function closeFilterDropdownWithEsc(e) {
    // TODO NOW: close filter dropdown with esc key and click outside
  }

  function removeElementsFromArray(element, array) {
    const delIndex = array.indexOf(element);
    array.splice(delIndex, 1);
  }

  function handleFilterCheckbox(e) {
    const filter = e.target.value;
    if (e.target.checked) setCurrFilters([...currFilters, filter]);
    else {
      const tempFilters = [...currFilters];
      removeElementsFromArray(filter, tempFilters);
      setCurrFilters(tempFilters);
    }
  }

  function saveStudentFilter() {
    setActiveFilters(currFilters);
    setOpenFilterDropdown(false);
    // TODO: Fetch fitlered students from backend
  }

  function resetStudentFilter() {
    filterForm.current.reset();
    setCurrFilters([]);
    setActiveFilters([]);
    // TODO: redisplay the student List before being filtered
  }

  // Return active fitlers JSX
  function generateActiveFilters() {
    let filterName;
    return (
      <>
        <h4 className="professorDashboard_activeFitlerTitle">
          Active Filters:{" "}
        </h4>
        <div className="professorDashboard_activeFilters">
          {activeFilters.map((filter, index) => {
            filterName = filter;
            if (filterName === "volunteer") filterName = "Volunteer";
            else if (filterName === "teamLead") filterName = "Team Lead";
            return (
              <div key={index} className="professorDashboard_activeFilter">
                {filterName}
              </div>
            );
          })}
          <button
            type="button"
            onClick={resetStudentFilter}
            className="professorDashboard_btn professorDashboard_filterResetBtn"
          >
            Reset
          </button>
        </div>
      </>
    );
  }

  // Sort the column of the tables
  // TODO NOW: check every columns of both tables
  function handleColumnSort(e) {
    const tableName = e.target.getAttribute("data-table-name");
    const column = e.target.id;
    let currSortOrder = null;
    if (currSortOrders.current[tableName].column === column) {
      currSortOrder = currSortOrders.current[tableName].order;
    }

    // new sort order has to be opposite of current sort order
    // if sorting for first time, sort order is ascending
    let sortOrder;
    if (currSortOrder === "ascending") sortOrder = "decending";
    else if (currSortOrder === "decending") sortOrder = "ascending";
    else if (currSortOrder === null) sortOrder = "ascending";

    if (currSortOrder === null) {
      currSortOrders.current[tableName].column = column;
      currSortOrders.current[tableName].order = "ascending";
    } else {
      currSortOrders.current[tableName].order = sortOrder;
    }
    const sortedTable = sortBy(tableName, column, sortOrder);

    if (tableName === "studentTable") setDisplayedStudents(sortedTable);
    else setDisplayedProjects(sortedTable);
  }

  // generate css selectors for sortable column icons
  function addSortableIcon(table, column) {
    let sortOrder;
    if (currSortOrders.current[table].column === column) {
      sortOrder = currSortOrders.current[table].order;
    }
    if (sortOrder === "ascending") return "bx bxs-down-arrow";
    if (sortOrder === "decending") return "bx bxs-up-arrow";
    return "bx bxs-sort-alt";
  }

  // Handle selectAll checkbox
  function selectAllCheckboxes(e) {
    const { checked } = e.target;
    checkboxes.forEach((checkbox) => {
      checkbox.checked = checked;
    });
    setSelectAll(checked);
  }

  function addToCheckboxes(ref) {
    checkboxes.push(ref);
  }

  function handleCheckbox(e) {
    if (e.target.checked === false) setSelectAll(false);
  }

  /** STUDENT TABLE */

  function deleteStudent(e) {
    // TODO
    // const studentId = e.target.getAttribute("data-student-id");
  }

  function addNewStudent() {
    // TODO
  }

  function handleSearchStudent(e) {
    if (e.key === "Enter" || e.type === "click") {
      // TODO: Search the entered student in backend
      // student's name is in e.target.value
    }
  }

  // Return student table JSX
  function generateStudentTable() {
    return (
      <div className="professorDashboard_table studentTable">
        {/* Table Header */}
        <label
          className="professorDashboard_checkboxLabel header"
          htmlFor="All Students"
        >
          <input
            type="checkbox"
            onChange={selectAllCheckboxes}
            checked={selectAll}
          />
        </label>
        <button
          className="header"
          type="button"
          data-table-name="studentTable"
          id="name"
          onClick={handleColumnSort}
        >
          Student Name <i className={addSortableIcon("studentTable", "name")} />
        </button>
        <button
          className="header"
          type="button"
          data-table-name="studentTable"
          id="_id"
          onClick={handleColumnSort}
        >
          Student ID <i className={addSortableIcon("studentTable", "_id")} />
        </button>
        <button
          className="header"
          type="button"
          data-table-name="studentTable"
          id="project"
          onClick={handleColumnSort}
        >
          Project <i className={addSortableIcon("studentTable", "project")} />
        </button>
        <button
          className="header"
          type="button"
          data-table-name="studentTable"
          id="class"
          onClick={handleColumnSort}
        >
          Class <i className={addSortableIcon("studentTable", "class")} />
        </button>
        <div className="header">Team Lead</div>
        <div className="header">Volunteer</div>
        <div className="header">Options</div>

        {/* Table Rows */}
        {displayedStudents.map((student) => (
          <React.Fragment key={student._id}>
            <label
              htmlFor="student"
              className="professorDashboard_checkboxLabel"
            >
              <input
                type="checkbox"
                onChange={handleCheckbox}
                ref={addToCheckboxes}
              />
            </label>
            <div className="professorDashboard_flexBox">
              <div>{student.name}</div>
              <div className="professorDashboard_studentEmail">
                {student.email}
              </div>
            </div>
            <div>{student._id}</div>
            <div className="professorDashboard_studentProject">
              <div>{student.project}</div>
            </div>
            <div>{student.class}</div>
            <div>{student.teamLead ? "Yes" : "No"}</div>
            <div>{student.volunteer ? "Yes" : "No"}</div>
            <div>
              <button
                type="button"
                data-student-id={student._id}
                onClick={deleteStudent}
                className="professorDashboard_btn professorDashboard_delBtn"
              >
                Delete
              </button>
            </div>
          </React.Fragment>
        ))}
      </div>
    );
  }

  /** PROJECT TABLE */

  function addNewProject() {
    // TODO
  }

  function handleSearchProject(e) {
    if (e.key === "Enter" || e.type === "click") {
      // TODO: Search the entered project in backend
      // project's name is in e.target.value
    }
  }

  function editProject(e) {
    // TODO
    // const projectId = e.target.getAttribute("data-project-id");
  }

  // Return project table JSX
  function generateProjectTable() {
    return (
      <div className="professorDashboard_table projectTable">
        {/* Table Header */}
        <label
          htmlFor="All Projects"
          className="professorDashboard_checkboxLabel header"
        >
          <input
            type="checkbox"
            onChange={selectAllCheckboxes}
            checked={selectAll}
          />
        </label>
        <button
          className="header"
          data-table-name="projectTable"
          type="button"
          id="name"
          onClick={handleColumnSort}
        >
          Project Name <i className={addSortableIcon("projectTable", "name")} />
        </button>
        <button
          className="header"
          data-table-name="projectTable"
          type="button"
          id="openSpots"
          onClick={handleColumnSort}
        >
          Open Spots
          <i className={addSortableIcon("projectTable", "openSpots")} />
        </button>
        <div className="header">Relevant Skills</div>
        <div className="header">Meeting Schedule</div>
        <div className="header">Options</div>
        {/* Table Rows */}
        {displayedProjects.map((project) => (
          <React.Fragment key={project._id}>
            <label
              htmlFor="student"
              className="professorDashboard_checkboxLabel"
            >
              <input
                type="checkbox"
                onChange={handleCheckbox}
                ref={addToCheckboxes}
              />
            </label>
            <div className="professorDashboard_flexBox">
              <div>{project.name}</div>
              <div className="professorDashboard_professorsContainer">
                {project.professors}
              </div>
            </div>
            <div>{`${project.openSpots} / ${project.capacity}`}</div>
            <div>{project.skills.join(", ")}</div>
            <div>{project.meetingSchedule}</div>
            <div>
              <button
                type="button"
                data-project-id={project._id}
                onClick={editProject}
                className="professorDashboard_btn professorDashboard_editBtn"
              >
                Edit
              </button>
            </div>
          </React.Fragment>
        ))}
      </div>
    );
  }

  return (
    <div className="professorDashboard">
      <div className="professorDashboard_sidebar">
        <div className="professorDashboard_profile">
          <span className="professorDashboard_avatar">T</span>
          <span>Theodora Anderson</span>
          <span className="professorDashboard_professorEmail">
            theodora.anderson@csun.edu
          </span>
        </div>
        <h3>DASHBOARD</h3>
        <button
          id="studentTable"
          type="button"
          className={isStudentTable ? "active" : ""}
          onClick={toggleTables}
        >
          STUDENTS
        </button>
        <button
          id="projectTable"
          type="button"
          className={!isStudentTable ? "active" : ""}
          onClick={toggleTables}
        >
          PROJECTS
        </button>
      </div>
      <div className="professorDashboard_mainContent">
        <div className="professorDashboard_topSection">
          <h3 className="professorDashboard_title">
            {isStudentTable ? "STUDENTS" : "PROJECTS"}
          </h3>
          <div className="professorDashboard_topSectionRight">
            <label
              htmlFor={isStudentTable ? "Search Student" : "Search Project"}
            >
              <div className="professorDashboard_searchBarContainer">
                <input
                  type="text"
                  className="professorDashboard_searchBar"
                  placeholder="search"
                  onKeyUp={
                    isStudentTable ? handleSearchStudent : handleSearchProject
                  }
                />
                <button
                  type="button"
                  onClick={
                    isStudentTable ? handleSearchStudent : handleSearchProject
                  }
                  className="professorDashboard_searchIcon"
                >
                  <i className="bx bx-search" />
                </button>
              </div>
            </label>
            <div className="professorDashboard_filterContainer">
              <button
                type="button"
                className="professorDashboard_btn professorDashboard_filterBtn"
                onClick={handleFilterDropdown}
              >
                Filters
              </button>
              <form
                className={
                  openFilterDropdown
                    ? "professorDashboard_filterDropDown active"
                    : "professorDashboard_filterDropDown"
                }
                ref={filterForm}
              >
                <h3>Filters</h3>
                <label htmlFor="COMP 492">
                  <input
                    type="checkbox"
                    id="COMP 492"
                    value="COMP 492"
                    onClick={handleFilterCheckbox}
                  />{" "}
                  COMP 492
                </label>
                <label htmlFor="COMP 493">
                  <input
                    type="checkbox"
                    id="COMP 493"
                    value="COMP 493"
                    onClick={handleFilterCheckbox}
                  />{" "}
                  COMP 493
                </label>
                <label htmlFor="Volunteer">
                  <input
                    type="checkbox"
                    id="Volunteer"
                    value="volunteer"
                    onClick={handleFilterCheckbox}
                  />{" "}
                  Volunteer
                </label>
                <label htmlFor="Team Lead">
                  <input
                    type="checkbox"
                    id="Team Lead"
                    value="teamLead"
                    onClick={handleFilterCheckbox}
                  />{" "}
                  Team Lead
                </label>
                <label htmlFor="Project">
                  <input type="checkbox" id="Project" /> Project
                </label>
                <button
                  type="button"
                  onClick={saveStudentFilter}
                  className="professorDashboard_btn professorDashboard_filterSaveBtn"
                >
                  Save
                </button>
              </form>
            </div>
            <button
              type="button"
              className="professorDashboard_addStudentBtn"
              onClick={isStudentTable ? addNewStudent : addNewProject}
            >
              {isStudentTable ? "ADD STUDENT" : "ADD PROJECT"}
            </button>
          </div>
        </div>
        {activeFilters.length > 0 && generateActiveFilters()}
        {isStudentTable ? generateStudentTable() : generateProjectTable()}
      </div>
    </div>
  );
}
