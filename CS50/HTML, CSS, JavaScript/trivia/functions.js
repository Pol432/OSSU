// Functions that edits buttons whether is correct or incorrect
function wrong(id){
    var button = document.getElementById(id);
    button.style.backgroundColor = "red";
    button.textContent = "Incorrect"
}
function correct(id){
    var button = document.getElementById(id);
    button.style.backgroundColor = "green";
    button.textContent = "Correct!"
}

// Function that edits the text of the free response
function check(){
    let answer = document.getElementById("user_input").value;
    answer = answer.toLowerCase();
    if (answer == "mice")
    {
        document.getElementById("user_input").style.backgroundColor = "green";
        document.getElementById("free_correct").hidden = false;
    }
    else
    {
        document.getElementById("user_input").style.backgroundColor = "red";
        document.getElementById("free_incorrect").hidden = false;
    }
}