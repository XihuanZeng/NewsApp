var express = require('express');
var router = express.Router();
const fs = require('fs');
var winston = require('winston');
var rpc_client = require('../rpc_client/rpc_client');

const logDir = 'log';
const tsFormat = () => (new Date()).toLocaleTimeString();



// we should refactor this part, put this into a logger.js and import from different modules
// we should also partition our err and stdout into different log files, use exceptionHandler
const logger = new (winston.Logger)({
  transports: [
    // colorize the output to the console
    new (winston.transports.Console)(
      { colorize: true,
        timestamp: tsFormat,
        level: 'info' }),
    new (winston.transports.File)(
      { filename: `${logDir}/results.log`,
        timestamp: tsFormat,
        level: 'info' }),
  ]
});
logger.level = 'debug';

// Create the log directory if it does not exist
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}


// GET users listing. 
router.get('/', function(req, res, next) {
  logger.info('getting more news')
  // it was res.render() in the template
  res.json(news);
});

// NewsPanel.js in client side will call this API
router.get('/userId=:userId&pageNum=:pageNum', function(req, res, next) {
  console.log("Fetching news...");
  // user ":" to get variable in url
  user_id = req.params['userId'];
  page_num = req.params['pageNum'];
 
  rpc_client.getNewsSummariesForUser(user_id, page_num,
 function(response) {
  res.json(response);
  });
})

module.exports = router;
