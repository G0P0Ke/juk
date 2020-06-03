var myMap;

ymaps.ready(init);


function init () {
    myMap = new ymaps.Map('map', {
        center: [55.76, 37.64], // Москва
        zoom: 10,
         controls: ['zoomControl']
    }, {
        searchControlProvider: 'yandex#search'
    });

    add_houses();
}

function add_houses() {
    let all_houses_html = document.getElementsByClassName('all_houses');

    console.log("Длина массива: ", all_houses_html.length)

    for (let i = 0; i < all_houses_html.length; i+=4) {

        ymaps.geocode(['Москва,', all_houses_html[i].value].join(''), {
        results: 1,
        kind: 'house'
        }).then(function (res) {

            var firstGeoObject = res.geoObjects.get(0),
            coords = firstGeoObject.geometry.getCoordinates();
            address = all_houses_html[i].value
            company = all_houses_html[i].name

            var HousePlacemark = new ymaps.Placemark(coords, {
            hintContent: company,
            balloonContent: address
            }, {
                iconLayout: 'default#image',
                iconImageHref: 'https://img2.freepng.ru/20180326/fzw/kisspng-house-logo-home-real-estate-business-home-5ab8bd2d3421a9.5548848215220564932135.jpg', // 1
                //iconImageHref: 'https://www.pngkey.com/png/detail/785-7855984_artificial-grass-family-icon-png-pink.png', //  2
                //iconImageHref: 'img/house.png', // не работает (по необъяснимым причинам)
                iconImageSize: [18, 18],
                iconImageOffset: [-5, -5]
            });

            myMap.geoObjects.add(HousePlacemark);
        });
    }
}