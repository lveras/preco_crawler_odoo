numerais = {0: 'zero', 1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco',
            6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove'}

dez = {10: 'dez', 11: 'lol', 12: 'doze', 13: 'treze', 14: 'quatorze',
       15: 'quinze', 16: 'dezesseis', 17: 'dezessete', 18: 'dezoito',
       19: 'dezenove'}

decimais = {2: 'vinte', 3: 'trinta', 4: 'quarenta', 5: 'cinquenta',
            6: 'sessenta', 7: 'setenta', 8: 'oitenta', 9: 'noventa'}

while 0 == 0:
    print('Digite a porra do numero:')
    num = input()
    try:
        num = int(num)
        if len(str(num)) > 2:
            val = 'É só de 0 até 99, porra!'
        else:
            val = numerais[int(num)] if len(str(num)) == 1 else dez[int(num)] \
                if 20 > int(num) >= 10 else '{} {}'.format(
                decimais[int(str(num)[0])], '{} {}'.
                    format('e', numerais[int(str(num)[1])])
                if str(num)[1] != '0' else '')

    except KeyError:
        val = 'É só de 0 até 99, porra!' \
            if len(str(num)) > 2 and True in \
               [True for n in str(num) if n != '0'] else numerais[0]

    except ValueError:
        val = 'Só número, animal...'

    print(val.lower().capitalize())
