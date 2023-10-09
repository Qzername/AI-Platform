experiments = []
currentSelectedExperiment = -1

function refreshExperiments()
{
    var jsonReceive = httpRequest(api + "Experiments", "GET")

    var obj = JSON.parse(jsonReceive)

    experiments = obj

    var html = ""

    for(var i = 0; i < obj.length;i++)
        html += `<div onclick="experimentClicked(${i})" class="bg-darkTheme1 w-100" style="height: 20px; margin-top: 5px;">${obj[i].name}</div>`

    document.getElementById("experimentList").innerHTML = html
}

function experimentClicked(id) 
{ 
    currentSelectedExperiment = id
    refreshGenerations(id)
}

refreshExperiments()
experimentClicked(0)