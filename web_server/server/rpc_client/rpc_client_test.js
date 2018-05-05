var client = require('./rpc_client');

// invoke 'add'
// callback functon only deal with resullt, err is handled in add funtion already
client.add(1, 2, function(res) {
    console.assert(res == 3);
})

// invoke "getNewsSummariesForUser"
client.getNewsSummariesForUser('test_user', 1, function(response) {
    console.assert(response != null);
});