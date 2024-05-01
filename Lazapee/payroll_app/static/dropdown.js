function toggleDropdown() {
    var dropdownMenu = document.getElementById("dropdownMenu");
    dropdownMenu.classList.toggle("hidden");
}

window.onclick = function(event) {
    if (!event.target.closest(".relative")) {
        var dropdowns = document.querySelectorAll(".relative > .show");
        dropdowns.forEach(function(dropdown) {
            dropdown.classList.add("hidden");
        });
    }
}