const http = require('http');
var fs = require('fs');
var url = require('url');
const { debug } = require('console');

const hostname = '127.0.0.1';
const port = 8080;

const exceptions = {
  "/control-panel":"/control-panel.html",
  "/":"/index.html"
}

const server = http.createServer((req, res) => {
  
  var q = url.parse(req.url, true);

  var filename;

  filename = q.pathname

  for(let exception in exceptions){
    if(q.pathname == exception)
      filename = exceptions[exception]
  }

  console.log(filename)
  
  filename = "page" + filename;

  fs.readFile(filename, function(err, data) {

    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html'});
      return res.end("404 Not Found");
    } 

    res.write(data);

    return res.end();
  });

});

server.listen(port, hostname, () => {
  // eslint-disable-next-line no-console
  console.log(`Server running at http://${hostname}:${port}/`);
});