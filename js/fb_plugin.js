
//// FB handlers
// Only works after `FB.init` is called
// only get permissions to view user's likes  
function myFacebookLogin() {
    FB.login(function (response) {
        if (response.authResponse) {
            FB.api('/me', { fields: 'email, likes' }, function (response) {
                console.log("Am I here? 2");
                document.getElementById("welcome-text").innerHTML = "Welcome to the website, " + response.name + ".";
                document.getElementById("welcome-text").style.display = "block";
                document.getElementById("readroot").style.display = "block";
                document.getElementById("buttons-fields-add").style.display = "block";
                // document.getElementById("add-field").style.display = "inline-block";
                // document.getElementById("remove-field").style.display = "inline-block";
                document.getElementById("facebook-login").style.display = "none";
            });
        } else {
            console.log("Am I here? 1");
            document.getElementById("welcome-text").style.display = "block";
            document.getElementById("welcome-text").innerHTML = "The website cannot work without your permission :(";
        }
    }, { scope: 'email,user_likes' });

}

$(document).on(
    'fbload',
    FB.api('/me', { fields: 'email, likes' }, function (response) {
        console.log(response);
    })
);

