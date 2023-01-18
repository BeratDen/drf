const contentContainer = document.getElementById("content-container");
const loginForm = document.getElementById("login-form");
const searchForm = document.getElementById("search-form");
const baseEndpoint = "http://localhost:8000/api";
if (loginForm) {
  //handle form
  loginForm.addEventListener("submit", handleLogin);
}
if (searchForm) {
  searchForm.addEventListener("submit", handleSearch);
}

function handleLogin(event) {
  event.preventDefault();
  const loginEndpoint = `${baseEndpoint}/token/`;
  let loginFormData = new FormData(loginForm);
  let loginObjectData = Object.fromEntries(loginFormData);
  let bodyStr = JSON.stringify(loginObjectData);
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: bodyStr,
  };
  fetch(loginEndpoint, options) //  Promise
    .then((response) => {
      return response.json();
    })
    .then((authData) => {
      console.log("authdata");
      handleAuthData(authData, getProductList);
    })
    .catch((err) => {
      console.log("err", err);
    });
}
function handleSearch(event) {
  event.preventDefault();
  let formData = new FormData(searchForm);
  let data = Object.fromEntries(formData);
  let searchParams = new URLSearchParams(data);
  const endpoint = `${baseEndpoint}/search/?${searchParams}`;
  const headers = {
    "Content-Type": "application/json",
  };
  const AuthToken = localStorage.getItem("access");
  if (AuthToken) {
    headers["Authorization"] = `Bearer ${AuthToken}`;
  }
  const options = {
    method: "GET",
    headers: headers,
  };
  fetch(endpoint, options) //  Promise
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const validData = isTokenNotValid(data);
      if (validData && contentContainer) {
        contentContainer.innerHTML = "";
        if (data && data.hits) {
          let htmlStr = "";
          for (let result of data.hits) {
            htmlStr += "<li>" + result.title + "</li>";
          }
          contentContainer.innerHTML = htmlStr;
          console.log(data.hits);
          if (data.hits.length === 0) {
            console.log("test");
            contentContainer.innerHTML = "<p>No Result Found</p>";
          }
        } else {
          contentContainer.innerHTML = "<p>No Result Found</p>";
        }
      }
    })
    .catch((err) => {
      console.log("err", err);
    });
}

function validateJWTToken() {
  //fetch
  const endpoint = `${baseEndpoint}/token/verify/`;
  const options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      token: localStorage.getItem("access"),
    }),
  };
  fetch(endpoint, options)
    .then((respone) => respone.json())
    .then((x) => {
      //refresh token if false clear local and raise alert
      console.log(x);
      isTokenNotValid();
    });
}

function handleAuthData(authData, callback) {
  console.log(authData.access);
  localStorage.setItem("access", authData.access);
  localStorage.setItem("refresh", authData.refresh);
  if (callback) {
    callback();
  }
}

function writeToContainer(data) {
  if (contentContainer) {
    contentContainer.innerHTML =
      "<pre>" + JSON.stringify(data, null, 4) + "</pre>";
  }
}

function getFetchOptions(method, body) {
  return {
    method: method === null ? "GET" : method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
    body: body ? body : null,
  };
}

function isTokenNotValid(jsonData) {
  if (jsonData.code && jsonData.code === "token_not_valid") {
    //run a refresh token pattern
    alert("Your Token Not Valid Please Login Again");
    return false;
  }
  return true;
}

function getProductList() {
  const endpoint = `${baseEndpoint}/products/`;
  const options = getFetchOptions();
  fetch(endpoint, options)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const validData = isTokenNotValid(data);
      if (validData) {
        writeToContainer(data);
      }
    });
}

validateJWTToken();
// getProductList();

const searchClient = algoliasearch(
  "EDK95X8MAM",
  "f3c74714ba0c232b1cea6be123c4ae2d"
);

const search = instantsearch({
  indexName: "brt_Product",
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: "#searchbox",
  }),

  instantsearch.widgets.clearRefinements({
    container: "#clear-refinements",
  }),

  instantsearch.widgets.refinementList({
    container: "#user-list",
    attribute: "user",
  }),

  instantsearch.widgets.refinementList({
    container: "#tags-list",
    attribute: "get_tags_list",
  }),

  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: `<a href={{ endpoint }}> <div> {{ title }} <p> {{ user }} </p>  <p> \${{ price }} </p>  </div> </a>`,
    },
  }),
]);

search.start();
