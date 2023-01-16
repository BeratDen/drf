const loginForm = document.getElementById("login-form");
const baseEndpoint = "http://localhost:8000/api/";
if (loginForm) {
  //handle form
  loginForm.addEventListener("submit", handleLogin);
}

function handleLogin(event) {
  event.preventDefault();
  const loginEndPoint = `${baseEndpoint}/token/`;
  let loginFormData = new FormData(loginForm);
  let loginObjectData = Object.fromEntries(loginFormData);
  let bodyString = JSON.stringify(loginObjectData);
  const opitons = {
    method: "POST",
    Headers: {
      ContentType: "application/json",
    },
    body: bodyString,
  };
  fetch(loginEndPoint, opitons) // request.post
    .then((response) => {
      console.log(response);
      return response.json();
    })
    .then((x) => {
      console.log(x);
    })
    .catch((err) => {
      console.log(err);
    });
}
