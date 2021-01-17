import functools


def meu_decorador(funcao):
    @functools.wraps(funcao)
    def func_que_roda_antes():
        print(">> Embrulhando função no decorador <<")
        funcao()
        print(">> Fechando o Embrulho da função no decorador <<")

    return func_que_roda_antes()


@meu_decorador
def minha_fucao():
    print("Exec minha funcao!")
    return True


minha_fucao()
