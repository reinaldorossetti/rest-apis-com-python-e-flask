class Funcionario():

    aumento = 1.05

    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def dados(self):
        return {'nome': self.nome, 'salário': self.salario}

    def aplicar_aumento(self):
        self.salario = self.salario * self.aumento

    @classmethod
    def definir_novo_aumento(cls, novo_aumento):
        cls.aumento = novo_aumento

test = Funcionario('Reinaldo', 11460)
Funcionario.definir_novo_aumento(1.1)
test.aplicar_aumento()
print(test.dados())