# Clase que representa un jugador.
# Cada pieza tendrá su jugador y simplemente contiene el nombre
class Jugador:
	def __init__(self, nombre: str):
		self.nombre = nombre

	def __str__(self):
		return self.nombre
	
	def __repr__(self):
		return self.nombre