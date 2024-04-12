# Como iniciar la pagina
Para poder iniciar la pagina, primero debemos utilizar el entorno virtual, para esto utilizamos el comando:
## Linux
```source venv/bin/activate```
## Windows
```
# En cmd.exe
venv\Scripts\activate.bat
# En PowerShell
venv\Scripts\Activate.ps1
```

Luego de esto iniciamos el localhost de flask con:
```flask run --debug```

Para ver la pagina hacemos [Ctrl + Click izq] sobre la dirección IP que nos muestra la terminal.

# En caso que no funcione
en la carpeta base del proyecto de encuentra un archivo de texto llamado ```requirements.txt```
, el cual contiene los requerimientos del entorno virtual, se puede volver a crear el entorno virtual con el siguiente comando:

```pip install -r requirements.txt```
