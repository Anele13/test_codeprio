class MovimientoException(Exception):
    pass

class SaldoInsuficienteException(MovimientoException):
    def __init__(self, saldo_cuenta):
        self.saldo_cuenta = saldo_cuenta

    def __str__(self):
        return f'Saldo insuficiente. Saldo actual: {self.saldo_cuenta}'