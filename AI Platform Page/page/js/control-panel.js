function submit(){
    let name = document.getElementById("name").value
    let password = document.getElementById("password").value
    
    document.getElementById("testOutput").innerHTML = httpGet("http://localhost:8080/")
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}