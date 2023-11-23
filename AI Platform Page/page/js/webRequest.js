const api = "http://localhost:5000/api/"

function httpRequest(theUrl, requestType, obj = null, contentType = 'application/json')
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( requestType, theUrl, false ); // false for synchronous request
    xmlHttp.setRequestHeader('Content-type', contentType);
    xmlHttp.send( obj );
    return xmlHttp.responseText;
}