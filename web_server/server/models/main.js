const mongoose = require('mongoose');

module.exports.connect = (uri) => {
  mongoose.connect(uri);

  mongoose.connection.on('error', (err) => {
    console.error(`Mongoose connection error: ${err}`);
    process.exit(1);
  });

  // load models
  // if you call this function, it will load ./user which has 
  require('./user');
};