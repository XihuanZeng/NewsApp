var express = require('express');
var path = require('path');
var app = express();


var index = require('./routes/index');
var news = require('./routes/news');

// view engine setup
// "views" is a folder/directory which contain the html files, 
// and express looks for the "views" folder as default 
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static',
    express.static(path.join(__dirname, '../client/build/static/')));

// TODO: remove this after development is done
app.all('*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
});

app.use('/', index);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;

