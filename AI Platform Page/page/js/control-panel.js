const api = "http://localhost:5000/api/"

function submit(){
    let name = document.getElementById("name").value
    let password = document.getElementById("password").value
    
    var obj = {
        Name: name,
        Password: password
    }

    var jsonSend = JSON.stringify(obj)
    document.getElementById("testOutput").innerHTML = httpRequest(api + "Groups", "POST", jsonSend)
    
    refreshGroups()
}

function refreshGroups()
{
    var jsonReceive = httpRequest(api+"Groups", "GET")

    var obj = JSON.parse(jsonReceive)

    var html = ""

    for(i = 0; i < obj.length; i++)
        html += "<div> " + obj[i].name +" <button onclick=\"deleteGroups(\'"+ obj[i].name +"\')\">Delete</button></div>\n"

    document.getElementById("groupList").innerHTML = html
    document.getElementById("testOutput").innerHTML = jsonReceive
}

function deleteGroups(name)
{

}

function httpRequest(theUrl, requestType, obj = null)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( requestType, theUrl, false ); // false for synchronous request
    xmlHttp.setRequestHeader('Content-type', 'application/json');
    xmlHttp.send( obj );
    return xmlHttp.responseText;
}

refreshGroups()