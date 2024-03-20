

function openForm() {
    document.getElementById("buyForm").style.display = "block";
    document.getElementById("overlay").classList.add("show");  // Dodaj klasę 'show'
    document.body.style.overflow = 'hidden'; // Zablokuj przewijanie strony
}

function closeForm() {
    document.getElementById("buyForm").style.display = "none";
    document.getElementById("overlay").classList.remove("show");  // Usuń klasę 'show'
    document.body.style.overflow = 'auto'; // Odblokuj przewijanie strony
}

