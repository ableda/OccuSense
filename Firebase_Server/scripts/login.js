(function() {
    
    "use strict";
	
      // Set the configuration for your app
  // TODO: Replace with your project's config object
  var config = {
    apiKey: "AIzaSyAmuxjc6J8Lwpuh4jDyKsQq0jiu_5SYnAU",
    authDomain: "occusense-f77ec.firebaseapp.com",
    databaseURL: "https://occusense-f77ec.firebaseio.com",
    storageBucket: "bucket.appspot.com"
  };
  firebase.initializeApp(config);
  

  // Get a reference to the database service
  var database = firebase.database();
    const auth = firebase.auth();
	
    
    const btnLogin = document.getElementById('loginbtn');
    
    btnLogin.addEventListener('click', e => {
      const txtEmail = document.getElementById('lg_username');
      const email = txtEmail.value;
      const txtPassword = document.getElementById('lg_password');
      const pass = txtPassword.value;
      const auth = firebase.auth();
      //Sign in
      const promise = auth.signInWithEmailAndPassword(email, pass);
      promise.catch(e => console.log(e.message));
      console.log("logged in!");
    })

});