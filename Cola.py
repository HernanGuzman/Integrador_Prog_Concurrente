class Cola:
    def __init__(self):
        self.cola = []

    def encolar(self, elemento):
        self.cola.insert(0, elemento)

    def desencolar(self):
        dato = None
        if not self.estaVacia():
            dato = self.cola.pop()
        return dato

    def top(self):
        dato = None
        if not self.estaVacia():
            dato = self.cola[len(self.cola)-1]
        return dato

    def estaVacia(self):
        return len(self.cola) == 0

    def len(self):
        return len(self.cola)
