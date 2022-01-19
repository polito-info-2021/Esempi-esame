# Possibile soluzione esercizio "Agenda appuntamenti"

# NOTA: Dal testo non è specificato cosa succede quando si inserisce un nuovo appuntamento: il file agenda.txt
# deve essere ri-scritto (con il nuovo appuntamento)? oppure la modifica avviene solo in memoria ed il file
# rimane invariato?
# In questa soluzione proviamo ad esplorare entrambe le alternative
import operator
from pprint import pprint

FILE_AGENDA = 'agenda.txt'
FILE_COMANDI = 'comandi.txt'


def leggi_agenda(nome_file):
    agenda = []
    with open(nome_file, 'r', encoding='utf-8') as file:
        for line in file:
            campi = line.rstrip().split(';')
            appuntamento = {
                'giorno': int(campi[0]),
                'ora': int(campi[1]),
                'descrizione': campi[2]
            }
            agenda.append(appuntamento)
    return agenda


def visualizza_giornata(agenda, giorno):
    appuntamenti_del_giorno = [app for app in agenda if app['giorno'] == giorno]
    appuntamenti_del_giorno.sort(key=operator.itemgetter('ora'))

    print(f'Appuntamenti del giorno {giorno}')
    for app in appuntamenti_del_giorno:
        print(f'Giorno {giorno:3} ore {app["ora"]:2}: {app["descrizione"]}')


def aggiungi_appuntamento(agenda, appuntamento):
    # Verifica se ci sono appuntamenti in conflitto nello stesso giorno/ora
    conflitto = False
    for app in agenda:
        if app['giorno'] == appuntamento['giorno'] and app['ora'] == appuntamento['ora']:
            conflitto = True
            break
    if conflitto:
        print(f'Impossibile inserire appuntamento nel giorno {appuntamento["giorno"]} ora {appuntamento["ora"]}')
        return False
    else:
        agenda.append(appuntamento)
        print(
            f'Inserito nuovo appuntamento nel giorno {appuntamento["giorno"]} ora {appuntamento["ora"]}: {appuntamento["descrizione"]}')
        return True


# SE OCCORRE MODIFICARE IL FILE
def aggiungi_al_file(nome_file, appuntamento):
    f = open(nome_file, 'a', encoding='utf-8')
    f.write(f'{appuntamento["giorno"]};{appuntamento["ora"]};{appuntamento["descrizione"]}')
    f.close()


def main():
    agenda = leggi_agenda(FILE_AGENDA)
    pprint(agenda)
    comandi = open(FILE_COMANDI, 'r', encoding='utf-8')
    for comando in comandi:
        if comando[0].lower() == 'i':
            campi = comando.split()
            appuntamento = {
                'giorno': int(campi[1]),
                'ora': int(campi[2]),
                'descrizione': ' '.join(campi[3:])
            }
            ok = aggiungi_appuntamento(agenda, appuntamento)
            if ok:  # SE OCCORRE MODIFICARE IL FILE
                aggiungi_al_file(FILE_AGENDA, appuntamento)  # SE OCCORRE MODIFICARE IL FILE
        elif comando[0].lower() == 'v':
            giorno = int(comando.split()[1])
            visualizza_giornata(agenda, giorno)
        else:
            print(f'COMANDO ERRATO: {comando}')

    comandi.close()


main()
