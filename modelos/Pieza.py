from modelos.Jugador import Jugador

# Pieza
# Cada pieza tiene un jugador asociado, un tamaño y una posición inicial nula.
# La posición es una tupla (x,y) que guardo en la pieza y es la única fuente de verdad.
# Para mover una pieza solo cambio sus posiciones, no se guarda en nigún otro sitio.
class Pieza:
	def __init__(self, jugador: Jugador, tamano: int):
		self.jugador = jugador
		self.tamano = tamano
		self.posicion: tuple[int,int] | None = None

	def __str__(self):
		return f"{self.jugador.nombre[0]}{self.tamano}"
	
	def __repr__(self) -> str:
		return f"{self.jugador.nombre[0]}{self.tamano}"

	