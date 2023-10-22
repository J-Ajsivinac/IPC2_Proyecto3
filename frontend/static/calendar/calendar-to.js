document.addEventListener('DOMContentLoaded', () => {
// start irrelevant code
    document.querySelector('#calendar-input-to').style.display = "flex";
    // end irrelevant code

    const options = {
    input: true,
    
    settings:{
        lang: "es",
    },
    actions: {
        changeToInput(e, calendar, dates) {
        if (dates[0]) {
            console.log(dates[0]);
            var dArr = dates[0].split("-");
            var newDate = dArr[2] + "/" + dArr[1] + "/" + dArr[0];
            calendar.HTMLInputElement.value = newDate;
            // if you want to hide the calendar after picking a date
            calendar.hide();
        } else {
            calendar.HTMLInputElement.value = "";
        }
        }
    }
    };

    const calendarInput = new VanillaCalendar("#calendar-input-to", options);
    calendarInput.init();
});
