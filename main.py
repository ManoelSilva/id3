import os
import utils.config as uc
import utils.csv as ucsv
import algoritmo.arvore_de_decisao as ad

class MainProgram:
    d_config = None
    atr_alvo = None
    id3 = None
    menu_actions = None

    def __init__(self):
        self.d_config = uc.carregar_config_csv('csv.cfg')
        self.atr_alvo = self.d_config['target']
        
        d_csv = ucsv.carregar_csv_d_cabecalho(self.d_config['csv_file'])
        d_csv = ucsv.montar_d_csv(d_csv, self.d_config['csv_columns'])
        
        atributos_separados = set(d_csv['cabecalho'])
        atributos_separados.remove(self.atr_alvo)
        
        id3Obj = ad.Id3(ucsv.valores_unicos(d_csv), self.atr_alvo)
        self.id3 = id3Obj.montar_id3(d_csv, atributos_separados)

        self.menu_actions = { 'main_menu': self.main_menu, '1': self.exibir_id3, '3': self.exit, }

    def exibir_id3(self):
        p_array = []
        set_regras = set()

        def traverse(no, p_array, set_regras):
            if 'rotulo' in no:
                p_array.append(' o ' + self.atr_alvo + ' É ' + no['rotulo'])
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

        traverse(self.id3, p_array, set_regras)
        print(os.linesep.join(set_regras))

        pass
        self.main_menu(False)

    def main_menu(self, clear):
        if clear:
            os.system('clear')
        
        print('Bem vindo,\n')
        print('Selecione a opção desejada:')
        print('1. Exibir árvore de decisão')
        print('2. Realizar predição')
        print('\n3. Sair')
        choice = input(' >>  ')
        self.exec_menu(choice)
    
        return

    def exec_menu(self, choice):
        os.system('clear')
        ch = choice.lower()
        if ch == '':
            self.menu_actions['main_menu'](True)
        else:
            try:
                self.menu_actions[ch]()
            except KeyError:
                print('Seleção inválida, por favor tente novamente.\n')
                self.menu_actions['main_menu'](True)
        return
    
    def exit(self):
        exit()
        return

    def back(self):
        self.menu_actions['main_menu']()

if __name__ == '__main__': 
    prg = MainProgram()
    prg.main_menu(True)