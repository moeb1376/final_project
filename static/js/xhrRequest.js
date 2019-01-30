$("#camScanner").click(function () {
    let upload_url = $("#upload_url").val();
    console.log(upload_url);
    $.ajax({
        url: '/xhrTest',
        data: {
            'method': "cam",
            'url': upload_url
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            alert("salam");
        }
    });
});
$("#map").click(function () {
    let upload_url = $("#upload_url").val();
    $.ajax({
        url: '/xhrTest',
        data: {
            'method': "map",
            'url': upload_url
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            if (data.images) {
                let a = document.getElementById("test");
                let images = data.images;
                images.forEach(image => {
                    a.innerHTML += `<a class="" href="#"><img src="/static/${image}"></a>`;
                });
                document.addEventListener('DOMContentLoaded', function () {
                    var elems = document.querySelectorAll('.carousel');
                    var options = {indicators: true, fullWidth: true};
                    var instances = M.Carousel.init(elems, options);
                });
            }
        }
    });
});