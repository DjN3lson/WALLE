class Grid:
    def __init__(self, width=10, height=10):
        self.width=width
        self.height=height

        self.cubos_basura = {
            (1, 1): True,
            (5, 6): True,
            (7, 1): True
        }

        self.basura_colectada = []
        self.basurero = (8,9)
        
        def tiene_basura(self, posicion):
            """Verifica si hay basura en una posicion."""
            pos = tuple(map(int, posicion))
            return self.trash_posicion.get(pos,False)
        
        def basura_colectada(self, posicion):
            """Recoge basura si hay en la posicion."""
            pos = tuple(map(int, posicion))
            if self.tiene_basura(pos):
                self.posicion_basura[pos] = False
                self.basura_colectada.append(pos)
                print(f"basura recogida en {pos}")

        def depositar_basura(self, posicion):
            """Deposita basura si el robot llega al basurero"""
            pos = tuple(map(int, posicion))
            if pos == self.basurero and self.basura_colectada:
                print(f"WALL-E deposito {len(self.basura_colectada)} bloques de basura.")
                self.basura_colectada.clear()

        def is_within_bound(self, posicion):
            x,y = map(int, posicion)
            return 0 <= x < self.width and 0 <= y <self.height
        
        def get_basura_posicion(self, posicion):
            """Devuelve las posiciones donde aun hay basura"""
            return [pos for pos, active in self.posicion_basura.items() if active]
        
        def __repr__(self):
            return f"Basura en: {self.get_basura_posicion()} | Recogida:{self.basura_colectada}"