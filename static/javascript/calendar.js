const daysContainer = document.getElementById("days-container");
const monthYear = document.getElementById("month-year");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

let currentDate = new Date();

function renderCalendar(date) {
    daysContainer.innerHTML = "";
    const today = new Date();
    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

    monthYear.textContent = date.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
    });

    // Add empty divs for days before the first of the month
    for (let i = 0; i < firstDay.getDay(); i++) {
        daysContainer.innerHTML += `<div></div>`;
    }

    // Add days of the current month
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const isToday =
            day === today.getDate() &&
            date.getMonth() === today.getMonth() &&
            date.getFullYear() === today.getFullYear();

        daysContainer.innerHTML += `<div class="day ${
            isToday ? "highlight" : ""
        }">${day}</div>`;
    }
}

prevBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate);
});

nextBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate);
});

renderCalendar(currentDate);
