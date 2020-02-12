import re
from itertools import combinations

def otkryvalka_fayla (put_k_faylu):
    """ Получаем на вход путь к исходному файлу
    считываем файл в строку
    возвращаем строку
    """
    with open (put_k_faylu, 'r') as openfile:
        fayl_kak_stroka = openfile.read()
        return fayl_kak_stroka

def vydelyalka_obyektov (kakoy_to_text):
    """ Получаем на вход текст
    Возвращаем список интересующих нас в этом тексте объектов
    (как список строк) -- это будущие узлы нашего графа
    """
    obyekty = re.findall (r'[А-ЯЁ][а-яё]+',kakoy_to_text) # намеренно примитивная логика
    # как раз здесь вы можете встроить что угодно более сложное
    return obyekty

def vydelyalka_svyazey (abzac):
    """ Получаем на вход абзац как строку
    выделяем в нем все интересующие нас объекты с помощью vydelyalka_obyektov
    создаем список пар "все со всеми" при помощи combinations
    возвращаем спиоск пар
    """
    obyekty_abzaca = vydelyalka_obyektov (abzac)
    obyekty_abzaca.sort() # отсортируем, чтобы нам не мешал разный порядок пар
    spisok_svyazey_abzaca = []
    tekushaya_para = []
    spisok_svyazey_abzaca = list(combinations(obyekty_abzaca, 2))
    return spisok_svyazey_abzaca

def obhodchik_abzacev (text_s_mnojestvom_abzacev):
    """ Получаем на вход файл как строку
    превращаем его в список абзацев
    обходим абзацы
    вытаскиваем из каждого его связи с помощью vydelyalka_svyazey
    кладем все связи всех абзацев в один список
    возвращаем список
    """
    spisok_abzacev = text_s_mnojestvom_abzacev.split('\n')
    spisok_vseh_svyazey = []
    for abzac in spisok_abzacev:
        print ('Текст абзаца: ', abzac)
        svyazi_tekushego_abzaca = vydelyalka_svyazey (abzac)
        print ('Все связи абзаца: ', svyazi_tekushego_abzaca)
        spisok_vseh_svyazey.extend (svyazi_tekushego_abzaca)
    print ('Все связи в документе: ', spisok_vseh_svyazey)    
    return spisok_vseh_svyazey

## вариант записи в граф без весов (как было на паре 05.02)
def zapis_v_graf (spisok_vseh_svyazey):
    """ Получаем на вход список связей в виде пар
    превращаем его в множество пар (убиваем дубликаты)
    возвращаем множество пар
    """
    graf = set (spisok_vseh_svyazey)
    return graf

## вариант записи в граф с весами  (ниже используется он)
def zapis_v_graf_s_vesami (spisok_vseh_svyazey):
    """ Получаем на вход список связей в виде пар
    превращаем его в словарь пар
    ключ -- пара, значение -- сколько раз такая пара встретилась(это будет вес связи в графе)
    возвращаем множество пар
    """
    graf = {}
    for svyaz in spisok_vseh_svyazey:
        if svyaz in graf:
            graf [svyaz] += 1
        else:
            graf [svyaz] = 1
    return graf

def zapis_v_fayl (put_k_vyhodnomu, graf):
    """ Получаем на вход путь к выходному файлу
    и граф в виде
    -- либо множества (случай невзвешеннго графа)
    -- либо словаря (случай взвешеннго графа)
    пишем его в файл построчно: одна связь (пара, ребро) -- одна строка
    """
    with open (put_k_vyhodnomu,'w') as output_file:
        for rebro in graf:
            if type(graf) == set: # случай невзвешенного графа, полученного функцией zapis_v_graf
                output_file.write (rebro[0]+','+rebro[1]+'\n')
            elif type(graf) == dict: # случай взвешенного графа, полученного функцией zapis_v_graf_s_vesami
                ves_rebra = graf [rebro]
                output_file.write (rebro[0]+','+rebro[1]+ ',' + str(ves_rebra) + '\n')
            
if __name__ == "__main__":
    while (True):
        vhodn_fayl = input ('путь к файлу с текстом: ')
        vyhodn_fayl = input ('куда записать: ')
        otkrytiy_fayl = otkryvalka_fayla (vhodn_fayl)
        spisok_svyazey = obhodchik_abzacev(otkrytiy_fayl)
        mnojestvo_svyazey_s_vesami = zapis_v_graf_s_vesami (spisok_svyazey)
        zapis_v_fayl (vyhodn_fayl, mnojestvo_svyazey_s_vesami)
    
    
    
