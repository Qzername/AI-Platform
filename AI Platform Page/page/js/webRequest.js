const api = "http://localhost:5000/api/"

function httpRequest(theUrl, requestType, obj = null, contentType = 'application/json')
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( requestType, theUrl, false ); // false for synchronous request
    xmlHttp.setRequestHeader('Content-type', contentType);
    xmlHttp.setRequestHeader('ngrok-skip-browser-warning', '6024');
    xmlHttp.send( obj );
    return xmlHttp.responseText;
}

async function httpRequestFetch(url, formData)
{
    for (var [key, value] of formData.entries()) { 
      console.log(key, value);
    }

    console.log(url)

    const response = await fetch(url,{
        method: "POST",
        body: formData,
      });
      
    return await response.text();
}