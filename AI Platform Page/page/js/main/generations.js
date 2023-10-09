currentSelectedGeneration = -1

function refreshGenerations(id)
{
    var generations = experiments[id].generations

    var html = ""

    for(var g in generations)
    {
        html += `
                <div class="d-inline bg-darkTheme2">
                  <div class="d-inline triangle">
                    <div class="d-inline px-1 triangle-offset">
                      ${generations[g].name}
                    </div>
                  </div>
                </div>`
        
    }

    document.getElementById("generationList").innerHTML = html
}