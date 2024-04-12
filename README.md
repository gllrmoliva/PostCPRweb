# Guía de Inicio para la Página

Para iniciar la página, es necesario utilizar un entorno virtual. Sigue estos pasos:

## En Linux

Abre una terminal y ejecuta el siguiente comando para activar el entorno virtual:

```
source venv/bin/activate
```

## En Windows (utilizando GIT BASH)

Abre GIT BASH y ejecuta el siguiente comando para activar el entorno virtual:

```
. venv/bin/Activate
```

Una vez activado el entorno virtual, inicia el servidor local de Flask con el siguiente comando:

```
flask run --debug
```

Para visualizar la página, abre tu navegador web y realiza clic izquierdo mientras mantienes presionada la tecla "Ctrl" en la dirección IP que aparece en la terminal (generalmente localhost).

# Solución de Problemas

En caso de que encuentres dificultades, sigue estos pasos:

1. Dirígete a la carpeta base del proyecto.
2. Encuentra el archivo de texto llamado `requirements.txt`, que contiene los requerimientos del entorno virtual.
3. Crea nuevamente el entorno virtual con la misma configuración utilizando el siguiente comando:

```
pip install -r requirements.txt
```
