import React from 'react';
import ReactDOM from 'react-dom';
import App from './App/App';
import registerServiceWorker from './registerServiceWorker';
import LoginPage from './LoginPage';

// render App component on root
ReactDOM.render(<App />, document.getElementById('root'));
// client get files from cache if the Internet connection is slow
registerServiceWorker();

