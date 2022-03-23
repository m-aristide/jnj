var inputphoto;
var img_photo;
var button;
var new_image = true;
var resizephoto;
var resultelt;

window.addEventListener('DOMContentLoaded', function () {

    inputphoto = document.getElementById('formFile');
    
    resizephoto = document.getElementById('resizephoto');

    button = document.getElementById('button');

    resultelt = document.getElementById('result');

    inputphoto.onchange = image_load

});

function image_load() {
    if(img_photo) {
        img_photo.remove();
    }
    img_photo = document.createElement('img');
    img_photo.style.width = '50%';

    if(!new_image) {
        button.style.display = 'block';
    }

    if (inputphoto.files && inputphoto.files[0]) {
        if(inputphoto.files[0].size > 2097152) {
            inputphoto.files = undefined;
            var span_size_file = document.createElement('span');
            span_size_file.style.color = '#f00';
            span_size_file.textContent = 'La taille de l\'image dépasse la taille maximale autorisée de 2Mo';
            resultelt.appendChild(span_size_file)
            return
        } else if (resultelt.hasChildNodes()) {
            resultelt.removeChild(resultelt.firstChild)
        }
        
        var reader = new FileReader();
        reader.onload = function (e) {
            img_photo.src = e.target.result;
            resultelt.appendChild(img_photo)
            go_crop();
        }
        reader.readAsDataURL(inputphoto.files[0]);
    }
}

function getRoundedCanvas(sourceCanvas) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var width = sourceCanvas.width;
    var height = sourceCanvas.height;

    canvas.width = width;
    canvas.height = height;
    context.imageSmoothingEnabled = true;
    context.drawImage(sourceCanvas, 0, 0, width, height);
    context.globalCompositeOperation = 'destination-in';
    context.beginPath();
    context.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, 2 * Math.PI, true);
    context.fill();
    return canvas;
}

function go_crop() {

    console.log('change')
    button.style.display = 'block';

    var croppable = false;
    var cropper = new Cropper(img_photo, {
        aspectRatio: 1,
        viewMode: 1,
        ready: function () {
            croppable = true;
        },
    });

    button.onclick = function () {
        var croppedCanvas;
        if (!croppable) {
            return;
        }
        // Crop
        croppedCanvas = cropper.getCroppedCanvas();
        // Round
        new_image = false;
        inputphoto.files = undefined
        img_photo.src = getRoundedCanvas(croppedCanvas).toDataURL();
        resizephoto.value = img_photo.src;
        img_photo.classList.remove('cropper-hidden');
        button.style.display = 'none';
        document.getElementsByClassName('cropper-container')[0].remove();
    };
}

function submit_form() {
    var form = document.getElementById('form_part');
    form.onsubmit = function(e) {
        document.getElementById('spinner').style.display = 'block';
        document.getElementById('form_part').scrollIntoView();
    }
}