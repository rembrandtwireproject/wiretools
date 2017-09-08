// Reading saved image
function getImage() {
    var dataImage = localStorage.getItem('imgData');
    bannerImg = document.getElementById('uploadedImage');
    bannerImg.src = "data:image/png;base64," + dataImage;
}

// Temporaily save image on the server
function save() {
    bannerImage = document.getElementById('uploadedImage');
    imgData = getBase64Image(bannerImage);
    localStorage.setItem("imgData", imgData);   
}

// Reading uploaded image
function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    var dataURL = canvas.toDataURL("image/png");

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

// For showing image editor
function showEditor() {
    document.getElementById('editor').style.display = "block";
    document.getElementById('flipButton').style.display = "block";
}