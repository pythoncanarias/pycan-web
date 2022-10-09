## Sobre el servidor de cache

Lo más sencillo sería usar `memcached`, pero en nuestro caso creo que tiene más
sentido usar `redis` porque ya está instalada en producción y el rendimiento
es similar. Eso si, hay que instalar `django-redis`, que ya está en el fichero
`requiremenst.txt`:


### Configurar la cache

Hay que habilitar la configuración, en el fichero `settings.py`, para que
reconozca _Redis_ como caché por defecto. Este sería un ejemplo de configuración:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "web"
    }
}
```

El campo `KEY_PREFIX`, si se define, se añade automáticamente a todos las
claves que se almacenan en _Redis_. He puesto `web` para hacer una "espacio de
nombres" para todo lo que sea web.

Si queremos optimizar el uso de la caché, podemos añadir un `signal` a los
modelos para que se borre la caché cada vez que se cambien los datos.  Esto lo
usamos para cachear los datos de la organización (Para más detalles ver
`apps\organizations\models.py`).

### Desarrollo local

Para no complicar el desarrollo, se puede indicar en la configuración que use
la memoria local de la máquina a modo de cache. Así no hay que instalar
_Redis_, si no queremos.

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

