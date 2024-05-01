function toggleDropdown(id_number) {
    var dropdownMenu = document.getElementById("dropdownMenu-" + id_number);
    dropdownMenu.classList.toggle("hidden");
}

window.onclick = function(event) {
    if (!event.target.closest(".relative")) {
        var dropdowns = document.querySelectorAll(".absolute:not(.hidden)");
        dropdowns.forEach(function(dropdown) {
            dropdown.classList.add("hidden");
        });
    }
}