var groups = []

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
    {
        html += `<div>Name: ${obj[i].name} <br> Password: ${obj[i].password} <br> <button onclick=\"deleteGroup(\'${obj[i].name}\')\">Delete</button></div>\n`
        groups[i] = {
            id: obj[i].id,
            name: obj[i].name
        }
    }

    document.getElementById("groupList").innerHTML = html
    document.getElementById("testOutput").innerHTML = jsonReceive
}

function changeGroup(experimentName)
{
    var experimentJSON = httpRequest(api + "Experiments/"+experimentName, "GET")
    var experiment = JSON.parse(experimentJSON)

    var current = document.getElementById("select"+experiment.id).value
    var currentID = groups.indexOf(groups.find(x=>x.name == current))

    if(experiment.allowedGroups != null && experiment.allowedGroups.length != 0)
    {
        var jsonOBJ = {
            ExperimentID: experiment.id,
            GroupID: experiment.allowedGroups[0].id
        }

        console.log(experiment.allowedGroups[0].id)
        
        httpRequest(api+"Permissions", "DELETE", JSON.stringify(jsonOBJ))    
    }

    if(current != "Public")
    {
        var jsonOBJ = {
            ExperimentID: experiment.id,
            GroupID: groups[currentID].id
        }

        httpRequest(api+"Permissions", "POST", JSON.stringify(jsonOBJ))
    }
}

refreshGroups()