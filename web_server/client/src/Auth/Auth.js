class Auth {
    /**
     * Authenticate a user. Save a token string in Local Storage
     *
     * @param {string} token
     * @param {string} email
     */
    // localStorage is the browser local storage, it can get and set
    static authenticateUser(token, email) {
      localStorage.setItem('token', token);
      localStorage.setItem('email', email);
    }
  
    /**
     * Check if a user is authenticated - check if a token is saved in Local Storage
     *
     * @returns {boolean}
     */
    // this is not a full authenticate user
    // we only check if the user has token or not, if they don't have, then not authenticated
    // if yes, we will later pass to the server side for real check
    static isUserAuthenticated() {
      return localStorage.getItem('token') !== null;
    }
  
    /**
     * Deauthenticate a user. Remove token and email from Local Storage.
     *
     */
    static deauthenticateUser() {
      localStorage.removeItem('token');
      localStorage.removeItem('email');
    }
  
    /**
     * Get a token value.
     *
     * @returns {string}
     */
    static getToken() {
      return localStorage.getItem('token');
    }
  
    /**
     * Get email.
     *
     * @returns {string}
     */
     static getEmail() {
       return localStorage.getItem('email');
     }
  }
  
  export default Auth;
  