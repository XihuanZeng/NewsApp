import 'materialize-css/dist/css/materialize.min.css';
import './App.css';

import React from 'react';

// you have to put it in the same dir
import logo from './logo.png';
import NewsPanel from '../NewsPanel/NewsPanel';

class App extends React.Component {
    render(){
        // note className is wrapper of JSX on class
        // you must have only one element, must use div to contain all of them if many
        return (
          <div>
              <img className='logo' src={logo} alt='logo'/>
              <div className='contaioner'>
                <NewsPanel />
              </div>
          </div>  
        );
    };
}

// if you add default here, you don't have to use {App}
export default App;