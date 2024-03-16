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
    var cards = document.querySelectorAll(".birdCard");
    cards.forEach(show);
}

function clearInput(box) {
    box.checked = false;
}

function show(card) {
    card.style.display = "inline-block";
}

function hide(card) {
    card.style.display = "none";
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

    // Get what colors are selected for each option and store them in sets.
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
    // Filter results based on selected attributes.
    // TODO remove all console.log
    // console.log(beak, head, chest, wings, back, tail, legs, size, kind, spotted);
    var cards = document.querySelectorAll(".birdCard");
    for (const card of cards) {
        let hide_card = 0;
        // Pull out bird attributes from the card and decide whether it stays visible.
        var descriptors = card.querySelectorAll(".description");
        for (const line of descriptors) {
            const whichAttr = line.innerText.toLowerCase().trim().split(":");
            const part = whichAttr[0].trim();
            const attrs = whichAttr[1].split(',');
            if (part == 'zobák') {
                hide_card = compare(attrs, beak);
                if (hide_card) {
                    break;
                }
            } else if (part == 'hlava') {
                hide_card = compare(attrs, head);
                if (hide_card) {
                    break;
                }
            } else if (part == 'hruď') {
                hide_card = compare(attrs, chest);
                if (hide_card) {
                    break;
                }
            } else if (part == 'křídla') {
                hide_card = compare(attrs, wings);
                if (hide_card) {
                    break;
                }
            } else if (part == 'záda') {
                hide_card = compare(attrs, back);
                if (hide_card) {
                    break;
                }
            } else if (part == 'ocas') {
                hide_card = compare(attrs, tail);
                if (hide_card) {
                    break;
                }
            } else if (part == 'nohy') {
                hide_card = compare(attrs, legs);
                if (hide_card) {
                    break;
                }
            } else if (part == 'velikost') {
                hide_card = compare(attrs, size);
                if (hide_card) {
                    break;
                }
            } else if (part == 'typ') {
                hide_card = compare(attrs, kind);
                if (hide_card) {
                    break;
                }
            } else if (part == 'kropenatost') {
                is_card_spotted = attrs[0].trim();
                if (spotted) {
                    if (is_card_spotted == 'ne') {
                        hide_card = 1;
                        break;
                    }
                } else if (!spotted) {
                    if (is_card_spotted == 'ano') {
                        hide_card = 1;
                        break;
                    }
                }
            }
        }
        console.log(hide_card);
        if (hide_card) {
            hide(card);
        } else {
            show(card);
        }
        }
}

function compare(colors, bodyPart) {
    //console.log();
    return 0;
}