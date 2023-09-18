# conmebol-api
CONMEBOL API te permite obtener información de los resultados, clasificación y próximos partidos referentes a la clasificación de la CONMEBOL para la Copa América.

los datos se obtienen de [onefootball](https://onefootball.com/en/home)

## URL Base
```
https://conmebol-api.vercel.app/
```

## Endpoints
`GET /`: Muestra un mensaje de bienvenida y proporciona un enlace a la documentación de la API.

`GET /api/classification`: Permite obtener las clasificaciones de los países que forman parte de la CONMEBOL.

`GET /api/results`: Permite obtener los resultados de las últimas jornadas de los partidos jugados en la CONMEBOL.

`GET /api/matches`: Permite obtener información sobre los próximos partidos de la CONMEBOL y los partidos que se están jugando en vivo.

### Uso
En el siguiente enlace devolverá un objeto json de los resultados de los últimos días de los partidos jugados.

```
https://conmebol-api.vercel.app/api/results
```