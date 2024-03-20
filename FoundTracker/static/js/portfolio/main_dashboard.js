
console.log("main_dashboard.js is connected");
var cockpitPocketElements = document.querySelectorAll(".cockpitPocketName");
cockpitPocketElements.forEach(function (element) {
    element.addEventListener("click", function () {
        var urlName = this.getAttribute('data-url');
        window.location.href = urlName;
        });
});