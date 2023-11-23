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

  var reader = new FileReader();
  reader.onload = function(e) {
    formData = new FormData()
    console.log(e)
    formData.append("file", e.target.result)
  };

  reader.readAsText(file);
}

document.getElementById('file-input')
  .addEventListener('change', readFile, false);

function runTestModel()
{
  console.log("abc")
  for (var [key, value] of formData.entries()) { 
    console.log(key, value);
  }
  console.log("cba")
  var jsonReceive = httpRequest(api + "Execute/Execute", "POST", formData, 'multipart/form-data')
  console.log(jsonReceive)
}