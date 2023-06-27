"""En este archivo se debe importar el archivo:
- ./controller.py
- ../util.py as util
- ../data/database.py as database
- ../tests/test_config.py as test_config
- ../tests/load_tests/ddos_simulation.py as ddos_simulation
- ../../main.py as main

Los imports deben hacerse de forma tal que funcionen con el siguiente
comando (estando parados dentro de la carpeta practico_02):
$PATH$/practico_02> python -m source.controller.ejercicio_03
"""

import source.controller.controller as controller
import source.util as util
import source.data.database as database
import main as main

# NO MODIFICAR - INICIO
assert main.name == "main"
assert util.name == "util"
assert database.name == "database"
assert controller.name == "controller"
#  MODIFICADO - INICIO
# assert test_config.name == "test_config"
# assert deploy_travis.name == "deploy_travis"
#  MODIFICADO - FIN
# NO MODIFICAR - FIN

# Este es el último ejercicio del TP2
