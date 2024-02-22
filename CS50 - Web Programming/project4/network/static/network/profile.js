document.addEventListener("DOMContentLoaded", follow());

function follow() {
    let button = document.getElementById("follow");
    let user_id = button.getAttribute("data-userID");

    fetch(`/profile_view/${user_id}`)
    .then(response => response.json())
    .then(data => {
        let profile = data.profile_user;
        if (profile.id == data.user || !data.user) { return; }
        button.style.display = "block";
        console.log(data.following);

        if (data.following) {
            button.innerHTML = "Unfollow";
        } else {
            button.innerHTML = "Follow";
        }

        button.onclick = follow_button;
    })
}

function follow_button() {
    let button = document.getElementById("follow");
    let action = button.innerHTML;
    let id = button.getAttribute("data-userID");

    fetch(`/follow?following=${id}&action="${action}"`)
    .then(() => {
        if (action == "Follow") {
            button.innerHTML = "Unfollow";
        } else {
            button.innerHTML = "Follow";
        }
        window.location.reload();
    })
}