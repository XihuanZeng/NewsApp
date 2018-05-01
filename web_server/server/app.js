var express = require('express');
var path = require('path');
var app = express();
var config = require('./config/config.json');
var auth = require('./routes/auth');
var bodyParser = require('body-parser');
var passport = require('passport');
var index = require('./routes/index');
var news = require('./routes/news');
var cors = require('cors');


app.use(bodyParser.json());

// connect mongodb
require('./models/main.js').connect(config.mongoDbUri);
// authChecker must be after connecting mongoose
var authCheckMiddleWare = require('./middleware/auth_checker');

// passport
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);


// view engine setup
// "views" is a folder/directory which contain the html files, 
// and express looks for the "views" folder as default 
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static',
    express.static(path.join(__dirname, '../client/build/static/')));

// TODO: remove this after development is done
// avoid cross-domain
app.use(cors());

// router
app.use('/', index);
app.use('/auth', auth);
app.use('/news', authCheckMiddleWare);
app.use('/news', news);



// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;

