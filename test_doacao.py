import unittest
from doacao import Doacao

class TestDoacao(unittest.TestCase):

    g# Roda antes de CADA teste
    def setUp(self):
        self.doacao = Doacao(1, "5kg de Arroz", 5, "2026-03-30", "Não-perecível")

    # Método de Teste 1
    def test_criacao_status(self):
        # Caso de Teste 1: Verifica o status default
        self.assertEqual(self.doacao.status, "Disponivel")
        # Caso de Teste 2: Verifica se os atributos foram guardados corretamente
        self.assertEqual(self.doacao.titulo, "5kg de Arroz")

    # Método de Teste 2
    def test_reservar(self):
        # Caso de Teste 1: Sucesso ao reservar item disponível
        sucesso = self.doacao.reservar()
        self.assertTrue(sucesso)
        self.assertEqual(self.doacao.status, "Reservado")
        
        # Caso de Teste 2: Falha ao tentar reservar algo que já foi reservado
        sucesso_segunda_vez = self.doacao.reservar()
        self.assertFalse(sucesso_segunda_vez)

    # Método de Teste 3
    def test_entregar(self):
        # Caso de Teste 1: Falha ao tentar entregar algo que não foi reservado
        falha = self.doacao.entregar()
        self.assertFalse(falha)

        # Caso de Teste 2: Sucesso ao entregar algo que está reservado
        self.doacao.reservar()
        sucesso = self.doacao.entregar()
        self.assertTrue(sucesso)
        self.assertEqual(self.doacao.status, "Entregue")

    # Método de Teste 4
    def test_cancelar_reserva(self):
        # Caso de Teste 1: Falha ao cancelar algo que está disponível
        falha = self.doacao.cancelar_reserva()
        self.assertFalse(falha)

        # Caso de Teste 2: Sucesso ao cancelar uma reserva ativa
        self.doacao.reservar()
        sucesso = self.doacao.cancelar_reserva()
        self.assertTrue(sucesso)
        self.assertEqual(self.doacao.status, "Disponivel")

    # Método de Teste 5
    def test_alterar_quantidade(self):
        # Caso de Teste 1: Sucesso ao colocar uma quantidade válida (> 0)
        sucesso = self.doacao.alterar_quantidade(10)
        self.assertTrue(sucesso)
        self.assertEqual(self.doacao.quantidade, 10)

        # Caso de Teste 2: Falha ao colocar quantidade inválida (<= 0)
        falha = self.doacao.alterar_quantidade(0)
        self.assertFalse(falha)
        # Garante que a quantidade anterior (10) não foi apagada
        self.assertEqual(self.doacao.quantidade, 10)

if __name__ == '__main__':
    unittest.main()