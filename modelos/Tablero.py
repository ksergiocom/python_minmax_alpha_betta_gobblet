from modelos.Jugador import Jugador
from modelos.Pieza import Pieza


class Tablero:

	# Inicialización del tablero
	def __init__(self) -> None:
		self.jugadores = [
			Jugador("Humano"),
			Jugador("Maquina"),
		]

		self.piezas: list[Pieza] = []
		for jugador in self.jugadores:
			for tamano in range(1, 5):
				for _ in range(3):
					self.piezas.append(Pieza(jugador, tamano))

		self.turno = self.jugadores[0]

	# Función para comprobar que una pieza se pueda colocar en una posición del tablero
	# Simplemente no se pueden colocar piezas del mismo tamaño o menor a la que ya está colocada
	def es_movimiento_valido(self, pieza: Pieza, posicion: tuple[int, int]) -> bool:
		pieza_superior_celda = self.pieza_superior_en_posicion(posicion)
		if pieza_superior_celda and pieza_superior_celda.tamano >= pieza.tamano:
			return False
		return True

	# Mover una pieza
	# Simplemente le asignamos una posicion a una pieza.
	# Hago una comprobación de que se pueda colocar (que sea un movimiento legal)
	# * En la práctica esa excepción nunca la uso porque siempre compruebo que sea un movimiento
	# 	válido antes de mover. (Es código inalcanzable, lo hice al principio)
	def mover_pieza(self, pieza: Pieza, posicion: tuple[int, int]) -> None:
		pieza_superior_celda = self.pieza_superior_en_posicion(posicion)
		if pieza_superior_celda and pieza_superior_celda.tamano >= pieza.tamano:
			raise Exception(
				"Es un movimiento inválido. Hay una pieza con un tamaño igual o superior en la celda."
			)
		pieza.posicion = posicion

	# Todas las piezas que todavía no se han colocado
	def piezas_sin_colocar(self) -> list[Pieza]:
		return [pieza for pieza in self.piezas if pieza.posicion == None]

	# Todas las piezas que no están siendo tapadas por otras
	def piezas_alcanzables(self) -> list[Pieza]:
		piezas = self.piezas_sin_colocar()
		for y in range(4):
			for x in range(4):
				p = self.pieza_superior_en_posicion((x, y))
				if p:
					piezas.append(p)
		return piezas

	# Funcion que devuelve la pila de piezas de una posicion concreta
	def piezas_en_posicion(self, posicion: tuple[int, int]) -> list[Pieza]:
		return [pieza for pieza in self.piezas if pieza.posicion == posicion]

	# Funcion auxiliar para comprobar la posición en tope de pila en una posicion concreta
	def pieza_superior_en_posicion(self, posicion: tuple[int, int]) -> Pieza | None:
		piezas = [pieza for pieza in self.piezas if pieza.posicion == posicion]
		if len(piezas) == 0:
			return None
		piezas.sort(key=lambda pieza: pieza.tamano)
		return piezas[-1]

	# Cambiar turno
	def cambiar_turno(self) -> None:
		if self.turno is self.jugadores[0]:
			self.turno = self.jugadores[1]
		else:
			self.turno = self.jugadores[0]

	# Función para comprobar si algún jugador ha ganado
	def es_estado_final(self):
		piezas: list[Pieza] = []

		# Filas
		for y in range(4):
			for x in range(4):
				p = self.pieza_superior_en_posicion((x, y))
				if p:
					piezas.append(p)
			if len(piezas) == 4 and all(p.jugador == piezas[0].jugador for p in piezas):
				return True
			piezas = []

		# Columnas
		for x in range(4):
			for y in range(4):
				p = self.pieza_superior_en_posicion((x, y))
				if p:
					piezas.append(p)
			if len(piezas) == 4 and all(p.jugador == piezas[0].jugador for p in piezas):
				return True
			piezas = []

		# Diagonal principal
		piezas = []
		for i in range(4):
			p = self.pieza_superior_en_posicion((i, i))
			if p:
				piezas.append(p)
		if len(piezas) == 4 and all(p.jugador == piezas[0].jugador for p in piezas):
			return True

		# Diagonal secundaria
		piezas = []
		for i in range(4):
			p = self.pieza_superior_en_posicion((i, 3 - i))
			if p:
				piezas.append(p)
		if len(piezas) == 4 and all(p.jugador == piezas[0].jugador for p in piezas):
			return True

		return False

	# Función de Heurística para determinan el valor del tablero actual (a favor de la máquina)
	# Simplemente doy más peso según el tamaño a:
	# 	- Pieza alcanzables
	#   - Filas / columnas / diagonales (Tener mas piezas es mucho mas importante que el peso)
	#   - Priorizo las esquinas porque atacan 3 zonas a la vez
	def heuristica(self) -> int:
		total = 0

		# Piezas alcanzables ----------------------------------------------------------------------
		piezas_maquina_sin_colocar = [
			p for p in self.piezas_sin_colocar() if p.jugador.nombre == "Maquina"
		]
		piezas_humano_sin_colocar = [
			p for p in self.piezas_sin_colocar() if p.jugador.nombre == "Humano"
		]

		for pieza in piezas_maquina_sin_colocar:
			total += pieza.tamano * 2
		for pieza in piezas_humano_sin_colocar:
			total -= pieza.tamano * 2

		# Piezas colocadas ------------------------------------------------------------------------
		# Filas
		for y in range(4):
			piezas_maquina: list[Pieza] = []
			piezas_humano: list[Pieza] = []
			for x in range(4):
				p = self.pieza_superior_en_posicion((x, y))
				if p:
					if p.jugador.nombre == "Maquina":
						piezas_maquina.append(p)
					else:
						piezas_humano.append(p)
			
			# Maquina gana! Hacer esta jugada!
			if len(piezas_maquina) == 4:
				return 999999
			
			# Defenderse!
			if len(piezas_humano) == 3:
				max_humano = max(p.tamano for p in piezas_humano)
				# Comprobamos si se puede bloquear
				puede_bloquear = any(p.tamano >= max_humano for p in piezas_maquina)
				if not puede_bloquear:
					total -= 999999

		# Filas
		for x in range(4):
			piezas_maquina: list[Pieza] = []
			piezas_humano: list[Pieza] = []
			for y in range(4):
				p = self.pieza_superior_en_posicion((x, y))
				if p:
					if p.jugador.nombre == "Maquina":
						piezas_maquina.append(p)
					else:
						piezas_humano.append(p)
			
			# Maquina gana! Hacer esta jugada!
			if len(piezas_maquina) == 4:
				return 999999
			
			# Defenderse!
			if len(piezas_humano) == 3:
				max_humano = max(p.tamano for p in piezas_humano)
				# Comprobamos si se puede bloquear
				puede_bloquear = any(p.tamano >= max_humano for p in piezas_maquina)
				if not puede_bloquear:
					total -= 999999


		# Diagonal principal
		piezas_maquina = []
		piezas_humano = []
		for i in range(4):
			p = self.pieza_superior_en_posicion((i, i))
			if p:
				if p.jugador.nombre == "Maquina":
					piezas_maquina.append(p)
				else:
					piezas_humano.append(p)

		if len(piezas_maquina) == 4:
			return 999999

		if len(piezas_humano) == 3:
			max_humano = max(p.tamano for p in piezas_humano)
			puede_bloquear = any(p.tamano >= max_humano for p in piezas_maquina)
			if not puede_bloquear:
				total -= 999999

		total += (4 ** len(piezas_maquina)) * sum(p.tamano for p in piezas_maquina)
		total -= (4 ** len(piezas_humano)) * sum(p.tamano for p in piezas_humano)


		# Diagonal secundaria
		piezas_maquina = []
		piezas_humano = []
		for i in range(4):
			p = self.pieza_superior_en_posicion((i, 3 - i))
			if p:
				if p.jugador.nombre == "Maquina":
					piezas_maquina.append(p)
				else:
					piezas_humano.append(p)

		if len(piezas_maquina) == 4:
			return 999999

		if len(piezas_humano) == 3:
			max_humano = max(p.tamano for p in piezas_humano)
			puede_bloquear = any(p.tamano >= max_humano for p in piezas_maquina)
			if not puede_bloquear:
				total -= 999999

		total += (4 ** len(piezas_maquina)) * sum(p.tamano for p in piezas_maquina)
		total -= (4 ** len(piezas_humano)) * sum(p.tamano for p in piezas_humano)


		# Esquinas --------------------------------------------------------------------------------
		esquinas = [(0, 0), (0, 3), (3, 0), (3, 3)]
		for x, y in esquinas:
			p = self.pieza_superior_en_posicion((x, y))
			if p:
				if p.jugador.nombre == "Maquina":
					total += 2 * p.tamano
				else:
					total -= 2 * p.tamano

		return total

	# Matriz que representa todas las casillas del tablero con una
	# lista de piezas colocadas en cada una de ellas.
	# * La uso como función auxiliar en la GUI
	def matriz(self) -> list[list[list[Pieza]]]:
		matriz: list[list[list[Pieza]]] = []
		for y in range(4):
			matriz.append([])
			for x in range(4):
				matriz[y].append([])

		for pieza in self.piezas:
			if not pieza.posicion:
				continue
			x, y = pieza.posicion
			matriz[y][x].append(pieza)

		for fila in matriz:
			for casilla in fila:
				casilla.sort(key=lambda pieza: pieza.tamano)

		return matriz
