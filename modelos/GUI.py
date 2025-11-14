import tkinter
from tkinter import messagebox

from modelos.Tablero import Tablero
from modelos.Pieza import Pieza
from modelos.AI import mini_max

class GUI:
	# Inicializar el tablero (inicializo otras cosas en el metodo generar, un poco chapuza)
	def __init__(self) -> None:
		self.tablero = Tablero()
		self.pieza_seleccionada:Pieza|None = None
		
	# Funcion para mandar mensajes popup
	def ventana_alerta(self, texto:str):
		messagebox.showinfo("showinfo", texto)
  
	# Seleccionar pieza al hacer click
	# Callback de los botones
	def seleccionar_pieza(self, pieza:Pieza):
		if self.tablero.turno.nombre != "Humano":
			return

		if pieza.jugador.nombre != "Humano":
			self.ventana_alerta("No puedes seleccionar piezas de la máquina")
			return
	  
		posicion = pieza.posicion
		if posicion and self.tablero.pieza_superior_en_posicion(posicion) is not pieza:
			self.ventana_alerta("No puedes seleccionar piezas tapadas")
			return
   
		self.pieza_seleccionada = pieza
		self.mensaje.config(text=f"Pieza seleccionada: {pieza}")
  
	# Funcion para deseleccionar una pieza
	# Callback para boton de UI
	def deseleccionar_pieza(self):
		self.pieza_seleccionada = None
		self.mensaje.config(text=f"Selecciona una pieza...")

	# Funcion para mover la pieza seleccionada a la casilla.
	# Comprobamos que haya una pieza seleccionada y que sea un movimiento valido
	# Actualizamos la lógica de la posición (atributo posicion de la pieza)
	# Comprobamos si se ha ganado con este movimiento, y si no es así, realizamos
	# el movimiento de la máquina. Por ultimo se rerenderiza todo y se devuelve el 
	# control al usuario.
	def handle_click_casilla(self, x, y):
		if self.pieza_seleccionada:
			if not self.tablero.es_movimiento_valido(self.pieza_seleccionada, (x,y)):
				self.ventana_alerta("Es un movimiento inválido")
				return

			self.tablero.mover_pieza(self.pieza_seleccionada, (x,y))
			self.pieza_seleccionada = None
			self.mensaje.config(text="Selecciona una pieza...")
			
			if self.tablero.es_estado_final():
				self.actualizar_casillas()
				self.actualizar_paneles_laterales() 
				self.ventana_alerta("Has ganado!")
				return

			self.tablero.cambiar_turno()
			self.actualizar_casillas()
			self.actualizar_paneles_laterales() 

			self.movimiento_maquina()

			self.mensaje.config(text="Selecciona una pieza...")

	# Funcion para renderizar el estado visual del tablero.
	def actualizar_casillas(self):
		matriz = self.tablero.matriz()
		for y, fila in enumerate(matriz):
			for x, casilla_piezas in enumerate(fila):
				# Obtener los botones de esta casilla
				botones = self.casillas[y][x].winfo_children()
				
				# Actualizar cada botón según las piezas en la casilla
				for i, boton in enumerate(botones):
					# Todos los indices que no sean el utimo boton, deben ser disabled y otro color
					if i < len(casilla_piezas):
						pieza = casilla_piezas[i]
	
 						# COLORINCHIS: https://patriciaemiguel.com/assets/tkinter_colores.png	  
						color_fondo = "SteelBlue4" if pieza.jugador.nombre == "Humano" else "DarkOrange4"
						
						boton.config(
							text=f"{pieza.jugador.nombre[0]}{pieza.tamano}",
							width=2*pieza.tamano,
							state="disabled",
							bg=color_fondo,
							fg="white",
						)

						# Solo el último botón (superior) se activa
						if i == len(casilla_piezas) - 1:
							# COLORINCHIS: https://patriciaemiguel.com/assets/tkinter_colores.png
							color_fondo = "SteelBlue1" if pieza.jugador.nombre == "Humano" else "DarkOrange1"
							boton.config(
								state="normal",
								command=(lambda p=pieza: self.seleccionar_pieza(p)),
								bg=color_fondo
							)

					# El resto de botones no tienen ninguna pieza
					else:
						boton.config(
							text="Vacío",
							state="disabled",
							bg="gainsboro",
							fg="black",
							width=2*4
						)
			
	# Generar toda la interfaz
	# Hay cosas que inicializo aquí en vez de en __init__
	# Lo dejo así por falta de tiempo...
	def generate(self):
		# Piezas del jugador
		piezas_jugador = [pieza for pieza in self.tablero.piezas_sin_colocar() if pieza.jugador.nombre == "Humano"]
		piezas_maquina = [pieza for pieza in self.tablero.piezas_sin_colocar() if pieza.jugador.nombre == "Maquina"]

		self.root = tkinter.Tk()
  
		self.jugador_frame = tkinter.Frame(self.root)
		self.jugador_frame.pack(side=tkinter.LEFT)
		for pieza in piezas_jugador:
			button = tkinter.Button(self.jugador_frame, bg="SteelBlue1", fg="white", text=f"{pieza.jugador.nombre[0]}{pieza.tamano}", width=2*pieza.tamano, command=lambda p=pieza: self.seleccionar_pieza(p))
			button.pack()


		# Contenedor central
		centro_frame = tkinter.Frame(self.root)
		centro_frame.pack(side=tkinter.LEFT)

		# Tablero central

		self.turno_label = tkinter.Label(centro_frame, text=f"Turno de: {self.tablero.turno.nombre}")
		self.turno_label.pack()
		self.mensaje = tkinter.Label(centro_frame, text=f"Selecciona una pieza...")
		self.mensaje.pack()
		buton_cancel_pieza = tkinter.Button(centro_frame, text="X deseleccionar pieza", command=self.deseleccionar_pieza)
		buton_cancel_pieza.pack()
		boton_reiniciar = tkinter.Button(centro_frame, bg="red", text="Reiniciar partida", command=self.reiniciar_partida)
		boton_reiniciar.pack()

		tablero_frame = tkinter.Frame(centro_frame)
		tablero_frame.pack()

		# Para poder acceder a las casillas
		self.casillas: list[list[tkinter.Frame|None]] = [
				[None,None,None,None],
				[None,None,None,None],
				[None,None,None,None],
				[None,None,None,None],
			]

		for y in range(4):
			for x in range(4):
				casilla = tkinter.Frame(tablero_frame, width=100, height=100,  borderwidth=3, relief="solid")
				casilla.grid(row=y, column=x, padx=5, pady=5)
				self.casillas[y][x] = casilla
				casilla.bind("<Button-1>", lambda event, px=x, py=y: self.handle_click_casilla(px, py))
				for _ in range(4):
					button = tkinter.Button(casilla, text="Vacío", state="disabled", width=2*4)
					button.pack()
					button.bind("<Button-1>", lambda event, px=x, py=y: self.handle_click_casilla(px, py))

		# Piezas de la máquina
		self.maquina_frame = tkinter.Frame(self.root)
		self.maquina_frame.pack(side=tkinter.LEFT)
  
		for pieza in piezas_maquina:
			button = tkinter.Button(self.maquina_frame, bg="DarkOrange1", fg="white", text=f"{pieza.jugador.nombre[0]}{pieza.tamano}", state="disabled", width=2*pieza.tamano)
			button.pack() 
		
		self.root.mainloop()
  
	# Funcion para ejecutar el movimiento de la máquina.
	# Usa minimax para buscar el mejor movimiento.
	# Realiza el movimiento, re-renderiza la UI y comprueba sí
	# la máquina ha ganado. Por ultimo devuelve el control al jugador
	def movimiento_maquina(self):
		self.mensaje.config(text="La máquina esta eligiendo una jugada...")
		self.root.update()
		mejor_tablero = mini_max(self.tablero, 0, 2, -999999, +999999)
  
		self.tablero = mejor_tablero
		self.actualizar_casillas()
		self.actualizar_paneles_laterales() 

		# Verificar si la máquina ganó
		if self.tablero.es_estado_final():
			self.ventana_alerta("La máquina ha ganado!")
			return
		
		# Cambiar turno al humano
		self.tablero.cambiar_turno()
		self.actualizar_casillas()
		self.actualizar_paneles_laterales() 
  
  
	# Re-renderizar las piezas disponibles sin colocar.
	def actualizar_paneles_laterales(self):
		# Limpiar paneles
		for widget in self.jugador_frame.winfo_children():
			widget.destroy()
		for widget in self.maquina_frame.winfo_children():
			widget.destroy()
		
		# Recrear botones de piezas sin colocar del humano
		piezas_jugador = [pieza for pieza in self.tablero.piezas_sin_colocar() if pieza.jugador.nombre == "Humano"]
		for pieza in piezas_jugador:
			button = tkinter.Button(self.jugador_frame, bg="SteelBlue1", fg="white", text=f"{pieza.jugador.nombre[0]}{pieza.tamano}", width=2*pieza.tamano, command=lambda p=pieza: self.seleccionar_pieza(p))
			button.pack()
		
		# Recrear botones de piezas de la máquina
		piezas_maquina = [pieza for pieza in self.tablero.piezas_sin_colocar() if pieza.jugador.nombre == "Maquina"]
		for pieza in piezas_maquina:
			button = tkinter.Button(self.maquina_frame, bg="DarkOrange1", fg="white", text=f"{pieza.jugador.nombre[0]}{pieza.tamano}", state="disabled", width=2*pieza.tamano)
			button.pack()
		
		# Actualizar label de turno
		self.turno_label.config(text=f"Turno de: {self.tablero.turno.nombre}")
  
  
	def reiniciar_partida(self):
		# Crear un tablero nuevo
		self.tablero = Tablero()
		self.pieza_seleccionada = None
		
		# Volver a renderizar todo
		self.actualizar_casillas()
		self.actualizar_paneles_laterales()
		self.turno_label.config(text=f"Turno de: {self.tablero.turno.nombre}")
		self.mensaje.config(text="Selecciona una pieza...")
