from abc import ABC, abstractmethod
import logging

# CONFIGURACIÓN DE LOGS
logging.basicConfig(
    filename="sistema.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# EXCEPCIONES PERSONALIZADAS
# =========================
class SistemaError(Exception): pass
class ValidacionError(SistemaError): pass
class ReservaError(SistemaError): pass

# =========================
# CLASE ABSTRACTA BASE
# =========================
class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

# =========================
# CLIENTE
# =========================
class Cliente(Entidad):
    def __init__(self, nombre, edad, email):
        if not nombre or not isinstance(nombre, str):
            raise ValidacionError("Nombre inválido: debe ser texto.")
        if edad < 18:
            raise ValidacionError(f"Cliente {nombre} es menor de edad.")
        if "@" not in email:
            raise ValidacionError(f"Email inválido: {email}")

        self.__nombre = nombre  
        self.__edad = edad
        self.__email = email

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} | Email: {self.__email}" 

# =========================
# SERVICIO ABSTRACTO
# =========================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# =========================
# SERVICIOS DERIVADOS
# =========================
class ReservaSala(Servicio): 
    def calcular_costo(self, horas, tasa_limpieza=50): 
        return (self.precio_base * horas) + tasa_limpieza

    def descripcion(self):
        return f"Servicio: {self.nombre} (Reserva de salas)"

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias, descuento=0.10): 
        total = self.precio_base * dias
        return total * (1 - descuento)

    def descripcion(self):
        return f"Servicio: {self.nombre} (Alquiler de equipos)"

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones, impuesto=0.19): 
        return (self.precio_base * sesiones) * (1 + impuesto)

    def descripcion(self):
        return f"Servicio: {self.nombre} (Asesoría especializada)"

# =========================
# RESERVA
# =========================
class Reserva:
    def __init__(self, cliente, servicio, cantidad):
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaError("Cliente inválido")
            if not isinstance(servicio, Servicio):
                raise ReservaError("Servicio inválido")
            if cantidad <= 0:
                raise ReservaError("Cantidad/Duración inválida")

            self.cliente = cliente
            self.servicio = servicio
            self.cantidad = cantidad 
            self.estado = "pendiente"

        except Exception as e:
            logging.error(f"Fallo en creación de reserva: {e}")
            raise ReservaError("Error crítico al inicializar la reserva") from e
            
    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.cantidad)
        except Exception as e:
            logging.error(f"Error en cálculo de costo: {e}")
            self.estado = "Fallida"
        else:
            self.estado = "Confirmada"
            print(f"Reserva exitosa: {self.servicio.descripcion()} | Costo: {costo}")
        finally: 
            print(f"Finalizando proceso de reserva. Estado: {self.estado}")

# =========================
# SIMULACIÓN (10 OPERACIONES)
# =========================
def ejecutar_sistema():
    print("--- SISTEMA DE GESTIÓN SOFTWARE FJ ---")
    clientes = []
    servicios = [
        ReservaSala("Sala Juntas", 80),
        AlquilerEquipo("Laptop", 25),
        AsesoriaEspecializada("Soporte Técnico", 150)
    ]

    operaciones = [
        lambda: clientes.append(Cliente("Juan Perez", 25, "juan@mail.com")),    
        lambda: clientes.append(Cliente("Niño", 10, "nino@mail.com")),          
        lambda: clientes.append(Cliente("Marta", 30, "marta_sin_correo")),      
        lambda: Reserva(clientes[0], servicios[0], 4).procesar(),            
        lambda: Reserva(clientes[0], servicios[1], 2).procesar(),               
        lambda: Reserva(clientes[0], servicios[2], 1).procesar(),            
        lambda: Reserva("Soy un String", servicios[0], 5).procesar(),          
        lambda: clientes.append(Cliente("Lucia Gomez", 21, "lucia@mail.com")), 
        lambda: Reserva(clientes[-1], servicios[1], 3).procesar(),              
        lambda: Reserva(clientes[0], servicios[0], -5).procesar()               
    ]

    for i, op in enumerate(operaciones, 1):
        print(f"\nOperación #{i}:")
        try:
            op()
        except Exception as e:
            logging.error(f"Error controlado en operación {i}: {e}")
            print(f"CONTROLADO: {e}")

if __name__ == "__main__":
    ejecutar_sistema()
