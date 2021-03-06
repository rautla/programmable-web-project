//This method is executed when the webpage is loaded.
$(function(){

	//TODO 2: Add corresponding click handler to buttons.
    
        //EXAMPLE:
        // #saveUser -> handleEditUser
        // #deleteUser -> handleDeleteUser
        // #addUser -> handleAddUser
        // Check http://api.jquery.com/on/ for more help.

        //$("#saveUser").on("click", handleEditUser);
        //$("#deleteUser").on("click", handleDeleteUser);
        //$("#addUser").on("click", handleAddUser);

	//TODO 2: Add corresponding click handlers for #deleteMessage button and #user_list li element
	//Since these elements are generated dynamically, you must use delegated events.
	//Recommend delegated are #messages for #deleteMessage button and #user_list for #user_list li element
        
        //EXAMPLE: 
        // #deleteMessage => handleDeleteMessage
        // #user_list li => handleGetUser
        // Direct and delegated events from http://api.jquery.com/on/
        //$("#messages").on("click", "#deleteMessage", handleDeleteMessage);
        //$("#user_list").on("click", "li", handleGetUser);

    //TODO‎: get something to show on page load (in our case this might be artists)    
    
        //Retrieve list of users from the server
        //getUsers();
})

//True or False
var DEBUG = true,
    APP_URL = "http://localhost:8000/forum/api",
    RESPONSE_FORMAT = "json",
//Format of the request
    CONTENT_TYPE = "application/"+RESPONSE_FORMAT;
    
    
/**** START RESTFUL CLIENT****/


    /*function getUsers() {
        //http://localhost:8000/forum/users
        var arr = [APP_URL, "users"]
        var apiurl = arr.join("/")
        $.ajax({
            url: apiurl,
            dataType:RESPONSE_FORMAT
        }).always(function(){
            //Remove old list of users, clear the form data hide the content information(no selected)
            $("#user_list").empty();
            clearUserInfo();
            $("#mainContent").hide();

        }).done(function (data, textStatus, jqXHR){
            if (DEBUG) {
                console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
            }
            
            if (RESPONSE_FORMAT === "json") {
                for (var i=0; i < data.length; i++){
                    var user = data[i];
                    appendUserToList(user.link.href, user.nickname);
                }
            }

            else if (RESPONSE_FORMAT === "xml"){

            }


        }).fail(function (jqXHR, textStatus, errorThrown){
            if (DEBUG) {
                console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
            }
            //Inform user about the error using an alert message.
            alert ("Could not fetch the list of users.  Please, try again");

        });
    }*/


function getUser(apiurl) {
    //TODO 1: Send the AJAX to retrieve the user information. Do not implement the handlers yet, just show some DEBUG text in the console. 
	//TODO 3: Implement the handlers successful and failures responses accordding to the function documentation.
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Authorization":"admin", "Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        
        /*var user = data.userprofile;
        
        
        $("#userData").find("#firstname").val(user.name.firstname);
        $("#userData").find("#lastname").val(user.name.lastname);
        $("#userData").find("#age").val(user.age);
        $("#userData").find("#gender").val(user.gender);
        $("#userData").find("#residence").val(user.residence);
        $("#userData").find("#email").val(user.email);
        $("#userData").find("#website").val(user.website);
        $("#userData").find("#picture").val(user.picture);
        $("#userData").find("#registrationdate").val(user.registrationdate);
        $("#userData").attr("action", apiurl);
        
        $("#userData").find("#nickname").val(user.nickname);
        
        var userHistory = data.history.href;
        getUserHistory(userHistory);
        
        $("#mainContent").show();*/
                
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
        alert("User information could not be retrieved.");
        /*$("#user_list li").removeClass("selected");
        $("#mainContent").hide();*/
    });
}

function deleteUser(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "DELETE", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function editUser(apiurl, userData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "PUT", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: userData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function createUser(apiurl, userData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "PUT", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: userData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function getUsers(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getUserComments(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function getUserTablatures(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function getTablatureComments(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getArtist(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function getArtists(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getSong(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getSongs(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function addTablature(apiurl, tablatureData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: tablatureData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function getTablatures(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getComment(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function deleteComment(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "DELETE", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function modifyComment(apiurl, commentData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "PUT", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: commentData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function replyComment(apiurl, commentData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: commentData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getRating(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: commentData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });

}

function addRating(apiurl, ratingData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: ratingData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getTablature(apiurl, commentData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: commentData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function deleteTablature(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "DELETE", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function editTablature(apiurl, tablatureData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "PUT", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: tablatureData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function commentTablature(apiurl, commentData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: commentData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}


function getTablatures(apiurl) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

function addTablatures(apiurl, tablatureData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
    });
}

/**** END RESTFUL CLIENT****/


/**** BUTTON HANDLERS ****/