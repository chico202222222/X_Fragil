import bcrypt


def gerar_hash(senha):
    if len(senha.encode('utf-8')) > 72:
        raise ValueError('Senha deve ter no máximo 72 bytes')
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verificar_senha(senha, hash_salvo):
    try:
        return bcrypt.checkpw(senha.encode('utf-8'), hash_salvo.encode('utf-8'))
    except ValueError:
        return False
