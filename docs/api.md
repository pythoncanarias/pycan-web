## API version 1

Por el momento la API solo sirve para obtener informacion de eventos.

### API para eventos

Con la API de eventos, como queremos que se pueda usar para cualquier eventos, la primera llamada a
hacer sería:

```
    https://pythoncanarias.es/api/v1/events/
```

Que te daría un listado abreviado de todas los eventos activos en la fecha actual. En este mommento
(11/oct/2019), la llamada devuelve el siguiente json:

```JSON
    {
        "status": "ok",
        "length": 1,
        "result": [
            {
                "event_id": 6,
                "slug": "pydaygc19",
                "name": "PyDay Gran Canaria 2019",
                "start": "2019-11-16",
                "url": "http://pythoncanarias.es/events/pydaygc19/",
                "detail": "/api/v1/events/pydaygc19/"
            }
        ]
    }
```

> Nota: Se pueden obtener _todos_ los eventos, incluyendo los pasados, con `/api/v1/events/all/`.

Todas las llamadas tienen como resultado un Json similar a este, en el sentido de que todas son un
diccionario con, como mínimo, el campo `status`. Si el valor en `status` es `ok`, entonces hay
tambien una entrada `result`, que contendrá el resultado en si de la llamada, y que podrá ser
cualquier contenido Json válido.

Además, puede que se incluyan _opcionalmente_ como metadatos de la respuesta otras entradas en el
diccionario principal (en paralelo a las entradas `status` y `result`). En este caso se incluye un
campo `length`, con valor `1`, inidicando que en el campo de resultados, que es una lista de
eventos, solo hay uno.

El otro valor posible de `status` es cuando hay algun error, en ese caso su valor es el literal
`error`, el campo `result` **NO** esta, y en su lugar hay una entrada `message` con una descripción
del problema que ocasionó el error. Por ejemplo, si intentamos obtener informacion de un evento
inexistente:

```
    https://pythoncanarias.es/api/v1/events/badhashtag/
```

Obtenemos:

```JSON
    {
        "status": "error",
        "message": "Event matching query does not exist."
    }
```

Una vez obtenida la lista de eventos, podemos obtener más información del mismo, usando el valor
en `hashtag` (En este caso `pydaygc19`) o más fácil todavía, usando la URL especificada en
`detail` que sería `/api/v1/events/pydaygc19/`.

Si realizamos una consulta a dicha dirección, obtenemos el siguiente resultado:

```JSON
    {
        "status": "ok",
        "length": 10,
        "result": {
            "event_id": 6,
            "name": "PyDay Gran Canaria 2019",
            "full_url": "http://pythoncanarias.es/events/pydaygc19/",
            "active": true,
            "start_date": "2019-11-16",
            "short_description": "El evento anual de Python m\u00e1s importante que se celebra en Canarias",
            "description": "**PyDay Gran Canaria 2019** es un evento tecnol\u00f3gico organizado por la asociaci\u00f3n [Python Canarias](https://pythoncanarias.es) cuyo principal objetivo es *promover el uso del lenguaje de programaci\u00f3n Python y servir como punto de encuentro de todas aquellas personas interesadas en el mismo*.\r\n\r\nEste evento no ser\u00eda posible sin la inestimable ayuda de la [SPEGC](https://www.spegc.org/formacion-y-eventos/pyday-gran-canaria-2019/) (Sociedad de Promoci\u00f3n Econ\u00f3mica de Gran Canaria) a quien agradecemos especialmente su colaboraci\u00f3n.",
            "venue": "/api/v1/venues/cdtic-innovacion-turistica/",
            "venue": "/api/v1/venues/cdtic-innovacion-turistica/",
            "speakers": "/api/v1/events/PyDayGC19/speakers/",
            "talks": "/api/v1/events/PyDayGC19/talks/",
            "tracks": "/api/v1/events/PyDayGC19/tracks/"
        }
    }
```

y ahora se puede elegir si quieres obtener las charlas ordenadas por ponente (Ordenadas
alfabéticamente por nombre del ponente) en `/api/v1/events/PyDayGC19/speakers/`, por las charlas,
(ordenadas alfabeticamente por título) `/api/v1/events/PyDayGC19/talks/` o agrupada por tracks (y
ordenada por horas), en: `/api/v1/events/PyDayGC19/tracks/`.

Por ejemplo, esta es una versión recortada de la consulta por ponentes:

```JSON
    {
        "status": "ok",
        "length": 13,
        "result": [
            {
                "speaker_id": 28,
                "name": "Alberto",
                "surname": "Ruiz",
                "bio": "Contribuidor del software libre en el \u00e1mbito de GNOME y el escritorio libre durante los \u00faltimos 15 a\u00f1os.\r\nActualmente trabajo en Red Hat como director del equipo de habilitamiento de hardware para portatiles y el stack UEFI y de gesti\u00f3n de arranque para RHEL.",
                "photo": "/media/speakers/speaker/Alberto_Ruiz.jpg",
                "social": {
                    "github": "https://github.com/aruiz",
                    "linkedin": "https://linkedin.com/in/acruiz",
                    "twitter": "https://twitter.com/acruiz"
                },
                "talks": [
                    {
                        "talk_id": 53,
                        "name": "M\u00f3dulos de Python en Rust",
                        "description": "Como hacer un m\u00f3dulo Python usando la API de CPython desde Rust para acelerar c\u00f3digo o acceder a funcionalidades disponibles en Rust.",
                        "start": "11:00",
                        "end": "11:50",
                        "track": "Hoth",
                        "tags": [
                            "api",
                            "core",
                            "meta-programming"
                        ]
                    }
                ]
            },
            
            ... &lt; Entradas omitidas por brevedad &gt;

            {
                "id": 15,
                "name": "Pedro Manuel",
                "surname": "Ramos Rodr\u00edguez",
                "bio": "Graduado en Ingenier\u00eda inform\u00e1tica por la ULL. Full stack developer en Edosoft Factory. Amante de la tecnolog\u00eda y de la ciencia. Curioso por naturaleza y siempre con ganas de aprender. Apasionado de la visualizaci\u00f3n de datos y de la ciencia de datos donde cada d\u00eda intenta aprender m\u00e1s sobre el tema.",
                "photo": "/media/speakers/speaker/pramos_-_Pedro_Ramos.png",
                "social": {
                    "github": "https://github.com/PedroRamosRguez",
                    "linkedin": "https://linkedin.com/in/pedro-ramos-4a5a41135",
                    "twitter": "https://twitter.com/pramos90"
                },
                "talks": [
                    {
                        "talk_id": 63,
                        "name": "Detectando TEA usando Machine Learning",
                        "description": "En la charla se hablar\u00e1 sobre un modelo realizado para la detecci\u00f3n del Trastorno Espectro Autista utilizando algoritmos de machine learning. El objetivo de esta charla, es mostrar que gracias a este tipo de t\u00e9cnicas, es posible ayudar a terapeutas que traten este tipo de trastornos a corroborar sus datos con los del modelo.",
                        "start": "16:30",
                        "end": "17:20",
                        "track": "Hoth",
                        "tags": [
                            "data-science",
                            "machine-learning"
                        ]
                    }
                ]
            }
        ]
    }
```

Además, puedes usar la llamada en la entrada `venue` para obtener información sobre la localización
del evento, incluyendo (Si está en la base de datos), la latitud y longitud de la
ubicación. En este caso, la llamada `/api/v1/venues/cdtic-innovacion-turistica/` devolverá:

```JSON
    {
        "status": "ok",
        "length": 6,
        "result": {
            "vanue_id": 6,
            "name": "CDTIC Innovaci\u00f3n Tur\u00edstica",
            "description": "El Centro Demostrador de las Tecnolog\u00edas de la Informaci\u00f3n y la Comunicaci\u00f3n para la Innovaci\u00f3n Tur\u00edstica (CDTIC Innovaci\u00f3n Tur\u00edstica) facilita a la sociedad local y a las empresas tur\u00edsticas el conocimiento y la adopci\u00f3n de las TIC a trav\u00e9s de diversas actividades.\r\n\r\nSe encuentra dentro del Recinto Ferial (Feria del Atl\u00e1ntico).",
            "address": "Av. de la Feria, 1, 35012 Las Palmas de Gran Canaria, Las Palmas",
            "coords": {
                "lat": 28.1058428,
                "long": -15.4466688
            },
            "photo": "/static/locations/img/noplace.png"
        }
    }
```

Podemos obtener un listado de todas las localizaciones en la base de datos con `/api/v1/vanues/`.


