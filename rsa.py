from secrets import randbelow
from math import gcd

def primo(num):
    if num == 2:
        return True

    if num < 2 or num % 2 == 0:
        return False

    for n in range(3, num, 2):
        if num % n == 0:
            return False

    return True

def egcd(a, b):
    if a == 0:
        return b, 0, 1

    g, x, y = egcd(b % a, a)

    return g, y - (b // a) * x, x

def modinv(a, m):
    g, x, y = egcd(a, m)

    if g != 1:
        raise Exception('Sem inversão modular')

    return x % m

def pow_mod(x, y, z):
    num = 1

    while y:
        if y & 1:
            num = num * x % z

        y >>= 1            
        x = x * x % z

    return num


class RSA(object):    
    @property
    def chave_publica(self):
        return self.n, self.e
    
    @property
    def chave_privada(self):
        return self.p, self.q, self.d    
    
    def gerar_primos(self, limite):
        self.p = randbelow(limite)
        self.q = randbelow(limite)
        
        while not primo(self.p):
            self.p = randbelow(limite)
        
        while self.p == self.q or not primo(self.q):
            self.q = randbelow(limite)
        
    def calcular_n(self):
        self.n = self.p * self.q
    
    def calcular_phi(self):
        self.phi = (self.p - 1) * (self.q - 1)
    
    def gerar_e(self):
        self.e = randbelow(self.phi)
        
        if self.e < 2 or gcd(self.e, self.phi) != 1:
            self.gerar_e()
            
    def calcular_d(self):
        self.d = modinv(self.e, self.phi)
    
    def gerar_chaves(self, limite=10**7):
        self.gerar_primos(limite)
        self.calcular_n()
        self.calcular_phi()
        self.gerar_e()
        self.calcular_d()
    
    @staticmethod
    def encriptar(mensagem, chave_publica):
        n, e = chave_publica
        
        mensagem_ascii = [ord(caractere) for caractere in mensagem]
        mensagem_encriptada = [str(pow_mod(caractere_ascii, e, n)) for caractere_ascii in mensagem_ascii]
        
        return ' '.join(mensagem_encriptada)
    
    @staticmethod
    def desencriptar(mensagem_encriptada, chave_privada=None):
        p, q, d = chave_privada

        mensagem_encriptada = mensagem_encriptada.split(' ')
        mensagem_ascii = [pow_mod(int(caractere_encriptado), d, p * q) for caractere_encriptado in mensagem_encriptada]
        mensagem = [chr(caractere_ascii) for caractere_ascii in mensagem_ascii]
        
        return ''.join(mensagem)
