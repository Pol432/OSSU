function open_content() {
    const leftBand = document.getElementById("left-band");
    const rightBand = document.getElementById("right-band");
    leftBand.setAttribute("style", "left: -50%");
    rightBand.setAttribute("style", "right: -50%");
}

document.addEventListener("DOMContentLoaded", open_content())