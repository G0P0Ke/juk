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
    let address = document.getElementById('address-id');
    console.log(address.value)

    ymaps.geocode(address.value, {

    results: 1

    }).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0),
                // Область видимости геообъекта.
            bounds = firstGeoObject.properties.get('boundedBy');

            firstGeoObject.options.set('preset', 'islands#darkBlueDotIconWithCaption');
            // Получаем строку с адресом и выводим в иконке геообъекта.
            firstGeoObject.properties.set('iconCaption', firstGeoObject.getAddressLine());

            // Добавляем первый найденный геообъект на карту.
            myMap.geoObjects.add(firstGeoObject);
            // Масштабируем карту на область видимости геообъекта.
            myMap.setBounds(bounds, {
                // Проверяем наличие тайлов на данном масштабе.
                checkZoomRange: true
            });
    });
}

function refind() {
    let address = document.getElementById('address-id');
    console.log(address.value)

    ymaps.geocode(address.value, {
        results: 1
        }).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0),
                // Область видимости геообъекта.
            bounds = firstGeoObject.properties.get('boundedBy');

            firstGeoObject.options.set('preset', 'islands#darkBlueDotIconWithCaption');
            // Получаем строку с адресом и выводим в иконке геообъекта.
            firstGeoObject.properties.set('iconCaption', firstGeoObject.getAddressLine());

            // Добавляем первый найденный геообъект на карту.
            myMap.geoObjects.add(firstGeoObject);
            // Масштабируем карту на область видимости геообъекта.
            myMap.setBounds(bounds, {
                // Проверяем наличие тайлов на данном масштабе.
                checkZoomRange: true
            });
        });
}
