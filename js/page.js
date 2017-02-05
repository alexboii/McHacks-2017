document.getElementById("add-field").onclick = moreFields;
document.getElementById("remove-field").onclick = remove;
document.getElementById("refresh-field").onclick = addWebsite;

var counter = 0;

function moreFields() {

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

    console.log(counter);

}

function remove() {
    var elem = document.getElementById("enter-website-" + counter);
    elem.remove();
    counter--;
}


function addWebsite() {

    console.log("AM I HERE 2?");

    var URL = document.getElementById("input-website").value;
    var URL2 = document.getElementById("enter-website-1").value;
    var result;

    $.ajax({
        url: 'http://localhost:5000/script/api/positive/' + URL,
        type: 'PUT',
        // data: URL,
        crossDomain: true,
        header: "Access-Control-Allow-Origin: *",
        success: function(data) {
            alert('Load was performed.');
        }
    });

    $.ajax({
        url: 'http://localhost:5000/script/api/testwebsite/' + URL2,
        type: 'GET',
        // data: URL2,
        crossDomain: true,
        header: "Access-Control-Allow-Origin: *",
        success: function(data) {
            console.log(data);
            document.getElementById("write").innerHTML = data;
        }
    });


}