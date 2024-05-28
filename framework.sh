#!/bin/bash

#Menu
fn menu() {
clear
t_file="13123"
n_file="22323423434"
b_file="1258"
t_size="123 MB"
n_size="22238563 TB"
b_size="1234 GV"
t_dirs="185623"
n_dirs="258623234"
b_dirs="156234"

echo -e "
                ██████╗  ██╗  ██████╗    ██████╗  ██████╗  ██╗ ██╗   ██╗ ███████╗
                ██╔══██╗ ██║ ██╔═══██╗   ██╔══██╗ ██╔══██╗ ██║ ██║   ██║ ██╔════╝
                ██████╔╝ ██║ ██║   ██║   ██║  ██║ ██████╔╝ ██║ ██║   ██║ █████╗  
                ██╔══██╗ ██║ ██║   ██║   ██║  ██║ ██╔══██╗ ██║ ╚██╗ ██╔╝ ██╔══╝  
                ██████╔╝ ██║ ╚██████╔╝   ██████╔╝ ██║  ██║ ██║  ╚████╔╝  ███████╗
     
     
    ________________________________________________________________________________________ 
    | Informação  ||  Disponivel(Online)  ||    Por Atualizar      ||       Backup          |
    |-------------||----------------------||-----------------------||-----------------------|
    | Ficheiros   ||  $(printf "%-20s" "${t_file}")|| $(printf "%-20s" "${n_file}")|| $(printf "%-20s" "${b_file}")|
    | Tamanho     ||  $(printf "%-20s" "${t_size}")|| $(printf "%-20s"  "${n_size}")|| $(printf "%-20s" "${b_size}")|
    | Pastas      ||  $(printf "%-20s" "${t_dirs}")|| $(printf "%-20s" "${n_dirs}")|| $(printf "%-20s" "${b_dirs}")|
    |_____________||______________________||_______________________||_______________________|

Opções:
 [1]  Verificar Ficheiros novos
 [2]  Atualizar Database       
 [3]  Backup Completo          
 [4]  Sair                     

Selecione uma opção (1-4):"
read option
}

if [ "$option" == "1" ]; then
    python -c "from support.py import opcao_1; opcao_1()"
    echo ""
    echo "Terminado! Prime qualquer tecla para voltar ao menu..."
    read
    menu

elif [ "$option" == "2" ]; then
    python -c "from support.py import opcao_2; opcao_2()"
    echo ""
    echo "Terminado! Prime qualquer tecla para voltar ao menu..."
    read
    menu
    
elif [ "$option" == "3" ]; then
    python -c "from support.py import opcao_3; opcao_3()"
    echo.
    echo "Terminado! Prime qualquer tecla para voltar ao menu..."
    read
    menu

elif [ "$option" == "4" ]; then
    exit
else
    echo "Opcão Invalida"
    echo ""
    echo "Regressar ao menu em 5 segundos..."
    sleep 1
    menu
fi
