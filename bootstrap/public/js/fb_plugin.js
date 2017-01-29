
//// FB handlers
// Only works after `FB.init` is called
// only get permissions to view user's likes  
function myFacebookLogin() {
    FB.login(function (response) {
        if (response.authResponse) {
            FB.api('/me', { fields: 'name, email, likes' }, function (response) {
                
                document.getElementById("welcome-text").innerHTML = "Welcome to the website, " + response.name + ".";
                document.getElementById("welcome-text").style.display = "block";
                document.getElementById("readroot").style.display = "block";
                document.getElementById("buttons-fields-add").style.display = "block";
                // document.getElementById("add-field").style.display = "inline-block";
                // document.getElementById("remove-field").style.display = "inline-block";
                document.getElementById("facebook-login").style.display = "none";

               console.log(response.likes.data)
               var likesJSON = JSONify(response.likes.data)
               retrieveLinks(likesJSON)
            });
        } else {
            
            document.getElementById("welcome-text").style.display = "block";
            document.getElementById("welcome-text").innerHTML = "The website cannot work without your permission :(";
        }
    }, { scope: 'email,user_likes' });

}

// transform array to JSON
function JSONify(arr) {
    var output = {}
    for(var i=0;i<arr.length;i++) {
        output[arr[i].id] = arr[i].name
    }

    return output;
}

// given a set of likes return an array of links
function retrieveLinks(likedPages) {
    var links = {}

    for(var page in likedPages) {
        $.ajax({
            type: "POST",
            url: "js/process_profile.php",
            data: { 'name': likedPages[page] },
            async: false,
            success: function(response) {
                console.log(response)
            }
        });
    }
}

