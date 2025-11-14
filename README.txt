Sistemas Inteligentes 2025
Autor: Sergiy Khudoley
Fecha: 12/11/2025


####################################################################
Introducción
####################################################################

GOBBLET con min-max y poda alfa-bet

Juego de mesa que consiste en hacer un cuatro en rayas con cubos de distinto tamaño. Se juega contra la IA

La heurística implementada es muy básica y le he agregado un pequeño porcentaje de aleatoriedad para que no siempre elija
las mismas jugadas.

Esta estructurado como un conjunto de instancias de Piezas que guardan sus coordenadas y gestiono la mayoría 
de las funcionalidades simplemente filtrando/iterando sobre este listado.

La mayor parte de la lógica está en las clases: Tablero y GUI.

	Tablero -> Se encarga principalmente en ser el "arbitro" de la partida, comprueba estados finales, validez de movimientos,
				devuelve el listado de piezas disponibles, etc.

	GUI 	-> Representación del juego y espera el movimiento del jugador para aplicar la jugada de la máquina.


No tiene dependencias. Para ejecutarlo simplemente hay que hacer:
	python main.py

*Se puede ajustar el nivel de exploración en el "método movimiento_maquina()" de la clase modelos.GUI


####################################################################
Notas
####################################################################

Me enfocado en el algoritmo minimax pero me he despreocupado de la complejidad del código ni en refactorizarlo. Hay muchas mejoras
que se podrían realizar.

La interfaz gráfica tiene algún error que no impide jugar, pero a veces es un poco "ortopédica" y te puede lanzar un aviso de jugada inválida.
(No he indagado mucho en esto)


####################################################################
Resumen del código
####################################################################

CLASES Y MÉTODOS:

Pieza
	*Atributos básicos . Principalmente -> guardo su posicion como una tupla (x,y)

Jugador
	*Atributos básicos

Tablero
	es_movimiento_valido
	mover_pieza
	piezas_sin_colocar
	piezas_alcanzables
	piezas_en_posicion
	pieza_superior_en_posicion
	cambiar_turno
	es_estado_final
	heuristica
	matriz

AI
	mini_max

GUI
	ventana_alerta
	seleccionar_pieza
	deseleccionar_pieza
	handle_click_casilla
	actualizar_casillas
	actualizar_paneles_laterales
	movimiento_maquina
	generar
