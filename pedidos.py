import ast
import sys
import unittest

def classificarSituacao(pedidos, tempo):
    return "CRÍTICO" if pedidos >= 5 or tempo > 600 else "ELEVADA" if pedidos >= 3 or tempo > 480 else "NORMAL"

def analisarPedidos(lista):
    pedidosUrgentes = 0
    tempoTotal = 0
    pedidoMaior = 0
    situacao = ""
    for prioridade, tempo in lista:
        if not ((1 <= prioridade <= 5) and tempo > 0):
            tempoTotal += 30
            continue
        if prioridade <= 2:
            pedidosUrgentes += 1
        if pedidoMaior < tempo:
            pedidoMaior = tempo
        tempoTotal += tempo

    situacao = classificarSituacao(pedidosUrgentes, tempoTotal)

    print(f"Número de pedidos urgentes: {pedidosUrgentes}")
    print(f"Tempo total estimado: {tempoTotal}")
    print(f"Tempo médio por pedido: {tempoTotal/10}")
    print(f"Pedido de maior duração: {pedidoMaior}")
    print(f"Situação atual: {situacao}")

    return (pedidosUrgentes, tempoTotal, pedidoMaior, situacao)

class TestAnalisePedidos(unittest.TestCase):
    
    def test_t1_normal(self):
        """T1: Cenário Normal - Pedidos válidos dentro do esperado."""
        lista = [
            (3, 40), (1, 50), (4, 30), (2, 60), (5, 20),
            (3, 45), (1, 55), (4, 25), (2, 35), (3, 50)
        ]
        p_urg, t_tot, p_maior, situacao = analisarPedidos(lista)
        self.assertEqual(p_urg, 4)        # 4 pedidos com prioridade <= 2
        self.assertEqual(t_tot, 410)      # Soma total dos tempos
        self.assertEqual(p_maior, 60)     # Maior tempo individual
        self.assertEqual(situacao, "ELEVADA")

    def test_t2_prioridade_invalida(self):
        """T2: Inválido — Prioridade fora do intervalo [1, 5] com tempo > 0."""
        lista = [
            (6, 50), 
            (1, 40),
            (0, 60)]
        p_urg, t_tot, p_maior, situacao = analisarPedidos(lista)
        self.assertEqual(p_urg, 1)        
        self.assertEqual(t_tot, 100)      
        self.assertEqual(p_maior, 40)

    def test_t3_tempo_invalido_ou_zero(self):
        """T3: Inválido — Prioridade inválida com tempo <= 0."""
        lista = [
            (6, 0), 
            (3, 50)
        ]
        p_urg, t_tot, p_maior, situacao = analisarPedidos(lista)
        self.assertEqual(p_urg, 0)
        self.assertEqual(t_tot, 80)

    def test_t4_fronteira(self):
        """T4: Fronteira - Limites exatos de prioridade (1 e 5) e tempo (480)."""
        lista = [
            (1, 450), 
            (5, 0)
        ]
        p_urg, t_tot, p_maior, situacao = analisarPedidos(lista)
        self.assertEqual(p_urg, 1)
        self.assertEqual(t_tot, 480)
        self.assertEqual(situacao, "NORMAL") 

    def test_t5_extremo(self):
        """T5: Extremo - Volume alto de urgência gerando classificação CRÍTICO."""
        lista = [
            (1, 100), (2, 100), (1, 100), (2, 100), (1, 100), (3, 150)
        ]
        p_urg, t_tot, p_maior, situacao = analisarPedidos(lista)
        self.assertEqual(p_urg, 5)       
        self.assertEqual(t_tot, 650)      
        self.assertEqual(situacao, "CRÍTICO")

    def test_t6_regressao(self):
        """T6: Regressão - Combinação de múltiplos cenários para garantir robustez."""
        lista = [
            (2, 200), (3, 200), (99, 50)
        ]
        p_urg, t_tot, p_maior, situacao = analisarPedidos(lista)
        self.assertEqual(p_urg, 1)
        self.assertEqual(t_tot, 430)
        self.assertEqual(situacao, "NORMAL")

def main():
    continuar = False
    lista = []

    if len(sys.argv) > 2:
        print("Usage: python3 pedidos.py {-t}")

    if len(sys.argv) > 1:
        if sys.argv[1] == "-t":
            sys.argv = [sys.argv[0]]
            unittest.main()
            return
        else:
            print("Wrong argument.\n")   
    

    while not continuar:
        try:
            lista = ast.literal_eval(input("Lista de pedidos: "))
        except (ValueError, SyntaxError):
            print("A lista deve ser no formato [(prioridade, tempo), ...]")
            continue

        print("\n")

        if not isinstance(lista, list):
            print("O input deve ser uma lista.")
            continue


        if len(lista) != 10:
            print(f"A lista deve ter 10 pedidos. Foram passados {len(lista)}.")
            continue

        valido = all(
            isinstance(p, tuple)
            and len(p) == 2
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in p)
            for p in lista
        )
        if not valido:
            print("Cada pedido deve ser um tuplo (prioridade, tempo) com dois números.")
            continue

        continuar = True


    analisarPedidos(lista)
    
if __name__ == "__main__":
    main()