import ast
import csv
import sys
import math
import os


def get_rotulos(d, atributo_alvo):
    linhas = d['linhas']
    # print(atributo_alvo)
    # input()
    col_idx = d['nome_p_idx'][atributo_alvo]
    rotulos = {}

    for linha in linhas:
        val = linha[col_idx]
        if val in rotulos:
            rotulos[val] = rotulos[val] + 1
        else:
            rotulos[val] = 1
    return rotulos


def entropia_calc(n, rotulos):
    ent = 0
    for label in rotulos.keys():
        p_x = rotulos[label] / n
        ent += - p_x * math.log(p_x, 2)
    return ent


def montar_particao(d, at_sep):
    particoes = {}
    linhas = d['linhas']
    atr_particao_idx = d['nome_p_idx'][at_sep]
    for linha in linhas:
        v_linha = linha[atr_particao_idx]
        if v_linha not in particoes.keys():
            particoes[v_linha] = {
                'nome_p_idx': d['nome_p_idx'],
                'idx_p_nome': d['idx_p_nome'],
                'linhas': list()
            }
        particoes[v_linha]['linhas'].append(linha)
    return particoes


def media_ent_particoes(d, at_sep, atributo_alvo):
    linhas = d['linhas']
    l = len(linhas)
    particoes = montar_particao(d, at_sep)
    media_ent = 0

    for cp in particoes.keys():
        part = particoes[cp]
        n_part = len(part['linhas'])
        # print(atributos_sep)
        # input()
        rotulos_part = get_rotulos(part, atributo_alvo)
        ent_part = entropia_calc(n_part, rotulos_part)
        media_ent += n_part / l * ent_part

    return media_ent, particoes


def get_rotulo_comum(rotulos):
    rc = max(rotulos, key=lambda k: rotulos[k])
    return rc


def montar_id3(d, uniqs, atributos_sep, atributo_alvo):
    rotulos = get_rotulos(d, atributo_alvo)
    no = {}

    if len(rotulos.keys()) == 1:
        no['rotulo'] = next(iter(rotulos.keys()))
        return no

    if len(atributos_sep) == 0:
        no['rotulo'] = get_rotulo_comum(rotulos)
        return no

    gim = None
    gim_atr = None
    gim_part = None
    l = len(d['linhas'])
    ent = entropia_calc(l, rotulos)

    for at_sep in atributos_sep:
        media_ent, particoes = media_ent_particoes(d, at_sep, atributo_alvo)
        gi = ent - media_ent
        if gim is None or gi > gim:
            gim = gi
            gim_atr = at_sep
            gim_part = particoes

    if gim is None:
        no['rotulo'] = get_rotulo_comum(rotulos)
        return no

    no['atributo'] = gim_atr
    no['nos'] = {}

    atributos_sep_sub_arv = set(atributos_sep)
    atributos_sep_sub_arv.discard(gim_atr)

    atrs_uniq = uniqs[gim_atr]

    for atr in atrs_uniq:
        if atr not in gim_part.keys():
            no['nos'][atr] = {'rotulo': get_rotulo_comum(rotulos)}
            continue
        partition = gim_part[atr]
        no['nos'][atr] = montar_id3(partition, uniqs, atributos_sep_sub_arv, atributo_alvo)

    return no    
