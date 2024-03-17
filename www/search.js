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
    const beak = new Array();
    const head = new Array();
    const chest = new Array();
    const wings = new Array();
    const back = new Array();
    const tail = new Array();
    const legs = new Array();
    const size = new Array();
    const kind = new Array();
    let spotted = 0;

    // Get what colors are selected for each option and store them in lists.
    var checkboxes = document.querySelectorAll("input[type=checkbox]");
    for (const box of checkboxes) {
        if (box.checked) {
            const whichBox = box.name.split("_");
            column = whichBox[0];
            option = whichBox[1];
            if (column == 'beak') {
                beak.push(option);
            } else if (column == 'head') {
                head.push(option);
            } else if (column == 'chest') {
                chest.push(option);
            } else if (column == 'wings') {
                wings.push(option);
            } else if (column == 'back') {
                back.push(option);
            } else if (column == 'tail') {
                tail.push(option);
            } else if (column == 'legs') {
                legs.push(option);
            } else if (column == 'size') {
                size.push(option);
            } else if (column == 'type') {
                kind.push(option);
            } else if (column == 'spotted') {
                spotted = 1;
            }
        }
    }
    // Filter results based on selected attributes.
    // TODO remove all console.log
    // TODO look for better pics in wiki photos.
    // TODO optimalizace - funkce pro kazdy checkbox pro pridani a odebrani barvy z mnoziny, generovat automaticky.
    // TODO does not work on bazant for some reason, is the female div a problem? Do we have to combine them? Merge male and female colors into one set.
    // console.log(beak, head, chest, wings, back, tail, legs, size, kind, spotted);
    var cards = document.querySelectorAll(".birdCard");
    for (const card of cards) {
        let hide_card = 0;
        // Pull out bird attributes from the card and decide whether it stays visible.
        var descriptors = card.querySelectorAll(".description");
        for (const line of descriptors) {
            const whichAttr = line.innerText.toLowerCase().trim().split(":");
            const part = whichAttr[0].trim();
            // Trim whitespaces from the color lists.
            const attrs = whichAttr[1].split(',').map(Function.prototype.call, String.prototype.trim);
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
                const [is_card_spotted] = attrs;
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
        if (hide_card) {
            hide(card);
        } else {
            show(card);
        }
        }
}

function compare(bodyPart, selected_colors) {
    // TODO sorted colors are not aplphabetically sorted - č
    if (selected_colors.every(val => bodyPart.includes(val))) {
        return 0;
    }
    return 1;
}