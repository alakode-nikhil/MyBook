function regAlert() {

    var un = document.getElementById('username').value;
    var fn = document.getElementById('first_name').value;
    var ln = document.getElementById('last_name').value;
    var email = document.getElementById('email').value;
    var pass = document.getElementById('pass').value;
    var cpass= document.getElementById('cpass').value;


    if (!un || !fn || !ln || !email || !pass || !cpass){
        alert('Enter all credentials');
        return;
    }

    alert('Registration sucessfull');
}

function loginAlert() {

    var un = document.getElementById('username').value;
    var pass = document.getElementById('pass').value;



    if (!un || !pass){
        alert('Enter all credentials');
        return;
    }

    alert('LOGIN sucessfull');
}