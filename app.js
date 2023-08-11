const http = require('http');
var fs = require('fs');
var url = require('url');

const hostname = '127.0.0.1';
const port = 8080;

const server = http.createServer((req, res) => {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
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