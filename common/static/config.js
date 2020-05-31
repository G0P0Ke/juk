var myMap;

ymaps.ready(init);


function init () {
    myMap = new ymaps.Map('map', {
        center: [55.76, 37.64],
        zoom: 10,
         controls: ['zoomControl']
    }, {
        searchControlProvider: 'yandex#search'
    });


    let all_houses_html = document.getElementsByClassName('all_houses');
    console.log("Длина массива: ", all_houses_html.length);

    for (let i = 0; i < all_houses_html.length; i++) {
        ymaps.geocode(all_houses_html[i].value, {
        results: 1,
        }).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            all_houses_html[i].value = firstGeoObject.getAddressLine();
        });
    }
}
