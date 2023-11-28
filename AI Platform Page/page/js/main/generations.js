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

let formData

function readFile(e)
{
  var file = e.target.files[0];
  if (!file) {
    return;
  }

  formData = new FormData()
  formData.append("file", file)
}

document.getElementById('file-input')
  .addEventListener('change', readFile, false);

async function runTestModel()
{
  console.log("abc")

  for (var [key, value] of formData.entries()) { 
    console.log(key, value);
  }

  console.log("cba")

  var jsonReceive = await httpRequestFetch(api + "Execute/Execute", formData)
  
  
  document.getElementById("apiResult").innerHTML = jsonReceive
  console.log(jsonReceive)
}