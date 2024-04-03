
var cockpitPocketElements = document.querySelectorAll(".cockpitPocketName");
cockpitPocketElements.forEach(function (element) {
    element.addEventListener("click", function () {
        var pocketName = this.textContent.trim(); // Pobieranie nazwy Konta
        var urlName = this.getAttribute('data-url') + "?pocket_name=" + encodeURIComponent(pocketName);
        window.location.href = urlName;
        });
});