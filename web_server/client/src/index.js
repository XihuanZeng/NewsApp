import React from 'react';
import ReactDOM from 'react-dom';
import App from './App/App';
import registerServiceWorker from './registerServiceWorker';
import LoginPage from './Login/LoginPage';
import SignUpPage from './SignUp/SignUpPage';

// render App component on root
// <App /> will use the App component
// document.getElementById('root'), in the index.html there is a <div id='root'>
ReactDOM.render(<SignUpPage />, document.getElementById('root'));
// client get files from cache if the Internet connection is slow
registerServiceWorker();

