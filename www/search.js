window.onload = function() {
    var box = document.querySelector("#javascriptNeeded");
    box.style.display = "none";
    clearFilter();
};

function clearFilter() {
    var checkboxes = document.querySelectorAll("input[type=checkbox]");
    checkboxes.forEach(clearInput);
    var notFoundBox = document.querySelector("#notFound");
    notFoundBox.style.display = "none"
}

function clearInput(box) {
    box.checked = false;
}

function onFilter() {
    const beak = new Set();
    const head = new Set();
    const chest = new Set();
    const wings = new Set();
    const back = new Set();
    const tail = new Set();
    const legs = new Set();
    const size = new Set();
    const kind = new Set();
    let spotted = 0;
    // get what colors are selected for each option.
    // pull apart details and parse description into arrays.
    var checkboxes = document.querySelectorAll("input[type=checkbox]");
    for (const box of checkboxes) {
        if (box.checked) {
            const whichBox = box.name.split("_");
            column = whichBox[0];
            option = whichBox[1];
            if (column == 'beak') {
                beak.add(option);
            } else if (column == 'head') {
                head.add(option);
            } else if (column == 'chest') {
                chest.add(option);
            } else if (column == 'wings') {
                wings.add(option);
            } else if (column == 'back') {
                back.add(option);
            } else if (column == 'tail') {
                tail.add(option);
            } else if (column == 'legs') {
                legs.add(option);
            } else if (column == 'size') {
                size.add(option);
            } else if (column == 'type') {
                kind.add(option);
            } else if (column == 'spotted') {
                spotted = 1;
            }

        }
    }
    console.log(beak, head, chest, wings, back, tail, legs, size, kind, spotted);
}
