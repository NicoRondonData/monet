# Descripción

En Monet servimos APIs usando el REST Framework y usamos features avanzados del Django
Admin.
Teniendo en cuenta lo anterior la prueba consiste en implementar modelos para manejar notas
de estudiantes, exámenes con sus preguntas y respuestas, y modificaciones en el django
Admin para mostrar las respuestas escogidas por un estudiante.
Se deben exponer endpoints para registrar la respuesta de un estudiante a preguntas de un
examen.

# Entregables

Enviar un link a un repositorio en Github que contenga lo siguiente:

- Una aplicación Django
- Una historia de commits que demuestre el orden de implementación
- Un archivo README que explique como funciona el proyecto

# Como Ejecutar el proyecto
Primero Eejcuta el build del proyecto
```
make build.dev
```
Luego Corre el proyecto
```
make run.local
```
Puedes visitar la aplciacion en http://localhost:8009/
Encontraras la info de drf en http://localhost:8009/api/v1/monet/

```
{
    "exams": "http://localhost:8009/api/v1/monet/exams/",
    "questions": "http://localhost:8009/api/v1/monet/questions/",
    "answers": "http://localhost:8009/api/v1/monet/answers/",
    "student_answers": "http://localhost:8009/api/v1/monet/student_answers/"
    "token": "http://localhost:8009/api/v1/token/" # Aqui puedes ver el tokend e un usuarios
}
```
Al momento de ejecutar se agraga cierta  informaciona la base de datos entre ellos los siguientes usuarios:
- admin: 1234
- estudiante_1: 1234
- estudiante_2: 1234
- estudiante_3:1234

Puedes pedir el toke de unusuario especifico http://localhost:8009/api/v1/token/ y para usar ese token es necesario
en el header añadir Bearer antes del token
### Para ejecutar test

Primero ejecuta los pasos anteriores
```
make test.local
```

### Para ejecutar linters
Primero ejecuta los pasos anteriores
```
make lint.local
