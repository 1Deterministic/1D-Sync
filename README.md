# 1D-Sync
**[Português](#português)**  
* **[Aviso](#aviso)**
* **[Introdução](#introdução)**
* **[Meu caso de uso](#meu-caso-de-uso)**
* **[Pré requisitos](#pré-requisitos)**
* **[Utilização](#utilização)**
* **[Condições de seleção](#condições-de-seleção)**

**[English](#english)**  
* **[Warning](#warning)**
* **[Intro](#intro)**
* **[My use case](#my-use-case)**
* **[Requirements](#requirements)**
* **[Utilization](#utilization)**
* **[Selection conditions](#selection-conditions)**

## Português
### Aviso
**Cuidado ao ler este readme, pois ele difere entre versões do programa. Veja sempre o arquivo readme incluído na release que você baixou. Este readme, em particular, é referente à versão 2.4-alpha2**

## Introdução
**[1D-Sync](https://github.com/1Deterministic/1D-Sync)** é uma ferramenta automatizada de "sincronização" unidirecional. Com ele é possível efetuar cópias de arquivos entre pastas em intervalos específicos de tempo, suportando diversas configurações e alguns filtros de arquivos. Foi desenvolvido como uma continuação do **[Fantastic-Five-Star-Music-Copier](https://github.com/1Deterministic/Fantastic-Five-Star-Music-Copier)** mas possui recursos extras **(veja [utilização](#utilização))**.

## Meu caso de uso
Possuo um servidor de arquivos, um desktop e dois celulares com os quais sincronizo dados. Com o **[1D-Sync](https://github.com/1Deterministic/1D-Sync)**, faço com que o servidor de arquivos copie certos arquivos entre essas pastas automaticamente. Por exemplo, as músicas avaliadas em 5 estrelas são sempre copiadas para um telefone que uso como dispositivo de mídia e também para o telefone que uso no dia-a-dia. Entretanto, como esse segundo possui muito pouco espaço de armazenamento, faço com que o **[1D-Sync](https://github.com/1Deterministic/1D-Sync)** copie arquivos aleatórios até um certo tamanho (1.5GB) e os troque de tempo em tempo, de forma que eu não sinta tanto a falta de espaço. Também copio automaticamente as imagens de câmera e WhatsApp para a pasta sincronizada com meu desktop, entre outros. Para sincronizar essas pastas com os dispositivos eu utilizo o **[syncthing](https://syncthing.net/)**, que já recomendei anteriormente.

## Pré-requisitos
* **Python 3**
    * **Linux**: provavelmente já está incluído na sua distribuição. Apenas verifique o comando correto que executa a versão 3 (em algumas distros é `python` e em outras `python3`). Para verificar, rode esses comandos com o argumento **-V** e veja qual versão ele mostra
    * **Windows**: você pode rodar o instalador disponível no [site oficial](https://www.python.org/downloads/) ou instalar através do **[Chocolatey](https://chocolatey.org/)** com o comando `choco install python`

* **python-magic**
    * Com o **pip** instalado no sistema, rode `pip install python-magic python-magic-bin` ou `pip3 install python-magic python-magic-bin`, dependendo do sistema operacional

* **eyeD3**
    * **Linux**: instalável através do **pip** com o comando `pip install eyed3` ou `pip3 install eyed3`, dependendo da distribuição. Se a sua distro não inclui o **pip** na instalação, você deve instalá-lo antes disso. No **Debian**, por exemplo, o comando é `apt install python3-pip`
    * **Windows**: baixe [esta versão **modificada** da biblioteca](https://github.com/1Deterministic/1D-Sync/raw/master/Dependencies/Windows/eyeD3-0.8.4-windows-modified-to-support-non-english-characters.zip), que suporta arquivos/caminhos com caracteres fora do inglês (como palavras acentuadas), extraia o arquivo **.zip** e, com o console dentro da pasta extraída, rode o comando `python setup.py install`

## Utilização
Edite o arquivo `Config/config.json`, colocando os valores à direita de acordo com suas preferências. **Os valores devem estar entre aspas**:

* `check_cooldown`: valor numérico de espera, em horas, entre as tentativas de sincronização. **Deve ser um valor numérico inteiro maior do que zero** - [opcional, o valor padrão é **1**]

* `startup_delay`: valor numérico de espera, em minutos, do início da execução antes de começar as sincronizações, sendo útil para não sobrecarregar a inicialização do sistema. **Deve ser um valor numérico inteiro maior ou igual a zero** - [opcional, o valor padrão é **0**]

* `save_log`: define se o log será salvo, deve ser **True** ou **False** - [opcional, o valor padrão é **True**]

* `log_only_if_an_error_occur`:  define se o log será gravado apenas quando houver um erro, deve ser **True** ou **False** - [opcional, o valor padrão é **False**]

* `log_only_if_a_sync__occur`:  define se o log será gravado apenas quando alguma sincronia for executada, ignorando as que estão em espera. `log_only_if_an_error_occur` tem preferência sobre essa opção. Deve ser **True** ou **False** - [opcional, o valor padrão é **False**]

* `logs_folder_maximum_size`: tamanho máximo que a pasta `Logs` pode ter. Se for excedido, os arquivos mais antigos serão apagados até que o tamanho máximo seja respeitado. **O critério de exclusão é baseado na data de modificação, deve ser um valor numérico inteiro maior ou igual a zero, 0 significa ilimitado e o valor é lido em MB** - [opcional, o valor padrão é **10**]

* `send_email`: define se o email será enviado, deve ser **True** ou **False** - [opcional, o valor padrão é **False**]

* `email_sender`: endereço de email responsável pelo envio de relatórios de sincronização (somente gmail suportado até o momento, verifique as opções de conta para habilitar o acesso por SMTP) - [obrigatório se `send_email` for **True**, não possui valor padrão]

* `email_sender_password`: senha do email de relatórios, recomendável criar uma conta de email apenas para esta finalidade, uma vez que a senha ficará em texto plano - [obrigatório se `send_email` for **True**, não possui valor padrão]

* `email_addressee`: endereço de email para onde os relatórios são enviados - [obrigatório se `send_email` for **True**, não possui valor padrão]

* `email_only_if_an_error_occur`: define se o email será enviado apenas quando houver um erro em alguma sincronia, deve ser **True** ou **False** - [obrigatório se `send_email` for **True**, não possui valor padrão]

* `post_sync_script`: script a ser executado após a sincronização. Rodará uma vez por loop do programa (ou seja, uma vez a cada período de tempo `check_cooldown`), imediatamente antes da gravação do log e envio do email. Se você está rodando no Windows e deseja utilizar funções do cmd como `dir`, acrescente ao início da linha o comando `powershell`, seguido do comando. Outra possibilidade é criar um arquivo **.bat** e executá-lo diretamente - [opcional, o valor padrão é um comando vazio]

* `run_post_sync_script_only_if_a_sync_occur`: define se o script pós-sincronização rodará apenas quando alguma sincronia for executada, ignorando as que estão em espera. Deve ser **True** ou **False** - [opcional, o valor padrão é False]

* `run_continuously`: define se o programa executará em loop ou se encerrará imediatamente após o fim da sincronização, deve ser **True** ou **False** - [opcional, o valor padrão é True]

Uma boa combinação é utilizar `run_continuously` juntamente com a inicialização do sistema, de forma que o programa esteja sempre em rodando em background. Para fazer isso verifique os passos a seguir, de acordo com seu sistema operacional.

* **Linux**:
    Você pode agendar a sua inicialização utilizando alguma ferramenta própria de sua distribuição ou ambiente gráfico ou ainda agendar a inicialização com o sistema utilizando o crontab. 
    * `crontab -e`
    * adicione a linha `@reboot python /caminho/da/pasta/1dsync.py` ou `@reboot python3 /caminho/da/pasta/1dsync.py`, dependendo da distribuição.

    Não agende sua inicialização para o usuário root, isso pode afetar pastas do sistema caso algum parâmetro de destino esteja errado.

* **Windows**:
    Você pode agendar a sua inicialização criando um arquivo **.bat** na pasta `Inicializar` do seu usuário. Por execmplo, o arquivo `C:\Users\Usuário\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\1dsync.bat` com o seguinte conteúdo:
    `start pythonw C:\caminho\da\pasta\1dsync.py`

O arquivo `Config/control.json` armazena as datas e horários das sincronizações, não é necessário editá-lo. Entretanto, caso queira forçar uma sincronização na próxima tentativa, basta remover a(s) respectivas linhas do arquivo ou trocar sua data agendada.

Utilize o arquivo `Syncs/sync.json.example` como template para criar uma sincronização. Note que o arquivo, para ser considerado, deve possuir a extensão `.json`, então você deve renomeá-lo (recomendável fazer uma cópia desse arquivo e renomear a cópia). **Os valores devem estar entre aspas**:

* `enable`: define se esta sincronização está ativa ou não, deve ser **True** ou **False** - [obrigatório]

* `source_path`: caminho para a pasta de origem. Não pode ser a mesma ou uma subpasta de `destination_path`. No Windows, substitua as barras invertidas `\` do caminho por barras invertidas duplas `\\` ou barras normais `/`, do contrário a sintaxe do arquivo estará incorreta - [obrigatório]

* `source_selection_condition`: condição de seleção de arquivos da pasta de origem, **veja [condições de seleção](#condições-de-seleção)** - [opcional, o valor padrão é **any file**]

* `source_maximum_age`: idade máxima permitida para que os arquivos sejam selecionados na pasta de origem com base na **data de modificação**, deve ser **any age**, o que permite qualquer idade, **ou um valor numérico inteiro maior que zero**, sendo lido em dias - [opcional, o valor padrão é **any age**]

* `source_subfolder_search`: define se serão procurados arquivos nas subpastas da pasta de origem, deve ser **True** ou **False** - [opcional, o valor padrão é **True**]

* `source_filelist_shuffle`: define se a lista de arquivos selecionados da origem será embaralhada, deve ser **True** ou **False** - [opcional, o valor padrão é **False**]

* `destination_path`: caminho para a pasta de destino. Não pode ser a mesma ou uma subpasta de `source_path`. No Windows, substitua as barras invertidas `\` do caminho por barras invertidas duplas `\\` ou barras normais `/`, do contrário a sintaxe do arquivo estará incorreta - [obrigatório]

* `destination_selection_condition`: condição de seleção de arquivos da pasta de destino, **veja [condições de seleção](#condições-de-seleção)** - [opcional, o valor padrão é **any file**]

* `destination_maximum_age`: idade máxima permitida para que os arquivos sejam selecionados na pasta de destino com base na **data de modificação**, deve ser **any age**, o que permite qualquer idade, **ou um valor numérico inteiro maior que zero**, sendo lido em dias - [opcional, o valor padrão é **any age**]

* `destination_subfolder_search`: define se serão procurados arquivos nas subpastas da pasta de destino, deve ser **True** ou **False** - [opcional, o valor padrão é **True**]

* `destination_filelist_shuffle`: define se a lista de arquivos selecionados do destino será embaralhada, deve ser **True** ou **False** - [opcional, o valor padrão é **False**]

* `hierarchy_maintenance`: define se a hierarquia de pastas será mantida na pasta destino, deve ser **True** ou **False** - [opcional, o valor padrão é **True**]

* `left_files_deletion`: define se os arquivos da pasta destino que não estiverem mais na pasta de origem ou não passarem na validação serão removidos, deve ser **True** ou **False** - [opcional, o valor padrão é **False**]

* `file_override`: define se os arquivos serão sobrescritos independetemente de já estarem presentes na pasta destino, deve ser **True** ou **False** - [opcional, o valor padrão é **False**]

* `size_limit`: define o tamanho limite de arquivos na pasta destino, **deve ser um valor numérico inteiro maior ou igual a zero, 0 significa ilimitado e o valor é lido em MB** - [opcional, o valor padrão é **0**]

* `sync_cooldown`: define o intervalo de tempo no qual a sincronização ficará dormente após executar, **deve ser um valor numérico inteiro maior que zero** - [opcional, o valor padrão é **4**]

Para ter mais de uma sincronização basta criar outro arquivo dentro da pasta `Syncs`, atentando para as mesmas regras. Arquivos dentro de pastas também serão lidos, desde que sejam válidos nas mesmas regras.

Os logs serão criados dentro da pasta `Logs`, com o título sendo a data e horário de execução das sincronizações. Não remova essa pasta.

## Condições de seleção
As condições de seleção atualmente disponíveis estão a seguir. Para utilizar mais de uma, separe-as com uma barra vertical (`|`). A barra vertical (`|`) é equivalente à operação lógica **OU**.

As condições de seleção são divididas em 4 tipos: **genérica**, **extensão**, **tipo** e **eyed3**


* **Genérica**
    * `any file`: selecionará **qualquer arquivo**

    * `none`: não selecionará **nenhum arquivo**. **Cuidado ao usar essa funcionalidade, pode quebrar a deleção de arquivos sobrando e a não sobrescrita de arquivos no destino, por exemplo**.

* **Extensão**: seleciona arquivos cuja extensão seja igual à opção recebida. Funciona seguindo o modelo `ext:extensão`, onde `ext:` é o prefixo que ativa esta opção. Por exemplo:
    * `ext:.txt` selecionará arquivos com a extensão `.txt`
    * `ext:.mp3` selecionará arquivos com a extensão `.mp3`

* **Tipo**: seleciona arquivos que pertençam ao tipo definido, independentemente da extensão do arquivo. Funciona seguindo o modelo `type:tipo`, onde `type:` é o prefixo que ativa esta opção. Esta opção é implementada usando **[tipos MIME](https://en.wikipedia.org/wiki/MIME)** e você pode consultar uma lista de tipos possíveis **[aqui](https://www.sitepoint.com/mime-types-complete-list/)**.
Por exemplo:
    * `type:image` selecionará todos os arquivos do tipo imagem
    * `type:audio` selecionará todos os arquivos do tipo audio

* **eyeD3**: seleciona arquivos mp3 com base em informações obtidas através da biblioteca **eyed3**. Funciona seguindo o modelo `eyed3:tag:valor`, onde `eyed3` é o prefixo que ativa esta opção, `tag` é o nome da tag sendo referenciada e `valor` é o valor desejado que a tag `tag` possua. Por exemplo:
    * `eyed3:rating:4` selecionará todos os arquivos mp3 que possuam a na tag rating um valor maior ou igual a 4. Esta é a única opção suportada nesta versão.


## English
### Warning
**Be careful when reading this readme because it differs between versions. Always read the readme file included in the release you downloaded. This particular readme refers to the version 2.4-alpha2**

## Intro
**[1D-Sync](https://github.com/1Deterministic/1D-Sync)** is an automated unidirectional "synchronization" tool. 
With it, it's possible to do file copy operations between folders in specified time intervals, supporting various configurations and some file filters. It was developed as a continuation of 
**[Fantastic-Five-Star-Music-Copier](https://github.com/1Deterministic/Fantastic-Five-Star-Music-Copier)** but it has some extra features **(see [utilization](#utilization))**.

## My use case
I have a domestic file server, a desktop machine and two smartphones wich I sync data. With **[1D-Sync](https://github.com/1Deterministic/1D-Sync)** I made the server copy certain files between these folders automatically. For instance, the 5 star rating musics are always copied to a phone that I use as a media device and for a phone I use as a daily driver. However, as the second one has very little storage space, I set **[1D-Sync](https://github.com/1Deterministic/1D-Sync)** 
to copy random files until certain size (1.5GB) and change them from time to time, in a way that I don't feel the short storage space so much. I also set it to copy images from the camera and WhatsApp to the folder synchronized with my desktop, and so on. To sync the folders between those devices I use **[syncthing](https://syncthing.net/)**, wich I previously recommended.

## Requirements
* **Python 3**
    * **Linux**: probably its already included in your distro. Just double check the correct command that executes the version 3 (in some distros its `python` and in others its `python3`). To verify, run these commands with the **-V** argument and see what version it shows.
    * **Windows**: you can run the installer available in the [official website](https://www.python.org/downloads/) or install using **[Chocolatey](https://chocolatey.org/)** with the command `choco install python`

* **python-magic**
    * With **pip** installed, run `pip install python-magic python-magic-bin` or `pip3 install python-magic python-magic-bin`, depending on your system

* **eyeD3**
    * **Linux**: installable through **pip** with the command `pip install eyed3` or `pip3 install eyed3`, depending on your distro. If your distribution doesn't include **pip** by default, you must install it before that. In **Debian**, for instance, the command is `apt install python3-pip`
    * **Windows**: download [this **modified** version of the library](https://github.com/1Deterministic/1D-Sync/raw/master/Dependencies/Windows/eyeD3-0.8.4-windows-modified-to-support-non-english-characters.zip) that supports files/paths with non english characters, extract the **.zip** file and, with the console in the extracted folder, run the command `python setup.py install`

## Utilization
Edit the file `Config/config.json`, changing the values on the right according to your preferences. **The values must be between quotes**:

* `check_cooldown`: numerical value, in hours, between synchronization attempts. **Must be an integer numerical value greater than zero** - [optional, the default value is **1**]

* `startup_delay`: numerical value, in minutes, to wait before starting the synchronizations, being useful to not overload the system initialization. **Must be an integer numerical value greater than or equal to zero** - [optional, the default value is **0**]

* `save_log`: defines if the log will be saved, must be **True** or **False** - [optional, the default value is **True**]

* `log_only_if_an_error_occur`:  defines if the log will be written only when an error occurred, must be **True** or **False** - [optional, the default value is **False**]

* `log_only_if_a_sync__occur`:  defines if the log will be written only if a sync was executed, ignoring the ones in cooldown. `log_only_if_an_error_occur` has preference over this option. Must be **True** or **False** - [optional, the default value is **False**]

* `logs_folder_maximum_size`: maximum size allowed for the `Logs` folder. If it's exceeded, the older files will be deleted until the maximum size is satisfied. **The exclusion criteria is based on the modified date, must be an integer numerical value greater than or equal to zero, 0 means unlimited and the value is read in MB** - [optional, the default value is **10**]

* `send_email`: defines if the email will be sent, must be **True** or **False** - [optional, the default value is **False**]

* `email_sender`: email address wich will send synchronization reports (only gmail is supported until now, check the account options to enable SMTP access) - [required if `send_email` is **True**, doesn't have a default value]

* `email_sender_password`: report email account password, is recommended to create an account ony for this porpose, since the password will be in plain text - [required if `send_email` is **True**, doesn't have a default value]

* `email_addressee`: email address to where the reports are sent - [required if `send_email` is **True**, doesn't have a default value]

* `email_only_if_an_error_occur`: defines if the email will be sent only when a sync error happens, must be **True** or **False** - [required if `send_email` is **True**, doesn't have a default value]

* `post_sync_script`: script to be executed after the synchronization. It will run once per program loop (once every `check_cooldown` time period), immediately before the log write and sending the email. If you're running on Windows and want to use cmd functions like `dir`, add at the beginning of the line the command `powershell`, followed by the command. Another option is to create a **.bat** file and run it directly - [optional, the default value is an empty command]

* `run_post_sync_script_only_if_a_sync_occur`: defines if the post sync script will run only if a sync was executed, ignoring the ones in cooldown. Must be **True** or **False** - [optional, the default value is False]

* `run_continuously`: defines if the program will run in loop or if it will stop immediately after the synchronization loop, must be **True** or **False** - [optional, the default value is True]

A good combination is to use `run_continuously` together with the system initialization, so the program will be always running in background. To achieve this, check the steps below, according with your operating system:

* **Linux**:
    You can schedule its initialization using some tool of your distribution or desktop environment or use crontab.
    * `crontab -e`
    * add the line `@reboot python /path/to/folder/1dsync.py` ou `@reboot python3 /path/to/folder/1dsync.py`, depending on your distro.

    Don't schedule its initialization to the root user, this can affect system folders if some destination parameter was mistaken.

* **Windows**:
    You can schedule its initialization creating a **.bat** file in the `Startup` folder of your user. For instance, the file `C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\1dsync.bat` with the following content:
    `start pythonw C:\path\to\folder\1dsync.py`

The file `Config/control.json` stores dates and times of the synchronizations, it's not necessary to change it. However, if you want to force a sync to run on the next attempt you can remove the respective line from the file or change it to some chosen date and time.

Use the file `Syncs/sync.json.example` as a template 
to create a synchronization. Note that the file, to be considered, must have the `.json` extension, so you have to rename it (recommended to duplicate this file and rename the copy). **The values must be between quotes**:

* `enable`: sets if this sync will be active or not, must be **True** or **False** - [required]

* `source_path`: path to the source folder. Cannot be the same or a subdirectory of `destination_path`. On Windows, change the inverted slashes `\` from the path to double inverted slashes `\\` or normal slashes `/`, or the syntax will be wrong - [required]

* `source_selection_condition`: selection condition for the files in the source folder, **see [selection conditions](#selection-conditions)** - [optional, the default value is **any file**]

* `source_maximum_age`: maximum allowed age for a file to be selected in the source folder based on the **modified date**, must be **any age**, that allows for any age, **or an integer numerical value greater than zero**, read in days - [optional, the default value is **any age**]

* `source_subfolder_search`: sets if the program will search for files in subfolders of the source folder, must be **True** or **False** - [optional, the default value is **True**]

* `source_filelist_shuffle`: sets if the source file list will be shuffled, must be **True** or **False** - [optional, the default value is **False**]

* `destination_path`: path to the destination folder. Cannot be the same or a subdirectory of `source_path`. On Windows, change the inverted slashes `\` from the path to double inverted slashes `\\` or normal slashes `/`, or the syntax will be wrong - [required]

* `destination_selection_condition`: selection condition for the files in the destination folder, **see [selection conditions](#selection-conditions)** - [optional, the default value is **any file**]

* `destination_maximum_age`: maximum allowed age for a file to be selected in the destination folder based on the **modified date**, must be **any age**, that allows for any age, **or an integer numerical value greater than zero**, read in days - [optional, the default value is **any age**]

* `destination_subfolder_search`: sets if the program will search for files in subfolders of the destination folder, must be **True** or **False** - [optional, the default value is **True**]

* `destination_filelist_shuffle`: sets if the destination file list will be shuffled, must be **True** or **False** - [optional, the default value is **False**]

* `hierarchy_maintenance`: sets if the directory hierarchy will be preserved on the destination folder for the copied files, must be **True** or **False** - [optional, the default value is **True**]

* `left_files_deletion`: sets if the files on the destination folder that are not on the source file list or did not pass the chosen validation will be removed, must be **True** or **False** - [optional, the default value is **False**]

* `file_override`: sets if the files will be overwritten even if they are already on the destination folder, must be **True** or **False** - [optional, the default value is **False**]

* `size_limit`: sets the size limit of the destination folder, **must be an integer numerical value greater than or equal to zero, 0 means unlimited and the value is read in MB** - [optional, the default value is **0**]

* `sync_cooldown`: sets the time interval where the sync will be sleeping after the execution, **must be an integer numerical value greater than zero** - [optional, the default value is **4**]

To have more than one sync you can just create another file inside the `Syncs` folder, paying attention to the same rules. Files inside folders will be used too, provided that they follow the same rules.

The logs will be created inside the `Logs` folder, with the file name being the date and time of the sync execution. Don't remove this folder.

## Selection conditions
The selection conditions currently available are as follows. To use more than one, split them with a vertical slash (`|`). The vertical slash (`|`) is equivalent to the logical operator **OR**.

The selection conditions are divided in 4 types: **generic**, **extension**, **type** and **eyed3**

* **Generic**
    * `any file`: will select **any file**

    * `none`: **will not select any file**. **Be careful when using this function, it may break left files deletion and file override (forcing override even when not asked), for instance**.

* **Extension**: will select files with an extension equal to the option received. Works like the model `ext:extension`, where `ext:` is the prefix that activates this option. For example:
    * `ext:.txt` will select files the the extension `.txt`
    * `ext:.mp3` will select files the the extension `.mp3`

* **Type**: will select files that belong to the defined type, regardless of the file extension. Works like the model `type:filetype`, where `type:` is the prefix that activates this option. This option is implemented using **[MIME types](https://en.wikipedia.org/wiki/MIME)** and you can see a list of possible types **[here](https://www.sitepoint.com/mime-types-complete-list/)**.
For example:
    * `type:image` will select image files
    * `type:audio` will select audio files

* **eyeD3**: will select mp3 files based on information received from the **eyed3** library. Works like the model `eyed3:tag:value`, where `eyed3` is the prefix that activates this option, `tag` is the name of the tag being referenced and `value` is the value that the tag `tag` must have. For instance:
    * `eyed3:rating:4` will select mp3 files with the rating tag greater or equal to 4. This is the only option supported in this version.

## [1Deterministic](https://github.com/1Deterministic), 2018
