import tkinter as tk
from tkinter import messagebox
import random

class YahtzeeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Yahtzee")
        self.root.geometry("800x600")

        # Variables del juego
        self.jugador1_nombre = "Jugador 1"
        self.jugador2_nombre = "Jugador 2"
        self.hoja_jugador1 = self.inicializar_hoja_de_puntuacion()
        self.hoja_jugador2 = self.inicializar_hoja_de_puntuacion()
        self.jugadores = [(self.jugador1_nombre, self.hoja_jugador1), (self.jugador2_nombre, self.hoja_jugador2)]
        self.num_rondas = 13
        self.ronda_actual = 1
        self.jugador_actual_index = 0
        self.dados = [0] * 5
        self.dados_congelados = [False] * 5
        self.lanzamientos_restantes = 3
        self.num_simulaciones = 500  # Número de simulaciones para Monte Carlo

        # Crear la interfaz
        self.crear_interfaz()

    def inicializar_hoja_de_puntuacion(self):
        """Inicializa una hoja de puntuación vacía."""
        return {
            "Aces": None,
            "Doses": None,
            "Treses": None,
            "Cuatros": None,
            "Cincos": None,
            "Seises": None,
            "Bono Superior": None,
            "Tres de un Tipo": None,
            "Cuatro de un Tipo": None,
            "Full House": None,
            "Escalera Menor": None,
            "Escalera Mayor": None,
            "Yahtzee": None,
            "Chance": None,
            "Total Inferior": 0,
            "Total Superior": 0,
            "Gran Total": 0
        }

    def crear_interfaz(self):
        """Crea la interfaz gráfica del juego."""
        # Etiqueta para mostrar la ronda y el turno
        self.info_label = tk.Label(self.root, text=f"Ronda {self.ronda_actual} - Turno de {self.jugadores[self.jugador_actual_index][0]}", font=("Arial", 16))
        self.info_label.pack(pady=10)

        # Recuadros para los dados
        self.dados_frame = tk.Frame(self.root)
        self.dados_frame.pack(pady=10)
        self.dados_labels = []
        for i in range(5):
            label = tk.Label(self.dados_frame, text="0", font=("Arial", 24), width=4, height=2, relief="solid", bg="white")
            label.grid(row=0, column=i, padx=5)
            self.dados_labels.append(label)

        # Botón para lanzar los dados
        self.lanzar_button = tk.Button(self.root, text="Lanzar Dados", font=("Arial", 14), command=self.lanzar_dados)
        self.lanzar_button.pack(pady=10)

        # Botones para congelar los dados
        self.congelar_buttons = []
        for i in range(5):
            button = tk.Button(self.dados_frame, text="Congelar", font=("Arial", 10), command=lambda i=i: self.congelar_dado(i))
            button.grid(row=1, column=i, pady=5)
            self.congelar_buttons.append(button)

        # Botón para elegir categoría
        self.categoria_button = tk.Button(self.root, text="Elegir Categoría", font=("Arial", 14), command=self.elegir_categoria)
        self.categoria_button.pack(pady=10)

        # Hoja de puntuación de ambos jugadores
        self.hoja_frame = tk.Frame(self.root)
        self.hoja_frame.pack(pady=10)
        self.hoja_jugador1_label = tk.Label(self.hoja_frame, text=f"{self.jugador1_nombre}:\n{self.formatear_hoja(self.hoja_jugador1)}", font=("Arial", 12), justify="left")
        self.hoja_jugador1_label.grid(row=0, column=0, padx=20)
        self.hoja_jugador2_label = tk.Label(self.hoja_frame, text=f"{self.jugador2_nombre}:\n{self.formatear_hoja(self.hoja_jugador2)}", font=("Arial", 12), justify="left")
        self.hoja_jugador2_label.grid(row=0, column=1, padx=20)

        # Etiquetas para mostrar los totales de puntos
        self.total_jugador1_label = tk.Label(self.root, text=f"Total de {self.jugador1_nombre}: {self.hoja_jugador1['Gran Total']} puntos", font=("Arial", 14))
        self.total_jugador1_label.pack(pady=5)

        self.total_jugador2_label = tk.Label(self.root, text=f"Total de {self.jugador2_nombre}: {self.hoja_jugador2['Gran Total']} puntos", font=("Arial", 14))
        self.total_jugador2_label.pack(pady=5)

    def formatear_hoja(self, hoja):
        """Formatea la hoja de puntuación para mostrarla en la interfaz."""
        return "\n".join([f"{categoria}: {puntuacion if puntuacion is not None else '-'}" for categoria, puntuacion in hoja.items()])

    def actualizar_interfaz(self):
        """Actualiza la interfaz gráfica con los datos actuales."""
        # Actualizar los valores de los dados
        for i in range(5):
            self.dados_labels[i].config(text=str(self.dados[i]))

        # Actualizar la información de la ronda y el turno
        self.info_label.config(text=f"Ronda {self.ronda_actual} - Turno de {self.jugadores[self.jugador_actual_index][0]}", font=("Arial", 16))

        # Actualizar las hojas de puntuación
        self.hoja_jugador1_label.config(text=f"{self.jugador1_nombre}:\n{self.formatear_hoja(self.hoja_jugador1)}")
        self.hoja_jugador2_label.config(text=f"{self.jugador2_nombre}:\n{self.formatear_hoja(self.hoja_jugador2)}")

        # Actualizar los totales de puntos
        self.total_jugador1_label.config(text=f"Total de {self.jugador1_nombre}: {self.hoja_jugador1['Gran Total']} puntos")
        self.total_jugador2_label.config(text=f"Total de {self.jugador2_nombre}: {self.hoja_jugador2['Gran Total']} puntos")

    def lanzar_dados(self):
        """Lanza los dados que no están congelados."""
        if self.lanzamientos_restantes > 0:
            # Simular el lanzamiento de dados usando ciclos y condicionales
            for i in range(5):
                if not self.dados_congelados[i]:
                    self.dados[i] = self.simular_lanzamiento()  # Usar la función de simulación

            self.lanzamientos_restantes -= 1

            # Restablecer los dados a no congelados después del lanzamiento
            self.dados_congelados = [False] * 5
            for i in range(5):
                self.dados_labels[i].config(bg="white")  # Cambiar el color de fondo a blanco

            self.actualizar_interfaz()

            # Si no quedan lanzamientos, abrir automáticamente la ventana de selección de categoría
            if self.lanzamientos_restantes == 0:
                self.elegir_categoria_montecarlo()  # Usar la función Monte Carlo para elegir categoría
        else:
            messagebox.showinfo("Yahtzee", "No tienes más lanzamientos en este turno.")

    def simular_lanzamiento(self):
        """Simula el lanzamiento de un dado usando ciclos y condicionales."""
        r = random.random()
        if r < (1 / 6):
            return 1
        elif r < (2 / 6):
            return 2
        elif r < (3 / 6):
            return 3
        elif r < (4 / 6):
            return 4
        elif r < (5 / 6):
            return 5
        else:
            return 6

    def congelar_dado(self, index):
        """Congela o descongela un dado."""
        self.dados_congelados[index] = not self.dados_congelados[index]
        self.dados_labels[index].config(bg="lightblue" if self.dados_congelados[index] else "white")

    def elegir_categoria(self):
        """Permite al jugador elegir una categoría para puntuar."""
        jugador_nombre, hoja_actual = self.jugadores[self.jugador_actual_index]
        categorias_disponibles = [cat for cat, puntaje in hoja_actual.items() if puntaje is None and cat not in ["Bono Superior", "Total Inferior", "Total Superior", "Gran Total"]]

        if not categorias_disponibles:
            messagebox.showinfo("Yahtzee", "No hay categorías disponibles.")
            return

        # Crear una ventana emergente para elegir la categoría
        categoria_window = tk.Toplevel(self.root)
        categoria_window.title("Elegir Categoría")
        tk.Label(categoria_window, text="Elige una categoría:", font=("Arial", 14)).pack(pady=10)

        for categoria in categorias_disponibles:
            tk.Button(categoria_window, text=categoria, font=("Arial", 12), command=lambda c=categoria: self.asignar_categoria(c, categoria_window)).pack(pady=5)

    def asignar_categoria(self, categoria, window):
        """Asigna la puntuación a la categoría seleccionada."""
        window.destroy()
        jugador_nombre, hoja_actual = self.jugadores[self.jugador_actual_index]
        puntuacion = self.calcular_puntuacion_categoria(categoria)
        hoja_actual[categoria] = puntuacion
        self.actualizar_totales(hoja_actual)
        self.cambiar_turno()

    def calcular_puntuacion_categoria(self, categoria):
        """Calcula la puntuación para la categoría seleccionada."""
        if categoria == "Aces":
            return sum(dado for dado in self.dados if dado == 1)
        elif categoria == "Doses":
            return sum(dado for dado in self.dados if dado == 2)
        elif categoria == "Treses":
            return sum(dado for dado in self.dados if dado == 3)
        elif categoria == "Cuatros":
            return sum(dado for dado in self.dados if dado == 4)
        elif categoria == "Cincos":
            return sum(dado for dado in self.dados if dado == 5)
        elif categoria == "Seises":
            return sum(dado for dado in self.dados if dado == 6)
        elif categoria == "Chance":
            return sum(self.dados)
        elif categoria == "Yahtzee":
            return 50 if len(set(self.dados)) == 1 else 0
        elif categoria == "Tres de un Tipo":
            return sum(self.dados) if self.tiene_n_de_un_tipo(3) else 0
        elif categoria == "Cuatro de un Tipo":
            return sum(self.dados) if self.tiene_n_de_un_tipo(4) else 0
        elif categoria == "Full House":
            return 25 if self.es_full_house() else 0
        elif categoria == "Escalera Menor":
            return 30 if self.es_escalera_menor() else 0
        elif categoria == "Escalera Mayor":
            return 40 if self.es_escalera_mayor() else 0
        return 0

    def tiene_n_de_un_tipo(self, n):
        """Verifica si hay al menos n dados con el mismo valor."""
        return any(self.dados.count(dado) >= n for dado in set(self.dados))

    def es_full_house(self):
        """Verifica si los dados forman un Full House (tres de un tipo y un par)."""
        valores = [self.dados.count(dado) for dado in set(self.dados)]
        return sorted(valores) == [2, 3]

    def es_escalera_menor(self):
        """Verifica si los dados forman una Escalera Menor (4 números consecutivos)."""
        dados_unicos = sorted(set(self.dados))
        for i in range(len(dados_unicos) - 3):
            if dados_unicos[i:i+4] == list(range(dados_unicos[i], dados_unicos[i] + 4)):
                return True
        return False

    def es_escalera_mayor(self):
        """Verifica si los dados forman una Escalera Mayor (5 números consecutivos)."""
        dados_unicos = sorted(set(self.dados))
        return dados_unicos == [1, 2, 3, 4, 5] or dados_unicos == [2, 3, 4, 5, 6]

    def actualizar_totales(self, hoja):
        """Actualiza los totales de la hoja de puntuación."""
        hoja["Total Superior"] = sum(puntuacion for categoria, puntuacion in hoja.items() if categoria in ["Aces", "Doses", "Treses", "Cuatros", "Cincos", "Seises"] and puntuacion is not None)
        hoja["Bono Superior"] = 35 if hoja["Total Superior"] >= 63 else 0
        hoja["Total Inferior"] = sum(puntuacion for categoria, puntuacion in hoja.items() if categoria in ["Tres de un Tipo", "Cuatro de un Tipo", "Full House", "Escalera Menor", "Escalera Mayor", "Yahtzee", "Chance"] and puntuacion is not None)
        hoja["Gran Total"] = hoja["Total Superior"] + hoja["Bono Superior"] + hoja["Total Inferior"]

    def cambiar_turno(self):
        """Cambia el turno al siguiente jugador o avanza a la siguiente ronda."""
        self.lanzamientos_restantes = 3
        self.dados = [0] * 5
        self.dados_congelados = [False] * 5
        self.jugador_actual_index = 1 - self.jugador_actual_index

        if self.jugador_actual_index == 0:
            self.ronda_actual += 1

        if self.ronda_actual > self.num_rondas:
            self.mostrar_ganador()
        else:
            self.actualizar_interfaz()

    def mostrar_ganador(self):
        """Muestra el ganador al final del juego."""
        jugador1_puntos = self.hoja_jugador1["Gran Total"]
        jugador2_puntos = self.hoja_jugador2["Gran Total"]

        if jugador1_puntos > jugador2_puntos:
            ganador = f"{self.jugador1_nombre} gana con {jugador1_puntos} puntos."
        elif jugador2_puntos > jugador1_puntos:
            ganador = f"{self.jugador2_nombre} gana con {jugador2_puntos} puntos."
        else:
            ganador = "¡Es un empate!"

        messagebox.showinfo("Yahtzee", f"Juego terminado.\n{ganador}")
        self.root.destroy()

    def elegir_categoria_montecarlo(self):
        """Elige la mejor categoría usando el método de Monte Carlo."""
        jugador_nombre, hoja_actual = self.jugadores[self.jugador_actual_index]
        categorias_disponibles = [cat for cat, puntaje in hoja_actual.items() if puntaje is None and cat not in ["Bono Superior", "Total Inferior", "Total Superior", "Gran Total"]]

        if not categorias_disponibles:
            messagebox.showinfo("Yahtzee", "No hay categorías disponibles.")
            return

        # Simular múltiples juegos para cada categoría y calcular la puntuación promedio
        puntuaciones_simuladas = {}

        for categoria in categorias_disponibles:
            total_puntuacion = 0
            for _ in range(self.num_simulaciones):
                # Simular el resto del turno y obtener la puntuación final
                puntuacion = self.simular_turno(categoria, list(self.dados), list(self.dados_congelados), self.lanzamientos_restantes)
                total_puntuacion += puntuacion

            # Calcular la puntuación promedio para la categoría
            puntuaciones_simuladas[categoria] = total_puntuacion / self.num_simulaciones

        # Elegir la categoría con la puntuación promedio más alta
        mejor_categoria = max(puntuaciones_simuladas, key=puntuaciones_simuladas.get)

        # Mostrar la categoría elegida en un messagebox
        messagebox.showinfo("Yahtzee", f"La categoría elegida por Monte Carlo es: {mejor_categoria}")

        # Asignar la categoría y continuar
        self.asignar_categoria_montecarlo(mejor_categoria)

    def simular_turno(self, categoria, dados_iniciales, dados_congelados_iniciales, lanzamientos_restantes_iniciales):
        """Simula el resto del turno y devuelve la puntuación para la categoría dada."""
        dados_simulados = list(dados_iniciales)
        dados_congelados = list(dados_congelados_iniciales)
        lanzamientos_restantes = lanzamientos_restantes_iniciales

        # Simular los lanzamientos restantes
        while lanzamientos_restantes > 0:
            # Lanzar los dados no congelados
            for i in range(5):
                if not dados_congelados[i]:
                    dados_simulados[i] = self.simular_lanzamiento()

            lanzamientos_restantes -= 1

            # Congelar dados aleatoriamente (simulando una estrategia)
            for i in range(5):
                dados_congelados[i] = random.random() < 0.5  # 50% de probabilidad de congelar

        # Calcular la puntuación para la categoría
        return self.calcular_puntuacion_categoria_simulada(categoria, dados_simulados)

    def simular_puntuacion(self, categoria):
        """Simula la puntuación para una categoría dada."""
        # Crear una copia de los dados actuales
        dados_simulados = list(self.dados)

        # Simular los dados restantes
        for i in range(5):
            if not self.dados_congelados[i]:
                dados_simulados[i] = self.simular_lanzamiento()

        # Calcular la puntuación para la categoría simulada
        return self.calcular_puntuacion_categoria_simulada(categoria, dados_simulados)

    def calcular_puntuacion_categoria_simulada(self, categoria, dados_simulados):
        """Calcula la puntuación para la categoría seleccionada con los dados simulados."""
        if categoria == "Aces":
            return sum(dado for dado in dados_simulados if dado == 1)
        elif categoria == "Doses":
            return sum(dado for dado in dados_simulados if dado == 2)
        elif categoria == "Treses":
            return sum(dado for dado in dados_simulados if dado == 3)
        elif categoria == "Cuatros":
            return sum(dado for dado in dados_simulados if dado == 4)
        elif categoria == "Cincos":
            return sum(dado for dado in dados_simulados if dado == 5)
        elif categoria == "Seises":
            return sum(dado for dado in dados_simulados if dado == 6)
        elif categoria == "Chance":
            return sum(dados_simulados)
        elif categoria == "Yahtzee":
            return 50 if len(set(dados_simulados)) == 1 else 0
        elif categoria == "Tres de un Tipo":
            return sum(dados_simulados) if self.tiene_n_de_un_tipo_simulada(3, dados_simulados) else 0
        elif categoria == "Cuatro de un Tipo":
            return sum(dados_simulados) if self.tiene_n_de_un_tipo_simulada(4, dados_simulados) else 0
        elif categoria == "Full House":
            return 25 if self.es_full_house_simulada(dados_simulados) else 0
        elif categoria == "Escalera Menor":
            return 30 if self.es_escalera_menor_simulada(dados_simulados) else 0
        elif categoria == "Escalera Mayor":
            return 40 if self.es_escalera_mayor_simulada(dados_simulados) else 0
        return 0

    def tiene_n_de_un_tipo_simulada(self, n, dados_simulados):
        """Verifica si hay al menos n dados con el mismo valor en los dados simulados."""
        return any(dados_simulados.count(dado) >= n for dado in set(dados_simulados))

    def es_full_house_simulada(self, dados_simulados):
        """Verifica si los dados simulados forman un Full House (tres de un tipo y un par)."""
        valores = [dados_simulados.count(dado) for dado in set(dados_simulados)]
        return sorted(valores) == [2, 3]

    def es_escalera_menor_simulada(self, dados_simulados):
        """Verifica si los dados simulados forman una Escalera Menor (4 números consecutivos)."""
        dados_unicos = sorted(set(dados_simulados))
        for i in range(len(dados_unicos) - 3):
            if dados_unicos[i:i+4] == list(range(dados_unicos[i], dados_unicos[i] + 4)):
                return True
        return False

    def es_escalera_mayor_simulada(self, dados_simulados):
        """Verifica si los dados simulados forman una Escalera Mayor (5 números consecutivos)."""
        dados_unicos = sorted(set(dados_simulados))
        return dados_unicos == [1, 2, 3, 4, 5] or dados_unicos == [2, 3, 4, 5, 6]

    def asignar_categoria_montecarlo(self, categoria):
        """Asigna la puntuación a la categoría seleccionada por Monte Carlo."""
        jugador_nombre, hoja_actual = self.jugadores[self.jugador_actual_index]
        puntuacion = self.calcular_puntuacion_categoria(categoria)
        hoja_actual[categoria] = puntuacion
        self.actualizar_totales(hoja_actual)
        self.cambiar_turno()

# Crear la ventana principal y ejecutar el juego
root = tk.Tk()
juego = YahtzeeGame(root)
root.mainloop()