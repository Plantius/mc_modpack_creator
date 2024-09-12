function toggleDiv(id) {
    var div = document.getElementById(id);
    console.log(div.style.display)
    div.style.display = div.style.display == "none" || div.style.display == "" ? "block" : "none";
}

var button = document.getElementById("save_project");
button.addEventListener("click", function(){
    toggleDiv("save_slug")
});