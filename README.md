<h1> Bioquimica-OneDriveSync </h1>

* [Informação Geral](#informação-geral)
* [Bibliotecas Usadas](#bibliotecas-usadas)
* [Setup](#setup)
* [Languagues](#languagues)

![Screenshot 2024-05-28 043429](https://github.com/MKVO-pts/Bioquimica-OneDriveSync/assets/76405447/9c9eb68b-4d2e-417c-85ef-448b700997f6)

## Informação Geral

Para ser mais rápido/eficiente a verificação se os novos materiais já existem ou não é feita automaticamente da seguinte forma: 
1. Os ficheiros são submetidos pelo "Forms" vão para uma pasta diferente
2. O programa vai à pasta e compara se o conteúdo submetidos já existe na drive  (Curiosidade: Calcula e compara os CheckSum dos ficheiros)
3. Um "Report" é criado a dizer quais são os ficheiros novos e repetidos
4. Os novos são adicionados à Drive


*Para além disto ainda faz mais algumas coisas só para guarantir que corre tudo bem  
Algumas funcionabilidades:
- Verifica automaticamente se há novas submissões e se já existem;
- Guarante os ficheiros não são corrompidos durante Upload/Download;
- Lista ficheiros e pastas;
- Backup e logs de Alterações;
- Etc...

## Bibliotecas Usadas

hashlib (calcular CheckSum usando MD5)
dotenv (Variáveis sistema seguras)
datetime (log de datas)


 
## Setup
first use git clone download the project, then run the install.sh
```
$ git clone https://github.com/MKVO-pts/Bioquimica-OneDriveSync.git
$ cd Bioquimica-OneDriveSync
$ bash install.sh (ainda não existe)
```

## Languagues
This program only use bach and python  
###### Made by MKvO
