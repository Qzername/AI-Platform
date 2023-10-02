function submitGroup(){
    let name = document.getElementById("groupName").value
    let password = document.getElementById("groupPassword").value
    
    var obj = {
        Name: name,
        Password: password
    }

    var jsonSend = JSON.stringify(obj)
    document.getElementById("testOutput").innerHTML = httpRequest(api + "Groups", "POST", jsonSend)
    
    refreshGroups()
}

function deleteGroup(name)
{
    httpRequest(api + "Groups/" + name, "DELETE")
    refreshGroups()
}

function refreshGroups()
{
    var jsonReceive = httpRequest(api+"Groups", "GET")

    var obj = JSON.parse(jsonReceive)

    var html = ""

    for(i = 0; i < obj.length; i++)
        html += "<div> " + obj[i].name +" <button onclick=\"deleteGroup(\'"+ obj[i].name +"\')\">Delete</button></div>\n"

    document.getElementById("groupList").innerHTML = html
    document.getElementById("testOutput").innerHTML = jsonReceive
}

refreshGroups()