document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#calendar-input').style.display = "flex";
    const options = {
    input: true,
    type: "multiple",
    settings:{
        lang: "es",
        range: {
            disablePast: false,
        },
        selection: {
            day: 'multiple-ranged',
        },
        visibility: {
            daysOutside: false,
        },
    },
    actions: {
        changeToInput(e, calendar, dates) {
        if (dates[0]) {
            if (dates[1]) {
                dates.sort((a, b) => +new Date(a) - +new Date(b));
                var d1 = dates[0].split("-");
                var d2 = dates[dates.length - 1].split("-");
                var date1 = d1[2] + "/" + d1[1] + "/" + d1[0];
                var date2 = d2[2] + "/" + d2[1] + "/" + d2[0];
                calendar.HTMLInputElement.value = `${date1} - ${date2}`;
            } else if (dates[0]) {
                var dArr = dates[0].split("-");
                var newDate = dArr[2] + "/" + dArr[1] + "/" + dArr[0];
                calendar.HTMLInputElement.value = newDate;
            } else {
                calendar.HTMLInputElement.value = '';
            }
        } else {
            calendar.HTMLInputElement.value = "";
        }
        }
    }
    };

    const calendarInput = new VanillaCalendar('#calendar-input', options);
    calendarInput.init();
});
