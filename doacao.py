class Doacao:
    def __init__(self, id_doacao, titulo, quantidade, validade, categoria):
        self.id_doacao = id_doacao
        self.titulo = titulo
        self.quantidade = quantidade
        self.validade = validade
        self.categoria = categoria
        self.status = "Disponivel"

    def reservar(self):
        if self.status == "Disponivel":
            self.status = "Reservado"
            return True
        return False

    def entregar(self):
        if self.status == "Reservado":
            self.status = "Entregue"
            return True
        return False

    def cancelar_reserva(self):
        if self.status == "Reservado":
            self.status = "Disponivel"
            return True
        return False

    def alterar_quantidade(self, nova_quantidade):
        if nova_quantidade > 0:
            self.quantidade = nova_quantidade
            return True
        return False