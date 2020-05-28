var myMap;
var myPlacemark;
let type;
let js_address;

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

    add_houses()

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

function add_houses() {
    let all_houses_html = document.getElementsByClassName('all_houses');

    console.log("Длина массива: ", all_houses_html.length)

    var myCollection = new ymaps.GeoObjectCollection(),
    myPoints = []

    for (let i = 0; i < all_houses_html.length; i++) {
        ymaps.geocode(all_houses_html[i].value, {
        results: 1,
        kind: 'house'
        }).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0),
            coords = firstGeoObject.geometry.getCoordinates();
            address = all_houses_html[i].value

            console.log(coords, address)

            firstGeoObject.options.set('preset', 'islands#redCircleIcon');

            myMap.geoObjects.add(firstGeoObject);
        });
    }
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

        type = firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData.kind');
        console.log('Тип геообъекта: %s', type);

        console.log('Адрес геообъекта: ', firstGeoObject.getAddressLine());
        address.value = firstGeoObject.getAddressLine()
        js_address = address.value
    });
}

function from_map_to_form() {
    coords = myPlacemark.geometry.getCoordinates()

    ymaps.geocode(coords).then(function (res) {
        var firstGeoObject = res.geoObjects.get(0);

        console.log('Адрес геообъекта: ', firstGeoObject.getAddressLine());

        type = firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData.kind');
        console.log('Тип геообъекта: %s', type);

        let address = document.getElementById('address-id');
        address.value = firstGeoObject.getAddressLine();
        js_address = address.value
    });
}


function is_house_check() {
    let address = document.getElementById('address-id');
    let answer = document.getElementById('is_house-id');

    if (type == 'house') {
        if (js_address == address.value) {
            console.log('ДОМ');
            answer.value = 1
        }
    }
    else {
        console.log('НЕДОМ');
        answer.value = 0
    }
}
