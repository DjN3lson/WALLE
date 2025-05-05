class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.posicion_basura = {
            (7,3): True,  # Solo un bloque de basura en (5,6)
            (1,6):True
        }
        self.basura_colectada = []
        self.basurero = (8, 8)
        
    def tiene_basura(self, posicion):
        """Verifica si hay basura en una posicion."""
        pos = (int(round(posicion[0])), int(round(posicion[1])))
        return self.posicion_basura.get(pos, False)
        
    def recoger_basura(self, posicion):
        """Recoge basura si hay en la posicion."""
        pos = (int(round(posicion[0])), int(round(posicion[1])))
        if pos in self.posicion_basura and self.posicion_basura[pos]:
            self.posicion_basura[pos] = False
            self.basura_colectada.append(pos)
            print(f"¡Basura recogida en {pos}! Basura restante: {len(self.get_basura_posicion())}")
            return True
        return False

    def depositar_basura(self, posicion):
        """Deposita basura si el robot llega al basurero"""
        pos = tuple(map(int, posicion))
        if pos == self.basurero and self.basura_colectada:
            print(f"WALL-E deposito {len(self.basura_colectada)} bloques de basura.")
            self.basura_colectada.clear()

    def is_within_bound(self, posicion):
        """Verifica si una posición está dentro de los límites del grid."""
        x, y = map(int, posicion)
        return 0 <= x < self.width and 0 <= y < self.height
        
    def get_basura_posicion(self):
        """Devuelve las posiciones donde aún hay basura."""
        return [pos for pos, active in self.posicion_basura.items() if active]
    
    def set_basura_posicion(self, posicion):
        return[pos for pos, active in self.posicion_basura.items() if active]

        
    def __repr__(self):
        """Representación en cadena del estado del grid."""
        return f"Basura en: {self.get_basura_posicion()} | Recogida:{self.basura_colectada}"