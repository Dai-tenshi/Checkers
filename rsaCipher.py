#Выбрать два простых различных числа
p, q = 89, 107
#Вычислить произведение
n = p * q
#Вычислить функцию Эйлера
fi = (p - 1) * (q - 1)
#Выбрать открытую экспоненту
en = 3


#Вычислить секретную экспоненту
def dec_key(en):
    i = 2
    while i < 20:
        formula = (1 + fi * i) % en
        dec = int((1 + fi * i) / en)
        if (formula == 0 and dec != en):
            return (dec)
        i = i + 1

dec = dec_key(en)
encrypte = []
decrypte = []

#Вычислить шифротекст
def encrypt(val):
    cypher = (val ** en) % n
    return (cypher)


#Вычислить исходное сообщение
def decrypt(val):
    decr = (val ** dec) % n
    return(decr)


#Итоговая функция шифрования
def rsa_encrypt(text):
    global encrypte
    for i in range(len(text)):
        encrypte.append(encrypt(ord(text[i])))
    return encrypte


#Итоговая функция дешифрования
def rsa_decrypt(encrypt_result):
    global encrypte
    global decrypte
    for i in range(len(encrypt_result)):
        decrypte.append(chr(decrypt(encrypte[i])))
    decrypte = ''.join(decrypte)
    return decrypte

