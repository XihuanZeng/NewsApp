var jayson = require('jayson');
 
// create a client
var client = jayson.client.http({
  port: 4040,
  hostname: 'localhost'
});
 
// don't invoke "add", wrap in a function instead
// we can use Promise, but Pormise is a ES6 concept
function add (a, b, callback) {
    client.request('add', [a, b], function(err, response) {
        if(err) throw err;
        console.log(response.result);
        // sequential call 
        callback(response.result);
      });

}

module.exports = {
    add: add
};