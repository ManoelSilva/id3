import os
import utils.config as uc
import utils.csv as ucsv
import algoritmo.arvore_de_decisao as ad


def exibir_id3(id3, atr_alvo):
    p_array = []
    set_regras = set()

    def traverse(no, p_array, set_regras):
        if 'rotulo' in no:
            p_array.append(' o ' + atr_alvo + ' É ' + no['rotulo'])
            set_regras.add(''.join(p_array))
            p_array.pop()
        elif 'atributo' in no:
            strif = 'SE ' if not p_array else ' E '
            p_array.append(strif + no['atributo'] + ' IGUAL ')
            for n in no['nos']:
                p_array.append(n)
                traverse(no['nos'][n], p_array, set_regras)
                p_array.pop()
            p_array.pop()

    traverse(id3, p_array, set_regras)
    print(os.linesep.join(set_regras))

    pass

def main():

    d_config = uc.carregar_config_csv('csv.cfg');
    d_csv = ucsv.carregar_csv_d_cabecalho(d_config['csv_file'])
    d_csv = ucsv.montar_d_csv(d_csv, d_config['csv_columns'])
    atributo_alvo = d_config['target']
    atributos_separados = set(d_csv['cabecalho'])

    atributos_separados.remove(atributo_alvo)

    uniqs = ucsv.valores_unicos(d_csv)
    id3 = ad.montar_id3(d_csv, uniqs, atributos_separados, atributo_alvo)

    exibir_id3(id3, atributo_alvo)



if __name__ == "__main__": main()