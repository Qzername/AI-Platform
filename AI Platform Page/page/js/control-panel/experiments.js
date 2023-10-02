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
    document.getElementById("testOutput").innerHTML =  httpRequest(api + "Experiments", "GET")
}

refreshExperiments()