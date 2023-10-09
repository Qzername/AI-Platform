function submitExperiment(){
    var experimentName = document.getElementById("experimentName").value

    experimentName = "\"" + experimentName + "\""

    var jsonOBJ = {
        Name: experimentName
    }

    var json = JSON.stringify(jsonOBJ)
    
    document.getElementById("testOutput").innerHTML = json

    httpRequest(api + "Experiments", "POST", experimentName)

    refreshExperiments()
}

function refreshExperiments(){
    var jsonReceive = httpRequest(api + "Experiments", "GET")

    var obj = JSON.parse(jsonReceive)

    var html = ""

    for(var i = 0; i < obj.length; i++)
    {
        html += `
        <div class="experiment">
            <b style="font-size: 48px;">${obj[i].name}</b> <br> 
            ID: ${obj[i].id} <br>
            <b>Permission:  </b>
            <select onchange="changeGroup(\'${obj[i].name}\')" id="select${obj[i].id}">`
        
        html += "<option>Public</option>"

        for(var g in groups)
        {
            html+= (obj[i].allowedGroups.length > 0 && obj[i].allowedGroups.some(x=>x.name == groups[g].name)) ?`<option selected>` :`<option>`
            html+= `${groups[g].name}</option>`          
        }

        html+=`</select> <br> 
            <b>Generations: </b> <br> ` 
    
        if(obj[i].generations != null) 
            for(var j = 0; j<obj[i].generations.length;j++)
                html += `<div class="generation">
                            <b>${obj[i].generations[j].name} </b>
                            <button>Upload model</button> 
                            <button onclick="deleteGeneration(${obj[i].generations[j].id})">Delete Generation</button>
                        </div>`    

        html+= `<button onclick="deleteExperiment(${obj[i].id})">Delete Experiment</button></div>`
    }
    
    document.getElementById("experimentList").innerHTML = html
    document.getElementById("testOutput").innerHTML = jsonReceive
}

function deleteExperiment(id)
{
    httpRequest(api + 'Experiments/' + id, "DELETE")
}

refreshExperiments()