import SignUpForm from './SignUpForm';
import React from 'react';

class SignUpPage extends React.Component {
  constructor() {
    super();

    // set the initial component state.
    this.state = {
      errors: {},
      user: {
        email: '',
        password: '',
        confirm_password: ''
      }
    };
  }

  processForm(event) {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;
    const confirm_password = this.state.user.confirm_password;

    console.log('email:', email);
    console.log('password', password);
    console.log('confirm_password', confirm_password);

    // TODO: post signup data.
  }

  // the name is little ambiguous, this function get applied to every input field
  // whenever user modify anything in the field, it will trigger this function call
  changeUser(event) {
    const field = event.target.name;  // email || password || confirm_password
    const user = this.state.user;
    user[field] = event.target.value;

    this.setState({user});

    const errors = this.state.errors;
    if (this.state.user.password !== this.state.user.confirm_password) {
      errors.password = "Password and Confirm Password don't match.";
    } else {
      errors.password = '';
    }
    this.setState({errors});
  }

  render() {
    return (
      <SignUpForm
       onSubmit={(e) => this.processForm(e)}
       onChange={(e) => this.changeUser(e)}
       errors={this.state.errors}
      />
    );
  }
}


export default SignUpPage;