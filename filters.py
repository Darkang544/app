def currencyFormat(value):
    # Formato europeo: 1.234,56 € (punto para miles, coma para decimales)
    value = float(value)
    if value == 0:
        return "- €"
    else:
        return "{:,.2f} €".format(value).replace('.', '_').replace(',', '.').replace('_', ',')
