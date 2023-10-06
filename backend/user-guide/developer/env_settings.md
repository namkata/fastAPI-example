### Settings provided by `Settings`:

When initialized, `Settings` reads the following environment variables into the specified attributes:

Environment Variable        | Attribute Name        | Type   | Default Value                                        | Descriptions
--------------------------- |-----------------------|--------|------------------------------------------------------| -----------
`APP_DEBUG`                 | `debug`               | `bool` | `False`                                              | 
`APP_DOCS_URL`              | `docs_url`            | `str`  | `"/docs`                                             |
`APP_OPENAPI_PREFIX`        | `openapi_prefix`      | `str`  | `""`                                                 |
`APP_OPENAPI_URL`           | `openapi_url`         | `str`  | `"/openapi.json"`                                    | 
`APP_REDOC_URL`             | `redoc_url`           | `str`  | `"/redoc"`                                           |
`APP_TITLE`                 | `title`               | `str`  | `"FastAPI"`                                          |
`APP_VERSION`               | `version`             | `str`  | `"0.1.0"`                                            |
`APP_DISABLE_DOCS`          | `disable_docs`        | `bool` | `False`                                              |
`APP_API_STR`               | `api_str`             | `str`  | `api/v1`                                             |
`APP_SECRET_KEY`            | `secret_key`          | `str`  | `secrets.token_urlsafe(32)` # Random                 |
`APP_SERVER_DOMAIN`         | `sever_domain`        | `str`  | `http://127.0.0.1:8000`                              |
`APP_ACCEPT_CORS_ORIGINS`   | `accept_cors_origins` | `list` | `["http://localhost:3000", "http://127.0.0.1:3000"]` |
`APP_CELERY_BROKER`   | `disable_docs`        | `bool` | `False`                                              |
`APP_DISABLE_DOCS`   | `disable_docs`        | `bool` | `False`                                              |
`APP_DISABLE_DOCS`   | `disable_docs`        | `bool` | `False`                                              |
`APP_DISABLE_DOCS`   | `disable_docs`        | `bool` | `False`                                              |

`Settings` also has a derived property `fastapi_kwargs` consisting of a dict with all of the attributes above except
`disable_docs`.

(Note that each of the keys of `fastapi_kwargs` are keyword arguments for `fastapi.FastAPI.__init__`.)

If `disable_docs` is `True`, the values of `docs_url`, `redoc_url`, and `openapi_url` are all set to `None`
in the `fastapi_kwargs` property value.
