import numpy as np

class WallE:
    def __init__(self, posicion_inicial=(0, 0), direccion_inicial=(1, 0)):
        """Inicializa la posición y dirección de Wall-E, así como otros parámetros."""
        self.posicion = np.array(posicion_inicial, dtype=int)
        self.posicion_anterior = self.posicion.copy()  # Guardar posición inicial
        self.direccion = self.normalize(np.array(direccion_inicial, dtype=float))
        self.velocidad = 1 #unidades por paso
        self.K = 2.0 #Ganancia para el control de direccion
        self.basura_colectada=[]
        self.ultima_matriz_rotacion = np.identity(2)

    def normalize(self, v):
            """Normaliza un vector v para que tenga una magnitud de 1."""
            norm = np.linalg.norm(v)
            return v / norm if norm != 0 else v
        
    def movimiento_frente(self):
        """Mueve a Wall-E hacia adelante en la dirección actual."""
        self.posicion_anterior = self.posicion.copy()  # Guardar posición antes de mover
        self.posicion += (self.velocidad * self.direccion).astype(int)
        
    def movimiento_atras(self):
        """Mueve a Wall-E hacia atras en la dirección actual."""
        self.posicion_anterior = self.posicion.copy()  # Guardar posición antes de mover
        self.posicion -= (self.velocidad * self.direccion).astype(int)

    def rotacion(self, angulo_de_rotacion):
        """Rota a Wall-E un ángulo dado en grados."""
        angulo_rad = np.radians(angulo_de_rotacion)
        matriz_rotacion = np.array([
            [np.cos(angulo_rad), -np.sin(angulo_rad)],
            [np.sin(angulo_rad), np.cos(angulo_rad)]
        ]) #R(THETA)
        self.direccion = self.normalize(np.dot(matriz_rotacion, self.direccion))
        self .theta = np.arctan2( self .direccion[ 1 ], self .direccion[ 0 ])

    def get_vector_a_meta(self, posicion_meta):
        """Devuelve el vector desde la posición actual hasta la posición objetivo."""
        return np.array(posicion_meta) - self.posicion
        
    def calculo_de_alineacion(self, posicion_meta):
            """Calcula la alineación entre la dirección actual y la dirección hacia la meta."""
            vector_a_meta = self.get_vector_a_meta(posicion_meta)
            unidad_vector_meta = self.normalize(vector_a_meta)
            p_punto = np.dot(self.direccion, unidad_vector_meta)
            cruz = np.linalg.det(np.array([self.direccion, unidad_vector_meta]))
            return p_punto, cruz
        
    def calculo_control(self, posicion_meta):
            """Calcula el control necesario para mover a Wall-E hacia la posición meta."""
            _, cruz = self.calculo_de_alineacion(posicion_meta)
            delta_v = self.K * cruz #Delta velocidad = K * (D x E)
            return delta_v
        
    def __repr__(self):
            return f"Posicion: {self.posicion}, Direccion: {self.direccion}, Theta: {np.grados(self.theta): 1.f} °"