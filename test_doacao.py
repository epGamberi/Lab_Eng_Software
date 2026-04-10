import unittest
from doacao import Doacao

class TestDoacao(unittest.TestCase):

    # Roda antes de cada teste para criar um objeto limpo
    def setUp(self): 
        self.doacao = Doacao(1, "5kg de Arroz", "5", "2026-03-30", "Não-perecível")

    # Teste 1: Verifica se a doação é criada com os dados certos e status inicial
    def test_criacao_doacao(self):
        self.assertEqual(self.doacao.titulo, "5kg de Arroz")
        self.assertEqual(self.doacao.status, "Disponivel")

    # Teste 2: Verifica o fluxo de reserva
    def test_reservar_doacao(self):
        sucesso = self.doacao.reservar()
        self.assertTrue(sucesso)
        self.assertEqual(self.doacao.status, "Reservado")

    # Teste 3: Verifica se uma instituição não consegue reservar algo já reservado
    def test_impedir_reserva_duplicada(self):
        self.doacao.reservar() # Reserva a primeira vez
        sucesso_segunda_vez = self.doacao.reservar() # Tenta de novo
        self.assertFalse(sucesso_segunda_vez)
        self.assertEqual(self.doacao.status, "Reservado")

    # Teste 4: Verifica o fluxo de entrega (UC5)
    def test_entregar_doacao(self):
        self.doacao.reservar() # Precisa estar reservado primeiro
        sucesso = self.doacao.entregar()
        self.assertTrue(sucesso)
        self.assertEqual(self.doacao.status, "Entregue")

    # Teste 5: Verifica o fluxo de cancelamento de reserva (UC6)
    def test_cancelar_reserva(self):
        self.doacao.reservar()
        sucesso = self.doacao.cancelar_reserva()
        self.assertTrue(sucesso)
        self.assertEqual(self.doacao.status, "Disponivel")

if __name__ == '__main__':
    unittest.main()