var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].onclick = function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.maxHeight){
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
        }
    }
}

function barFunction(x) {
    /* Change aspect of the menu button */
    x.classList.toggle("change");
    if (document.getElementById("sidenav").offsetWidth == "0") {
        /* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
        document.getElementById("sidenav").style.width = "250px";
        document.getElementById("menu3Bar").style.left = "250px";
    }
    else {
        /* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
        document.getElementById("sidenav").style.width = "0";
        document.getElementById("menu3Bar").style.left = "0";
    }
}
