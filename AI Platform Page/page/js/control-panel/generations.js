function submitGeneration()
{
    var experimentID = document.getElementById("generationExperimentID").value
    var generationName = document.getElementById("generationName").value

    var obj = {
        ExperimentID: experimentID,
        Name: generationName
    }

    var json = JSON.stringify(obj)
    
    httpRequest(api + "Generations", "POST", json)

    refreshExperiments()
}

function deleteGeneration(generationID)
{
    httpRequest(api + "Generations/"+ generationID, "DELETE")

    refreshExperiments()
}