var jayson = require('jayson');
 
// create a client
// see backend server operations.py for this RPC
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

function getNewsSummariesForUser(user_id, page_num, callback) {
    client.request('getNewsSummariesForUser', [user_id, page_num], function(err, response) {
      if (err) throw err;
      console.log(response);
      callback(response.result);
    });
}

// no need to add callback
function logNewsClickForUser(user_id, news_id) {
    client.request('logNewsClickForUser', [user_id, news_id], function(err, response){
        if (err) throw err;
        console.log(response);
    });
}



module.exports = {
    add: add,
    getNewsSummariesForUser: getNewsSummariesForUser,
    logNewsClickForUser: logNewsClickForUser
};