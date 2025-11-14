import copy
import random

from modelos.Tablero import Tablero

# Función de min-max con poda alfa-beta
#
# Recibimos un tablero y a partir de el determinamos todas las piezas que podemos mover e intentamos
# hacer cada uno de los movimientos. 
# 
# Solo se hará hasta X niveles de profundidad y devolverá el tablero con el valor de la heurística
# maximizado para la máquina.
def mini_max(tablero: Tablero, nivel_actual: int, nivel_max: int, alfa: int, beta: int) -> Tablero:
    
    # Caso base. Fin de la recursión, hemos alcanzado el nivel más profundo
    # del árbol o hemos encontrado una posición que gana.
    if nivel_actual == nivel_max or tablero.es_estado_final():
        return tablero
    
    sucesores: list[Tablero] = []

    # Vemos todas las posibilidades de movimientos posibles a realizar
    piezas_del_turno = [p for p in tablero.piezas_alcanzables() if p.jugador.nombre == tablero.turno.nombre]
    
    for pieza in piezas_del_turno:
        for x in range(4):
            for y in range(4):
                
                # Clausulas de guarda (misma posición y movimiento inválido)
                if pieza.posicion == (x, y):
                    continue
                if not tablero.es_movimiento_valido(pieza, (x, y)):
                    continue
                    
                # Buscamos la pieza en el nuevo tablero y la cambiamos de posición a la nueva
                nuevo_tablero = copy.deepcopy(tablero)
                piezas_filtradas = [
                    p for p in nuevo_tablero.piezas 
                    if p.jugador.nombre == pieza.jugador.nombre 
                    and p.tamano == pieza.tamano 
                    and p.posicion == pieza.posicion
                ]
                pieza_nueva = piezas_filtradas[0] # Solo debería existir una :)
                pieza_nueva.posicion = (x, y)
                # Nuevo sucesor
                sucesores.append(nuevo_tablero)


    mejor_tablero = None
    
    # Para no realizar siempre la misma secuencia de jugadas voy a hacer un shuffle de los sucesores. Asi el orden es diferente.
    # *Se que esto penalizará el rendimiento, pero lo voy a sacrificar por darle más aleatoriedad
    random.shuffle(sucesores)

    # MAX
    if tablero.turno.nombre == "Maquina":
        mejor_valor = -999999
        for sucesor in sucesores:
            # El deepcopy es para poder cambiar de turno y que no afecte al devolverlo
            sucesor_evaluado = copy.deepcopy(sucesor)
            sucesor_evaluado.cambiar_turno()
            
            resultado = mini_max(sucesor_evaluado, nivel_actual + 1, nivel_max, alfa, beta)
            
            # Pequeña variabilida del 5% para darle algo random (y tener variaciones en el ordenador vs ordenador)
            factor_random = random.uniform(0.95, 1.05)
            valor = int(resultado.heuristica() * factor_random)
            
            
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_tablero = sucesor  # Guardamos el sucesor SIN cambio de turno
            
            alfa = max(alfa, valor)
            if beta <= alfa:
                break
    
    # MIN
    else:
        mejor_valor = +999999
        for sucesor in sucesores:
            # El deepcopy es para poder cambiar de turno y que no afecte al devolverlo
            sucesor_evaluado = copy.deepcopy(sucesor)
            sucesor_evaluado.cambiar_turno()
            
            resultado = mini_max(sucesor_evaluado, nivel_actual + 1, nivel_max, alfa, beta)
            
            # Pequeña variabilida del 5% para darle algo random (y tener variaciones en el ordenador vs ordenador)
            factor_random = random.uniform(0.95, 1.05)
            valor = int(resultado.heuristica() * factor_random)
            
            
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_tablero = sucesor  # Guardamos el sucesor SIN cambio de turno
            
            beta = min(beta, valor)
            if beta <= alfa:
                break

    print(f"\t->\tMinmax: [Valor:{mejor_valor}][Alfa:{alfa}][Beta:{beta}]")
    return mejor_tablero if mejor_tablero else tablero