// Logic
import Auth from '../Auth/Auth';
import React from 'react';
import LoginForm from './LoginForm';
import PropTypes from 'prop-types'

class LoginPage extends React.Component {
    // I think in all documentations constructor() only has 1 arg, which is props
    // to make it possible to use context.router, we have to at the end of the page
    // use ProtoTypes.

    constructor(props, context) {
        super(props, context);

        // init component
        this.state = {
            errors: {},
            user: {
                email: '',
                password: ''
            }
        };
    }

    render() {
        return (
            <LoginForm
            onSubmit = {(e)=> this.processForm(e)}
            onChange = {(e)=> this.changeUser(e)}
            errors={this.state.errors}
            />
        );
    }

    processForm(event) {
        // cannot let you do the post request and reload page
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;

        console.log('email:', email);
        console.log('password', password);
        // post login 
        const url = 'http://' + window.location.hostname + ':3000' + '/auth/login';
        const request = new Request(
          url,
          {
            method:'POST', headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.state.user.email,
            password: this.state.user.password
          })
        });

        fetch(request).then(response => {
            // this 200 means post request succeed, authentication passed on backend
            if (response.status === 200) {
              this.setState({
                errors: {}
              });
      
              response.json().then(json => {
                console.log(json);
                // here we just store the token on local browser
                Auth.authenticateUser(json.token, email);
                this.context.router.replace('/');
              });
            } else {
              console.log('Login failed');
              response.json().then(json => {
                const errors = json.errors ? json.errors : {};
                errors.summary = json.message;
                this.setState({errors});
              });
            }
          });

    }

    // this event is system generate for us
    // change this.user whenever there is change
    changeUser(event) {
        const field = event.target.name; // either email or password, defined in html
        const user = this.state.user;
        user[field] = event.target.value;
        this.setState({user})
    }
}

// To make react-router work
LoginPage.contextTypes = {
    router: PropTypes.object.isRequired
  };


export default LoginPage;