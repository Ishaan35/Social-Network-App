likePost = async () => {
  let button = window.event.target;
  let liked = button.getAttribute("liked") == "true" ? true : false;
  let id = button.id;

  await fetch(`likePost/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      like: !liked,
    }),
    headers: { "X-CSRFToken": getCookie("csrftoken") },
  });

  await fetch(`likePost/${id}`)
    .then((data) => data.json())
    .then((d) => {
      console.log(document.getElementById(`numLikes:${id}`).innerHTML);
      document.getElementById(`numLikes:${id}`).innerHTML = d.Likes;
      document.getElementById(`${id}`).setAttribute("liked", `${!liked}`);
      document.getElementById(`${id}`).innerHTML =
        liked == false
          ? `<i class="far fa-thumbs-down" style="font-size: xx-large; color: #ff4343;"></i> 
                                <label style="margin-left: 10px; margin-top: 5px; pointer-events:none; color: gray;">Unlike</label>`
          : `<i class="far fa-thumbs-up" style="font-size: xx-large; color: #19a7ff;"></i>
                                <label style="margin-left: 10px; margin-top: 10px; pointer-events:none; color: gray;">Like</label>`;
      document.getElementById(`${id}`).className =
        liked == false ? "likebtn" : "likebtn";
    });
};

follow = async (id) => {
  let button = window.event.target;
  let following = button.getAttribute("following") == "true" ? true : false;

  await fetch(`follow/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      following: !following,
    }),
    headers: { "X-CSRFToken": getCookie("csrftoken") },
  });

  await fetch(`follow/${id}`)
    .then((data) => data.json())
    .then((d) => {
      document.getElementById(`numFollowers:${id}`).innerHTML = d.followers;
      document
        .getElementById(`followBtn:${id}`)
        .setAttribute("following", `${!following}`);

      document.getElementById(`followBtn:${id}`).innerHTML =
        following == false ? "Unfollow" : "Follow";
      document.getElementById(`followBtn:${id}`).className =
        following == false ? "btn-danger" : "btn-primary";

      console.log(d);
    });
};

enableEdit = (id) => {
  id = parseInt(id);
  document.getElementById(`EditPostDiv:${id}`).hidden = false;
  document.getElementById(`EditPost:${id}`).hidden = true;

  let existingText = document.getElementById(`PostBody:${id}`).innerHTML;
  document.getElementById(`PostBody:${id}`).hidden = true;

  document.getElementById(`EditPostTextarea:${id}`).value = existingText;
};

edit = async (id) => {
  await fetch(`editPost/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      newBody: document.getElementById(`EditPostTextarea:${id}`).value,
    }),
    headers: { "X-CSRFToken": getCookie("csrftoken") },
  });

  await fetch(`editPost/${id}`)
    .then((data) => data.json())
    .then((d) => {
      body = d.body;

      document.getElementById(`EditPostTextarea:${id}`).value = "";
      document.getElementById(`EditPostDiv:${id}`).hidden = true;
      document.getElementById(`EditPost:${id}`).hidden = false;
      document.getElementById(`PostBody:${id}`).hidden = false;
      document.getElementById(`PostBody:${id}`).innerHTML = body;
    });
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
