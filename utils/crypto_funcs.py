import math
import random
from sympy import isprime, mod_inverse


def generate_primes(bits=8):
    p = q = 0
    while p == q:
        p = random.getrandbits(bits)
        q = random.getrandbits(bits)

        while not isprime(p): 
            p = random.getrandbits(bits)
        while not isprime(q): 
            q = random.getrandbits(bits)

    return p, q

def rsa_keygen(p, q): # Paso 1: Generar (obtener) dos números primos
    # Paso 2: Calcular n = p * q
    n = p * q

    # Paso 3: Calcular la función de Euler φ(n) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)

    # Paso 4: Elegir d tal que MCD[d, φ(n)] = 1
    d = random.randint(2, phi_n - 1)
    while math.gcd(d, phi_n) != 1:
        d = random.randint(2, phi_n - 1)

    # Paso 5: Calcular e tal que e * d ≅ 1 mod (φ(n))
    e = mod_inverse(d, phi_n)

    # Clave pública: (e, n), Clave privada: (d, n)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    message_bytes = message.encode('utf-8')
    encrypted = [pow(byte, e, n) for byte in message_bytes]
    return encrypted

def decrypt(ciphertext, private_key):
    d, n = private_key
    decrypted_bytes = bytes([pow(char, d, n) for char in ciphertext])
    return decrypted_bytes.decode('utf-8')
