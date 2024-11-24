function fetchServer() {
  const logout = true;
  fetch(`/home/:${logout}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      window.location.href = "/";
    })
    .catch((err) => {
      console.error(err);
    });
}
