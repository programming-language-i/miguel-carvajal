def suma(valor1, valor2):
    return valor1 + valor2

def resta(valor1, valor2):
    return valor1 - valor2

def multiplicacion(valor1, valor2):
    return valor1 * valor2

def division(valor1, valor2):
    if valor2 != 0:
        return valor1 / valor2
    else:
        return "Error: Division by zero is not allowed."



resultado_suma = suma(3, 5)
print(f"El resultado de la suma es: {resultado_suma}")

resultado_resta = resta(10, 4)
print(f"El resultado de la resta es: {resultado_resta}")

resultado_multiplicacion = multiplicacion(6, 7)
print(f"El resultado de la multiplicación es: {resultado_multiplicacion}")

resultado_division = division(20, 4)
print(f"El resultado de la división es: {resultado_division}")




