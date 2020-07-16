function on() {
    document.getElementById("overlay").style.display = "block";
}

function onservice() {
    $("#overlayservice").fadeIn('0.1');
    document.getElementById("overlayservice").style.display = "block";

}

function off() {
    $("#overlayservice").fadeOut('0.1');
    document.getElementById("overlay").style.display = "none";
    //document.getElementById("overlayservice").style.display = "none";
    document.getElementById("overlaytraining").style.display = "none";

}

function ontraining() {
    document.getElementById("overlaytraining").style.display = "Block";
}