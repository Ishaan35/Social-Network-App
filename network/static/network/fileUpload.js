function setFileValue() {
  let file = document.getElementById("profilePicInput").files[0];
  let name = file.name;

  const objectURL = URL.createObjectURL(file);

  let image = `<img src='${objectURL}' height='30px' width='30px' style='margin-right:15px; border-radius:5px'>`;

  document.getElementById(
    "fileNameDisplay"
  ).innerHTML = `<div class='fileNameDiv'> ${image} ${name}</div>`;
}

function setFilePreviewPost() {
  let file = document.getElementById("postPictureInput").files[0];
  let name = file.name;

  const objectURL = URL.createObjectURL(file);

  document.getElementById("uploadedPostImageInput").src = objectURL;
}
