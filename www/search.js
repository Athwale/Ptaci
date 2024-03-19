window.onload = function() {
    var box = document.querySelector("#javascriptNeeded");
    box.style.display = "none";
    clearFilter();
};

function clearFilter() {
    var checkboxes = document.querySelectorAll("input[type=checkbox]");
    checkboxes.forEach(clearInput);
    var checkboxes = document.querySelectorAll("input[type=radio]");
    checkboxes.forEach(clearInput);
    var notFoundBox = document.querySelector("#notFound");
    notFoundBox.style.display = "none"
    var default_radio = document.querySelector("#spotted_neurčeno");
    var default_radio_1 = document.querySelector("#type_neurčeno");
    var default_radio_2 = document.querySelector("#size_neurčeno");
    default_radio.checked = true;
    default_radio_1.checked = true;
    default_radio_2.checked = true;
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

function compare(bodyPart, selected_colors) {
    if (selected_colors[0] == 'neurčeno') {
        return true;
    }
    return selected_colors.every(val => bodyPart.includes(val));
}

function merge_descriptors(descriptors) {
    var merged = {};
    for (const line of descriptors) {
        const parsed_attr = line.innerText.toLowerCase().trim().split(":");
        const part = parsed_attr[0].trim();
        // Trim whitespaces from the color lists.
        const attrs = parsed_attr[1].split(',').map(Function.prototype.call, String.prototype.trim);
        if (part in merged) {
            current_list = merged[part];
            for (color of attrs) {
                if (! current_list.includes(color)) {
                    current_list.push(color);
                }
            }
            merged[part] = current_list;
        } else {
            merged[part] = attrs;
        }
    }
    return merged;
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
    const spotted = new Array('ne');

    // Get what colors are selected for each option and store them in lists.
    var radios = document.querySelectorAll("input[type=radio]");
    for (const r of radios) {
        if (r.checked) {
            const which_r = r.id.split("_");
            const column = which_r[0];
            const option = which_r[1];
            if (column == 'size') {
                size.push(option);
            } else if (column == 'type') {
                kind.push(option);
            } else if (column == 'spotted') {
                spotted[0] = option;
            }
        }
    }
    var checkboxes = document.querySelectorAll("input[type=checkbox]");
    var body_parts = {'beak': beak, 'head': head, 'chest': chest, 'wings': wings, 'back': back, 'tail': tail, 'legs': legs};
    for (const box of checkboxes) {
        if (box.checked) {
            const whichBox = box.name.split("_");
            const column = whichBox[0];
            const option = whichBox[1];
            var list = body_parts[column];
            list.push(option);
        }
    }
    // Filter results based on selected attributes.
    // TODO var vs const?
    // TODO remove all console.log
    // TODO optimize image size to what we have now.
    // TODO look for better and female pics in wiki photos.
    // TODO optimalizace - funkce pro kazdy checkbox pro pridani a odebrani barvy z mnoziny, generovat automaticky.
    var body_parts = {'zobák': beak, 'hlava': head, 'hruď': chest, 'křídla': wings, 'záda': back, 'ocas': tail, 'nohy': legs, 'velikost': size, 'typ': kind, 'kropenatost': spotted};
    var cards = document.querySelectorAll(".birdCard");
    var hidden = 0;
    for (const card of cards) {
        let hide_card = 0;
        stop = false;
        // Pull out bird attributes from the card and decide whether it stays visible.
        var descriptors = card.querySelectorAll(".description");
        var all_colors = merge_descriptors(descriptors)
        for (const [part, selected_colors] of Object.entries(body_parts)) {
            // Compare returns true when all selected colors are on the bird part.
            if (! compare(all_colors[part], selected_colors)) {
                hide(card);
                hidden++;
                // Only one decision to hide is needed.
                stop = true;
                break;
            } else {
                show(card);
            }
            if (stop) {
                continue;
            }
        }
    }

    var notFoundBox = document.querySelector("#notFound");
    if (cards.length == hidden) {
        notFoundBox.style.display = "block";
    } else {
        notFoundBox.style.display = "none";
    }
}