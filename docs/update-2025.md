## Relación de cambios realizados en 2025

- Todas las páginas tienen ahora una ruta de migas de pan (_breadcrumbs_) indicando
la ruta jerárquica dentro de la web.

- Python se ha actualizado a ...

- Django se ha actualizado a ....

- La base de datos se ha actualizado a Postgres16.

- El sistema de pagos se ha paasado a GoCardless ? (Tentativa)

- Font awesome se ha actualizado a 5.10.2. Se descarga además de forma local.

- Como la base de datos estaba en una versión de postgres muy
  antigua, los formatos de exportación / importación daban algunos
  problemas. Se implemento una exportación propia, usando ``dumpdata`
  y ``loaddata``.

- Todas las operaciones realizadas en js en el servidor se han eliminado o
  reemplazado:

    - Compresión de css: Lo realiza el servidor de forma automática.

    - Ofuscación del código: Eliminada, ya que todo el código está en claro en el
      repositorio de todas maneras.

    - Cacheo de versiones de los recursos estáticos. Eliminado por ahora. Hay paquetes
      específicos de django para resolverlo.

  En otras palabras, ya no hay que instalar node, npm, etc.


- Eventos:

  - La página única de detalles de un evento se ha dividido en varias
    páginas separadas, cada una enfocada en un aspecto del evento.

    - Ponentes (``speakers``)



