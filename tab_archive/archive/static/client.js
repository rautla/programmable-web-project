//This method is executed when the webpage is loaded.
var logged_user = "";

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
    $("#Users").on("click", handleUsers);
    $("#Artists").on("click", handleArtists);
    $("#Songs").on("click", handleSongs);
    $("#Tablatures").on("click", handleTablatures);
    $("#searchForm").submit(handleSearch);
    $("#reglink").on("click", handleRegister);
    $("#login").submit(handleLogin);
    $("#logout").on("click", handleLogout);
    $("#Userdata").submit(handleUserData);
    $("#Newtablature").on("click", handleNewTablature);
    $("#Addtablature").on("click", handleAddTablature);
    
    //$('#search').bind('keypress', handleSearch);

	//TODO 2: Add corresponding click handlers for #deleteMessage button and #user_list li element
	//Since these elements are generated dynamically, you must use delegated events.
	//Recommend delegated are #messages for #deleteMessage button and #user_list for #user_list li element
        
        //EXAMPLE: 
        // #deleteMessage => handleDeleteMessage
        // #user_list li => handleGetUser
        // Direct and delegated events from http://api.jquery.com/on/
        //$("#messages").on("click", "#deleteMessage", handleDeleteMessage);
        //$("#user_list").on("click", "li", handleGetUser);
        
    $("#Table").on("click", "td", handleClickTable);

    //TODO‎: get something to show on page load (in our case this might be artists)    
    
        //Retrieve list of users from the server
        //getUsers();
    $("#Table").show();
    $("#leftcolumn").find("#Newtablature").hide();
    getArtists("/tab_archive/artists");
    handleLogout();
})

//True or False
var DEBUG = true,
    APP_URL = "http://localhost:8000/forum/api",
    RESPONSE_FORMAT = "json",
//Format of the request
    CONTENT_TYPE = "application/"+RESPONSE_FORMAT;
    
    
/**** START RESTFUL CLIENT****/


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
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        
        
        var email = data.user.email;
        if (email == undefined) {
            $("#Userprofile").find("#Email").hide();
        } else {
            $("#Userprofile").find("#Email").show();
        }
        $("#Userprofile").find("#Nickname").val(data.user.user_nickname);
        $("#Userprofile").find("#Email").val(data.user.email);
        $("#Userprofile textarea").val(data.user.description);
        $("#Userprofile").find("#Description").val(data.user.description);        
        $("#Userprofile").find("#Picture").val(data.user.picture);
        
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
        //alert("User information could not be retrieved.");
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

function createUser(apiurl, userData, credentials) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "PUT", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: userData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR) {
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        $("#login").hide();
        $("#reglink").hide();
        $("#logout").show();
        login(credentials);
        alert("Created.");
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
        
        var r = new Array();
        //var j = -1, recordId;
        var j = -1;
        r[++j] =  '<table><thead><tr><th>Users</th></tr></thead><tbody>'; 
        for (var i in data) {
            var d = data[i];
            r[++j] = '<tr><td class="user">';
            r[++j] = '<a href="';
            r[++j] = data[i].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i].link.rel;
            r[++j] = '" >';
            r[++j] = data[i].user_nickname;
            r[++j] = '</a></td></tr>';
        }
        r[++j] = '</tbody></table>';
        $('#Table').html(r.join(''));
        
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
            console.log("RECEIVED ERROR: textStatus:", textStatus, ";error:", errorThrown);
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
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        
        var r = new Array();
        var j = -1;
        r[++j] =  '<table><thead><tr><th>Artists</th></tr></thead><tbody>'; 
        for (var i in data) {
            var d = data[i];
            r[++j] = '<tr><td class="artist">';
            r[++j] = '<a href="';
            r[++j] = data[i].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i].link.rel;
            r[++j] = '" >';
            r[++j] = data[i].artist_id;
            r[++j] = '</a></td></tr>';
        }
        r[++j] = '</tbody></table>';
        $('#Table').html(r.join(''));
        
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
        $('#Table').html('<p style="font-size:200%;text-align:center;">Not found</p>');
    });
}

function findArtists(apiurl, searchData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: searchData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        
        var r = new Array();
        var j = -1;
        r[++j] =  '<table><thead><tr><th>Artists</th></tr></thead><tbody>'; 
        for (var i in data) {
            var d = data[i];
            r[++j] = '<tr><td class="artist">';
            r[++j] = '<a href="';
            r[++j] = data[i].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i].link.rel;
            r[++j] = '" >';
            r[++j] = data[i].artist_id;
            r[++j] = '</a></td></tr>';
        }
        r[++j] = '</tbody></table>';
        $('#Table').html(r.join(''));
        
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		
		$('#Table').html('<p style="font-size:200%;text-align:center;">Not found</p>');
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
        
        var r = new Array();
        var j = -1;
        r[++j] =  '<table><thead><tr><th>Artist</th><th>Song</th></tr></thead><tbody>'; 
        for (var i in data) {
            var d = data[i];
            r[++j] = '<tr><td class="artist">';
            r[++j] = '<a href="';
            r[++j] = data[i]["artist"].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i]["artist"].link.rel;
            r[++j] = '" >';
            r[++j] = data[i]["artist"].artist_id;
            r[++j] = '</a></td>';
            //r[++j] = data[i].artist_id;
            //r[++j] = '</td>';
            r[++j] = '<td class="song">';
            r[++j] = '<a href="';
            r[++j] = data[i]["song"].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i]["song"].link.rel;
            r[++j] = '" >';
            r[++j] = data[i]["song"].song_id;
            r[++j] = '</a></td></tr>';
        }
        r[++j] = '</tbody></table>';
        $('#Table').html(r.join(''));
        
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
        $('#Table').html('<p style="font-size:200%;text-align:center;">Not found</p>');
    });
}

function findSongs(apiurl, searchData) {
    $.ajax({
        url: apiurl, //The URL of the resource
        type: "POST", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: searchData, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json"}// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        
        var r = new Array();
        var j = -1;
        r[++j] =  '<table><thead><tr><th>Artist</th><th>Song</th></tr></thead><tbody>'; 
        for (var i in data) {
            var d = data[i];
            r[++j] = '<tr><td class="artist">';
            r[++j] = '<a href="';
            r[++j] = data[i]["artist"].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i]["artist"].link.rel;
            r[++j] = '" >';
            r[++j] = data[i]["artist"].artist_id;
            r[++j] = '</a></td>';
            //r[++j] = data[i].artist_id;
            //r[++j] = '</td>';
            r[++j] = '<td class="song">';
            r[++j] = '<a href="';
            r[++j] = data[i]["song"].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i]["song"].link.rel;
            r[++j] = '" >';
            r[++j] = data[i]["song"].song_id;
            r[++j] = '</a></td></tr>';
        }
        r[++j] = '</tbody></table>';
        $('#Table').html(r.join(''));
        
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		$('#Table').html('<p style="font-size:200%;text-align:center;">Not found</p>');
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
        
        var r = new Array();
        var j = -1;
        r[++j] =  '<table><thead><tr><th>Artist</th><th>Song</th><th>Tablature</th><th>User</th><th>Rating</th></tr></thead><tbody>'; 
        for (var i in data) {
            var d = data[i];
            r[++j] = '<tr><td class="artist">';
            r[++j] = '<a href="';
            r[++j] = data[i]["artist"].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i]["artist"].link.rel;
            r[++j] = '" >';
            r[++j] = data[i]["artist"].artist_id;
            r[++j] = '</a></td>';
            //r[++j] = data[i].artist_id;
            //r[++j] = '</td>';
            if (data[i].tablature.rating_count > 0) {
                var rating = data[i].tablature.rating/data[i].tablature.rating_count;
            } else {
                var rating = "-";
            }
            
            r[++j] = '<td class="song">';
            r[++j] = '<a href="';
            r[++j] = data[i]["song"].link.href;
            r[++j] = '" rel="';
            r[++j] = data[i]["song"].link.rel;
            r[++j] = '" >';
            r[++j] = data[i]["song"].song_id;
            r[++j] = '</a></td>';
            r[++j] = '<td class="tablature">';
            r[++j] = '<a href="';
            r[++j] = data[i].tablature.link.href;
            r[++j] = '" rel="';
            r[++j] = data[i].tablature.link.rel;
            r[++j] = '" >';
            r[++j] = data[i].tablature.tablature_id;
            r[++j] = '</a></td>';
            r[++j] = '<td class="user">';
            r[++j] = '<a href="';
            r[++j] = data[i].tablature.user.link.href;
            r[++j] = '" rel="';
            r[++j] = data[i].tablature.user.link.rel;
            r[++j] = '" >';
            r[++j] = data[i].tablature.user.user_nickname;
            r[++j] = '<td class="rating">';
            r[++j] = rating;
            r[++j] = '</td>';
            r[++j] = '</a></td></tr>';
        }
        r[++j] = '</tbody></table>';
        $('#Table').html(r.join(''));
        
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
        
        $('#Table').html('<p style="font-size:200%;text-align:center;">Not found</p>');
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


/*function getTablatures(apiurl) {
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
}*/

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

function login(credentials) {
    $.ajax({
        url: "http://localhost:8000/tab_archive/login", //The URL of the resource
        type: "GET", //The resource method
        contentType: CONTENT_TYPE, //The mime type of the request body
        data: null, //The body of the HTTP request
        processData: false, //Do not transform the data in key-value
        dataType:RESPONSE_FORMAT, //The format expected in the 
        headers: {"Accept": "application/json", "username" : credentials.username, "password" : credentials.password }// An object containing //headers
    }).done(function (data, textStatus, jqXHR){
        //code to be executed when response is //received. Data is an object. jqXHR is the //XMLHttpRequest object
		//console.log("done");
        if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        logged_user = credentials.username;
        console.log(logged_user);
        if (logged_user == undefined) { 
        } else {
            $("#leftcolumn").find("#Newtablature").show();
        }
    }).fail(function (jqXHR, textStatus, errorThrown){
        //code to be executed when response has an //error status code or response is malformed
        if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
        
        $("#login").show();
        $("#logout").hide();
        $("#reglink").show();
    });
}

/**** END RESTFUL CLIENT****/


/**** BUTTON HANDLERS ****/
function handleUsers(event) {
    $("#Table").show();
	$("#Userprofile").hide();
    $("#Tablaturepage").hide();
    if (DEBUG) {
		console.log("Triggered handleUsers");
	}
    
    var url = $("#Users").attr("href");
    //$("#breadcrumb").html(url);
    breadcrumbs(url);
    console.log(url);
	getUsers(url);
    
    return false;
}

function handleArtists(event) {
    $("#Table").show();
	$("#Userprofile").hide();
    $("#Tablaturepage").hide();
    if (DEBUG) {
		console.log ("Triggered handleArtists")
	}
    
    var url = $("#Artists").attr("href");
    //$("#breadcrumb").html(url);
    breadcrumbs(url);
    console.log(url);
	getArtists(url);
    
    return false;
}

function handleClickTable(event) {
    $("#Table").show();
	if (DEBUG) {
		console.log ("Triggered handleClickTable")
	}
    var url = $(this).children("a").attr("href");
    //$("#breadcrumb").html(url);
    breadcrumbs(url);
    var column = $(this).attr("class");
    if (column == "user") {
        handleUser(url);
    }
    console.log(url + " " + column);
    //var url = $("#Artists").attr("href");
    //console.log(url);
	//getArtists(url);
    
    return false;
}

function handleUser(url) {
    clearUserForm();
    $("#Table").hide();
    $("#Tablaturepage").hide();
    $("#Userprofile").show();
    
    var nickname = url;
    nickname = nickname.split("/");
    nickname = nickname[nickname.length-1];
    
    if (logged_user != nickname) {
        console.log(logged_user);
        console.log(nickname);
        console.log("if");
        $("#Userprofile input[name=password]").hide();
        $("#Userprofile input[name=password2]").hide();
        $("#Userprofile p[name=password]").hide();
        $("#Userprofile p[name=password2]").hide();
        $("#Applybutton").hide();
        
        $("#Userprofile input[name=nickname]").attr("readonly", "readonly");
        $("#Userprofile textarea").attr("readonly", "readonly");
        $("#Userprofile input[name=picture]").attr("readonly", "readonly");
    } else {
        console.log("else");
        $("#Userprofile input[name=password]").show();
        $("#Userprofile input[name=password2]").show();
        $("#Applybutton").show();
        
        $("#Userprofile input[name=nickname]").removeAttr("readonly");
        $("#Userprofile textarea").removeAttr("readonly");
        $("#Userprofile input[name=picture]").removeAttr("readonly");
    }
    
    getUser(url);
    
    return false;
}

function handleSongs(event) {
    $("#Table").show();
    $("#Userprofile").hide();
    $("#Tablaturepage").hide();
	if (DEBUG) {
		console.log ("Triggered handleSongs");
	}
    
    var url = $("#Songs").attr("href");
    //$("#breadcrumb").html(url);
    breadcrumbs(url);
    console.log(url);
	getSongs(url);
    
    return false;
}

function handleTablatures(event) {
    $("#Table").show()
	$("#Userprofile").hide();
    $("#Tablaturepage").hide();
    if (DEBUG) {
		console.log ("Triggered handleTablatures");
	}
    
    var url = $("#Tablatures").attr("href");
    //$("#breadcrumb").html(url);
    breadcrumbs(url);
    console.log(url);
	getTablatures(url);
    
    return false;
}

function handleNewTablature(event) {
    $("#Table").hide()
	$("#Userprofile").hide();
    $("#Tablaturepage").show();
    
    if (DEBUG) {
       console.log("Triggered handleNewTablature");            
    }
    
    $("#Commentnew").hide();
    $("#Commentreply").hide();
    $("#rate").hide();
    $("#rating").hide();
    $("#delete").hide();
    $("#comments").hide();
    $("#tabinfo").hide();
    return false;
}

function handleAddTablature(event) {
    if (DEBUG) {
       console.log("Triggered handleAddTablature");            
    }
    
    var artist = $("#Tablaturepage").find("#Artistname").val();
    var song = $("#Tablaturepage").find("#Songname").val();
    var body = $("#Tablaturepage").find("#Tablature").val();
    
    var url = '/tab_archive/artists/' + artist + '/' + song
    
    
    data = {"body":body, "user_nickname":logged_user}
    
    addTablature(url, JSON.stringify(data));
    
    return false;
}

function handleRegister(event) {
    
    $("#Userprofile input[name=password]").show();
    $("#Userprofile input[name=password2]").show();
    $("#Applybutton").show();
        
    $("#Userprofile input[name=nickname]").removeAttr("readonly");
    $("#Userprofile textarea").removeAttr("readonly");
    $("#Userprofile input[name=picture]").removeAttr("readonly");

    $("#Table").hide();
    clearUserForm();
    $("#Userprofile").show();
    $("#Tablaturepage").hide();
    if (DEBUG) {
        console.log ("Triggered handleRegister");
    }
    
    return false;
}    

function clearUserForm() {
    
    $("#Userprofile").find("#Email").show();
    
    $("#Userprofile").find("#Nickname").val("Nickname");
    $("#Userprofile").find("#Email").val("Email");
    $("#Userprofile").find("#Description").val("Description");        
    $("#Userprofile").find("#Picture").val("Picture");
}

function breadcrumbs(url) {
    var legs = url.split("/");
    var homeIndex = legs.indexOf("tab_archive");
    homeIndex;
    var crumb = [];
    for (var i = homeIndex; i < legs.length; i++) {
        var link = "";
        for (var j = homeIndex; j <= i; j++) {
            link += "/" + legs[j]; 
        }
        if (i == homeIndex) {
            crumb[i] = '<a href="' + "/tab_archive/artists" + '" >' + legs[i] + "</a>";
        } else {
            crumb[i] = '<a href="' + link + '" >' + legs[i] + "</a>";
        }
    }
    console.log(crumb);
    $("#breadcrumb").html(crumb.reverse().join(" "));
}

function handleSearch(event) {
    $("#Table").show();
    $("#Userprofile").hide();
    if (DEBUG) {
        console.log ("Triggered handleSearch");
    }
    
    if ($(":radio:checked").val() == "Song") {
        if (DEBUG) {
            console.log("Song search");
            //var url = "/tab_archive/songs            
        }
        var url = "/tab_archive/songs"
        breadcrumbs(url);
        var keyword = $("#search").val();
        var searchData = {"keyword":keyword};
        findSongs(url, JSON.stringify(searchData));    
    }

    if ($(":radio:checked").val() == "Artist") {
        if (DEBUG) {
            console.log("Artist search");            
        }
        var url = "/tab_archive/artists"
        breadcrumbs(url);
        var keyword = $("#search").val();
        var searchData = {"keyword":keyword};
        findArtists(url, JSON.stringify(searchData));
    }
    
    return false;
}

function handleLogin(event) {
    if (DEBUG) {
       console.log("Triggered handleLogin");            
    }
    var credentials = {"username":$("#login input[type=text]").val(), "password":$("#login input[type=password]").val()};
    //login(JSON.stringify(credentials));
    login(credentials);
    $("#login").hide();
    $("#reglink").hide();
    $("#logout").show();
    return false;
}

function handleUserData(event) {
    if (DEBUG) {
       console.log("Triggered handleUserData");            
    }
    var password = $("#Userdata input[name=password]").val();
    var password2 = $("#Userdata input[name=password2]").val();
    var nickname = $("#Userdata input[name=nickname]").val();
    if (password == password2) {
        
        var userData = {"picture" : $("#Userdata input[name=picture]").val(),
                        "password" : password,
                        "description" : $("#Userdata textarea").val(),
                        "email" : $("#Userdata input[name=email]").val()
                        };
        var url = "/tab_archive/users/" + nickname;
        console.log(url);
        
        var credentials = {"username":nickname, "password":password};
        
        if (nickname == logged_user) {
            editUser(url, JSON.stringify(userData));    
            
        } else {
            createUser(url, JSON.stringify(userData), credentials);    
            
        }
        
        
    } else {
        alert("Passwords don't match");
    }
    
    return false;
}

function handleLogout(event) {
    if (DEBUG) {
       console.log("Triggered handleLogout");            
    }
    login({});
    logged_user = ""
    $("#login").show();
    $("#logout").hide();
    $("#reglink").show();
    $("#leftcolumn").find("#Newtablature").hide();
}

