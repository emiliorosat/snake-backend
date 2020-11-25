from datetime import date

def ObrenerSigno(fecha: date):
    dia = fecha.day
    switch = {
        1: enero(dia),
        2: febrero(dia),
        3: marzo(dia),
        4: abril(dia),
        5: mayo(dia),
        6: junio(dia),
        7: julio(dia),
        8: agosto(dia),
        9: septiembre(dia),
        10: octubre(dia),
        11: noviembre(dia),
        12: diciembre(dia)
    }
    return switch[fecha.month]

    

def enero(dia):
    if dia >=21:
        return "Acuario"
    else:
        return "Capricornio"
def febrero(dia):
    if dia >= 19:
        return "Piscis"
    else:
        return "Acuario"
def marzo(dia):
    if dia >=21:
        return "Aries"
    else:
        return "Piscis"
def abril(dia):
    if dia >=21:
        return "Tauro"
    else:
        return "Aries"
def mayo(dia):
    if dia >=21:
        return "Geminis"
    else:
        return "Tauro"
def junio(dia):
    if dia >=22:
        return "Cancer"
    else:
        return "Geminis"
def julio(dia):
    if dia >=23:
        return "Leo"
    else:
        return "Cancer"
def agosto(dia):
    if dia >=23:
        return "Virgo"
    else:
        return "Leo"
def septiembre(dia):
    if dia >=23:
        return "Libra"
    else:
        return "Virgo"
def octubre(dia):
    if dia >=23:
        return "Escorpion"
    else:
        return "Libra"
def noviembre(dia):
    if dia >=23:
        return "Sagitario"
    else:
        return "Escorpion"
def diciembre(dia):
    if dia >=22:
        return "Capricornio"
    else:
        return "Sagitario"