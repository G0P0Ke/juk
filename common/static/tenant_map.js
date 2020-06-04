var myMap;
var myPlacemark;

function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

// Определяем адрес по координатам (обратное геокодирование).
function getAddress(coords) {
    myPlacemark.properties.set('iconCaption', 'поиск...');
    ymaps.geocode(coords).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0);
        myPlacemark.properties.set({
            // Формируем строку с данными об объекте.
            iconCaption: [
            // Название населенного пункта или вышестоящее административно-территориальное образование.
            firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
            // Получаем путь до топонима, если метод вернул null, запрашиваем наименование здания.
            firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
            ].filter(Boolean).join(', '),

            // В качестве контента балуна задаем строку с адресом объекта.
            balloonContent: firstGeoObject.getAddressLine()
        });
    });
}

ymaps.ready(init);


function init () {
    myMap = new ymaps.Map('map', {
        center: [55.76, 37.64], // Москва
        zoom: 10,
         controls: ['zoomControl']
    }, {
        searchControlProvider: 'yandex#search'
    });

    from_form_to_map()

    myMap.events.add('click', function (e) {
        var coords = e.get('coords');

        // Если метка уже создана – просто передвигаем ее.
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        getAddress(coords);
    });
}

function from_form_to_map() {
    let address = document.getElementById('address-id');

    ymaps.geocode(address.value, {
        results: 1,
        kind: 'house'
    }).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0),

        coords = firstGeoObject.geometry.getCoordinates()
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
            myPlacemark.properties.set({
                balloonContent: firstGeoObject.getAddressLine()
            });
        }
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        getAddress(coords);

        // Область видимости геообъекта.
        bounds = firstGeoObject.properties.get('boundedBy');
        myMap.setBounds(bounds, {
            // Проверяем наличие тайлов на данном масштабе.
            checkZoomRange: true
        });

        console.log('Адрес геообъекта: ', firstGeoObject.getAddressLine());
        address.value = firstGeoObject.getAddressLine()
    });
}

function from_map_to_form() {
    coords = myPlacemark.geometry.getCoordinates()

    ymaps.geocode(coords).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0);

        console.log('Адрес геообъекта: ', firstGeoObject.getAddressLine());

        let address = document.getElementById('address-id');
        address.value = firstGeoObject.getAddressLine()
    });
}