let video = document.getElementById('video');
let canvas = document.getElementById("canvas");
let click_button = document.querySelector("#click-photo");


/**
 * Enable the camera functionality
 */
async function sendFace()
{
    
    let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
	video.srcObject = stream;
}

/**
 * Take the image, then upload it to the server.
 */
async function takePic()
{
    // Save the image to the canvas element
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let image_data_url = canvas.toDataURL('image/jpeg');
    var file = dataURItoBlob(image_data_url);

    // upload the image to the server.
    const url = '/api';
    const data = new FormData();
    data.append('image', file);

    const response = await fetch(url, {
        method: 'post',
        body: data,
    });

    // wait for the response
    const responseText = await response.text();
    console.log(responseText);
    
    if (responseText == '0'){
        alert('You are not Paul Sweeney')
    }

    else{
        alert('Welcome, Paul Sweeney')
    }
}

/**
 * Convert a data uri to a blob object
 */
function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);
    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ia], {type:mimeString});
    }
