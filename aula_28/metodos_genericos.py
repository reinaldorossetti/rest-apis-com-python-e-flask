# args antes do kwargs
def metodo_kwargs(*args, **kwargs):
    print(args)
    print(kwargs)

metodo_kwargs(3, 'ask', 4, 'qualquer q seja', nome='Ana', idade=25)