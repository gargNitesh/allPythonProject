/**
 * author : Komal Jain
 */

function submitLogin() {
	document.getElementById("LoginForm").action = "userLogin";
	document.getElementById("LoginForm").method = "post"; 
	document.getElementById("LoginForm").submit();
}

