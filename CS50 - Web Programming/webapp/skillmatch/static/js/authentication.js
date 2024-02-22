window.onload = function() {
  if (window.performance) {
      if (performance.navigation.type == 1) {
          location.reload();
      }
  }
};

const checkboxes = document.querySelectorAll('input[type="checkbox"]')
checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('click', () => {
        checkboxes.forEach((otherCheckbox) => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false
            }
        })
    })
})

var login_form = document.getElementById("login_form");
var register_form = document.getElementById("register_form");
var authentication = document.getElementById("authentication")

function fadeOut(el) {
    el.style.opacity = 1;

    (function fade() {
        if ((el.style.opacity -= 0.1) < 0) {
        el.style.display = "none";
        } else {
        requestAnimationFrame(fade);
        }
    })();
}

function fadeIn(el, display) {
    el.style.opacity = 0;
    el.style.display = display || "block";

    (function fade() {
        var val = parseFloat(el.style.opacity);
        if (!((val += 0.1) > 1)) {
        el.style.opacity = val;
        requestAnimationFrame(fade);
        }
    })();
}

function auth() {
    const nav_bar = document.getElementById("band_menu");
    nav_bar.remove()

    const login_switch = document.getElementById("login_switch");
    const register_switch = document.getElementById("register_switch");

    login_switch.onclick = login_view;
    register_switch.onclick = register_view;

    console.log(authentication.dataset.form)
    if (authentication.dataset.form == "login") {
        login_form.style.display = "block";
        register_form.style.display = "none";
    } else {
        login_form.style.display = "none";
        register_form.style.display = "block";
    }
}

function login_view() {
    if (register_form.style.display !== "none") {
        fadeOut(register_form);
        setTimeout(() => {
            fadeIn(login_form);
        }, 600);
    }
}

function register_view() {
    if (login_form.style.display !== "none") {
        fadeOut(login_form);
        setTimeout(() => {
            fadeIn(register_form);
        }, 600);
    }
}

document.addEventListener("DOMContentLoaded", auth());