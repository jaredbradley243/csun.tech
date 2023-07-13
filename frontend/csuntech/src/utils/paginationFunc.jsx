import React from "react";

export function computeProjectsInCurrPage(projects, currPage, projectPerPage) {
  let list = [];
  const startIndex = (currPage - 1) * projectPerPage;
  list = projects.slice(startIndex, startIndex + projectPerPage);
  return list;
}

export function computeTotalPages(numOfProjects, projectPerPage) {
  const total = Math.ceil(numOfProjects / projectPerPage);
  return total;
}

export function makePageBtnActive(pageBtnContainer, currPage) {
  const pageBtnsList = Array.from(pageBtnContainer.current.children);
  pageBtnsList.forEach((btn) => {
    if (parseInt(btn.getAttribute("data-btn-value"), 10) === currPage)
      btn.classList.add("active");
    else btn.classList.remove("active");
  });
}

export function generatePageBtnsHelper(start, end, changePage) {
  const buttons = [];
  for (let i = start; i <= end; i += 1)
    buttons.push(
      <button key={i} data-btn-value={i} type="button" onClick={changePage}>
        {i}
      </button>
    );
  return buttons;
}

export function generatePageBtns(totalPages, currPage, changePage) {
  let buttons = [];
  if (totalPages < 6) {
    buttons = generatePageBtnsHelper(1, totalPages);
  } else {
    const firstBtn = (
      <button
        className="active"
        key="1"
        data-btn-value="1"
        type="button"
        onClick={changePage}
      >
        1
      </button>
    );
    const lastBtn = (
      <button
        key={totalPages}
        data-btn-value={totalPages}
        type="button"
        onClick={changePage}
      >
        {totalPages}
      </button>
    );
    const spacingDots = [
      <span key="spacing1">...</span>,
      <span key="spacing2">...</span>,
    ];
    buttons.push(firstBtn);
    if (currPage - 2 > 1) buttons.push(spacingDots[0]);

    if (currPage < 3) {
      buttons = buttons.concat(generatePageBtnsHelper(2, 4, changePage));
    } else if (totalPages - currPage < 2) {
      buttons = buttons.concat(
        generatePageBtnsHelper(totalPages - 3, totalPages - 1, changePage)
      );
    } else {
      buttons = buttons.concat(
        generatePageBtnsHelper(currPage - 1, currPage + 1, changePage)
      );
    }

    if (currPage + 2 < totalPages) buttons.push(spacingDots[1]);
    buttons.push(lastBtn);
  }
  return buttons;
}
