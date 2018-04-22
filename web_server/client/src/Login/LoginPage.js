// Logic

import React from 'react';
import LoginForm from './LoginForm';

class LoginPage extends React.Component {
    constructor() {
        super();

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
        event.preventDedault();

        const email = this.state.user.email;
        const password = this.state.user.password;

        console.log('email:', email);
        console.log('password', password);
        // TODO: post login 
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

export default LoginPage;