var counter;

document.getElementById("add-field").onclick = moreFields;
document.getElementById("remove-field").onclick = remove;

function moreFields() {

    console.log("AM I here?");
    counter++;
    var newFields = document.getElementById("input-website").cloneNode(true);
    newFields.id = "enter-website-" + counter;
    newFields.style.display = "block";

    var newField = newFields.childNodes;

    for (var i = 0; i < newField.length; i++) {
        var theName = newField[i].name
    }

    if (theName) {
        newField[i].name = theName + counter;
    }

    var insertHere = document.getElementById("writeroot");
    insertHere.parentNode.insertBefore(newFields, insertHere);

}

function remove() {
    var elem = document.getElementById("enter-website-" + counter);
    elem.remove();
    counter--;
}


