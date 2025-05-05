import numpy as np

class WallE:
    def __init__(self, posicion_inicial=(0.0, 0.0), direccion_inicial=(0.0, 0.0)):
        self.posicion = np.array(posicion_inicial, dtype=float)
        self.direccion = self.normalize(np.array)(direccion_inicial, dtype=float)
        self.velocidad = 2.0 #unidades de la velocidad
        self.K = 4.0 #Ganancia para el control de direccion

        def normalize(self, v):
            norm = np.linalg.norm(v)
            return v / norm if norm != 0 else v
        
        def movimiento_frente(self):
            self.posicion += self.velocidad * self.direccion
        
        def rotacion(self, angulo_de_rotacion):
            angulo = np.radians(angulo_de_rotacion)
            matriz_rotacion = np.array([
                [np.cos(angulo), -np.sin(angulo)]
                [np.sin(angulo), np.cos(angulo)]
            ])
            self.direccion = self.normalize(matriz_rotacion @ self.direccion)

        def get_vector_a_meta(self, posicion_meta):
            return np.array(posicion_meta) - self.posicion
        
        def calculo_de_alineacion(self, posicion_meta):
            vector_a_meta = self.get_vector_a_meta(posicion_meta)
            unidad_vector_meta = self.normalize(vector_a_meta)
            p_punto = np.dot(self.direccion, unidad_vector_meta)
            cruz = np.linalg.det(np.array([self.direccion, unidad_vector_meta]))
            return p_punto, cruz
        
        def calculo_control(self, posicion_meta):
            _, cruz = self.calculo_de_alineacion(posicion_meta)
            delta_v = self.K * cruz #Delta velocidad = K * (D x E)
            return delta_v
        
        def __repr__(self):
            return f"Posicion: {self.posicion}, Direccion: {self.direccion}"