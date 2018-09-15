# 1D-Sync
**[Português](#português)**  
**[English](#english)**  

## Português
**[1D-Sync](https://github.com/1Deterministic/1D-Sync)** é uma ferramenta automatizada de "sincronização" unidirecional. Com ele é possível efetuar cópias de arquivos entre pastas em intervalos específicos de tempo, suportando diversas configurações e alguns filtros de arquivos. Foi desenvolvido como uma continuação do **[Fantastic-Five-Star-Music-Copier](https://github.com/1Deterministic/Fantastic-Five-Star-Music-Copier)** mas possui recursos extras **(veja [utilização](#utilização))**.

## Meu caso de uso
Possuo um servidor de arquivos, um desktop e dois celulares com os quais sincronizo dados. Com o **[1D-Sync](https://github.com/1Deterministic/1D-Sync)**, faço com que o servidor de arquivos copie certos arquivos entre essas pastas automaticamente. Por exemplo, as músicas avaliadas em 5 estrelas são sempre copiadas para um telefone que uso como dispositivo de mídia e também para o telefone que uso no dia-a-dia. Entretanto, como esse segundo possui muito pouco espaço de armazenamento, faço com que o **[1D-Sync](https://github.com/1Deterministic/1D-Sync)** copie arquivos aleatórios até um certo tamanho (1.5GB) e os troque de tempo em tempo, de forma que eu não sinta tanto a falta de espaço. Também copio automaticamente as imagens de câmera e WhatsApp para a pasta sincronizada com meu desktop, entre outros. Para sincronizar essas pastas com os dispositivos eu utilizo o **[syncthing](https://syncthing.net/)**, que já recomendei anteriormente.

## Utilização
O executável irá rodar indefinidamente, por isso é mais apropriado configurá-lo para rodar em background. Você pode agendar a sua inicialização utilizando alguma ferramenta própria de sua distribuição ou ambiente gráfico ou ainda agendar a inicialização com o sistema utilizando o crontab. 

* `crontab -e`
* adicionar a linha `@reboot /caminho/do/executável/1dsync.exe`

Não agende sua inicialização para o usuário root, isso pode afetar pastas do sistema caso algum parâmetro de destino esteja errado.

Lembre-se de dar permissão de execução para o arquivo, o que pode ser feito com
* `chmod +x /caminho/do/executável/1dsync.exe`

Edite o arquivo `Config/config.json`, editando os valores à direita de acordo com suas preferências. **Os valores devem estar entre aspas**:

* `check_cooldown`: valor numérico de espera, em horas, entre as tentativas de sincronização - [obrigatório]

* `save_log`: define se o log será salvo, deve ser **True** ou **False** - [obrigatório]

    * `log_only_if_an_error_occur`:  define se o log será gravado apenas quando houver um erro em alguma sincronia, deve ser **True** ou **False** - [obrigatório se `save_log` for **True**]

* `send_email`: define se o email será enviado, deve ser **True** ou **False** - [obrigatório]

    * `email_sender`: endereço de email responsável pelo envio de relatórios de sincronização (somente gmail suportado até o momento, verifique as opções de conta para habilitar o acesso por SMTP) - [obrigatório se `send_email` for **True**]

    * `email_sender_password`: senha do email de relatórios, recomendável criar uma conta de email apenas para esta finalidade, uma vez que a senha ficará em texto plano - [obrigatório se `send_email` for **True**]

    * `email_addressee`: endereço de email para onde os relatórios são enviados - [obrigatório se `send_email` for **True**]

    * `email_only_if_an_error_occur`: define se o email será enviado apenas quando houver um erro em alguma sincronia, deve ser **True** ou **False** - [obrigatório se `send_email` for **True**]

* `post_sync_script`: script a ser executado após a sincronização. Rodará uma vez por loop do programa (ou seja, uma vez a cada período de tempo `check_cooldown`), imediatamente antes da gravação do log e envio do email - [opcional]

* `logs_folder_maximum_size`: tamanho máximo que a pasta `Logs` pode ter. Se for excedido, os arquivos mais antigos serão apagados até que o tamanho máximo seja respeitado. **O critério de exclusão é baseado na data de modificação, deve ser um valor numérico inteiro maior ou igual a zero, 0 significa ilimitado e o valor é lido em MB** - [opcional]

O arquivo `Config/control.json` armazena as datas e horários das sincronizações, não é necessário editá-lo. Entretanto, caso queira forçar uma sincronização na próxima tentativa, basta remover a(s) respectivas linhas do arquivo ou trocar sua data agendada.

Utilize o arquivo `Syncs/sync.json.example` como template para criar uma sincronização. Note que o arquivo, para ser considerado, deve possuir a extensão `.json`, então você deve renomeá-lo (recomendável fazer uma cópia desse arquivo e renomear a cópia). **Os valores devem estar entre aspas**:

* `enable`: define se esta sincronização está ativa ou não, deve ser **True** ou **False** - [obrigatório]

* `source_path`: caminho para a pasta de origem - [obrigatório]

* `source_selection_condition`: condição de seleção de arquivos da pasta de origem, **veja [validações](#validações)** - [obrigatório]

* `source_maximum_age`: idade máxima permitida para que os arquivos sejam selecionados na pasta de origem com base na **data de modificação**, deve ser **any age**, o que permite qualquer idade, **ou um valor numérico inteiro maior que zero**, sendo lido em dias - [obrigatório]

* `source_subfolder_search`: define se serão procurados arquivos nas subpastas da pasta de origem, deve ser **True** ou **False** - [obrigatório]

* `source_filelist_shuffle`: define se a lista de arquivos selecionados da origem será embaralhada, deve ser **True** ou **False** - [obrigatório]

* `destination_path`: caminho para a pasta de destino - [obrigatório]

* `destination_selection_condition`: condição de seleção de arquivos da pasta de destino, **veja [validações](#validações)** - [obrigatório]

* `destination_maximum_age`: idade máxima permitida para que os arquivos sejam selecionados na pasta de destino com base na **data de modificação**, deve ser **any age**, o que permite qualquer idade, **ou um valor numérico inteiro maior que zero**, sendo lido em dias - [obrigatório]

* `destination_subfolder_search`: define se serão procurados arquivos nas subpastas da pasta de destino, deve ser **True** ou **False** - [obrigatório]

* `destination_filelist_shuffle`: define se a lista de arquivos selecionados do destino será embaralhada, deve ser **True** ou **False** - [obrigatório]

* `hierarchy_maintenance`: define se a hierarquia de pastas será mantida na pasta destino, deve ser **True** ou **False** - [obrigatório]

* `left_files_deletion`: define se os arquivos da pasta destino que não estiverem mais na pasta de origem ou não passarem na validação serão removidos, deve ser **True** ou **False** - [obrigatório]

* `file_override`: define se os arquivos serão sobrescritos independetemente de já estarem presentes na pasta destino, deve ser **True** ou **False** - [obrigatório]

* `size_limit`: define o tamanho limite de arquivos na pasta destino, **deve ser um valor numérico inteiro maior ou igual a zero, 0 significa ilimitado e o valor é lido em MB** - [obrigatório]

* `sync_cooldown`: define o intervalo de tempo no qual a sincronização ficará dormente após executar, **deve ser um valor numérico inteiro maior que zero** - [obrigatório]

Para ter mais de uma sincronização basta criar outro arquivo dentro da pasta `Syncs`, atentando para as mesmas regras. Arquivos dentro de pastas também serão lidos, desde que sejam válidos nas mesmas regras.

Os logs serão criados dentro da pasta `Logs`, com o título sendo a data e horário de execução das sincronizações. Não remova essa pasta.

## Validações
As validações atualmente disponíveis estão a seguir. Para utilizar mais de uma validação, separe-as com um ponto-e-vírgula (`;`). O ponto-e-vírgula (`;`) é equivalente à operação lógica **OU** nas validações.

* `audio`: selecionará arquivos de áudio com as extensões **mp3**, **ogg**, **flac**, **wma**, **wav** ou **opus**

* `favorite audio`: selecionará arquivos de áudio com a extensão **mp3** que possuírem um **rating de 5 estrelas**

* `image`: selecionará arquivos de imagem com as extensões **jpg**, **jpeg**, **png**, **gif** ou **bmp**

* `video`: selecionará arquivos de vídeo com as extensões **mp4**, **mpeg**, **wmv**, **mkv**, **mpg** ou **avi**

* `document`: selecionará documentos com as extensões **docx**, **doc**, **rtf**, **odt**, **ott**, **pdf** ou **txt**

* `sheet`: selecionará planilhas com as extensões     **xslx**, **xls**, **ods**, **ots** ou **csv**

* `presentation`: selecionará apresentações com as extensões **pptx**, **pps**, **odp** ou **otp**

* `any file`: selecionará **qualquer arquivo**

* `none`: não selecionará **nenhum arquivo**. **Cuidado ao usar essa funcionalidade, pode quebrar a deleção de arquivos sobrando e a não sobrescrita de arquivos no destino, por exemplo**.


## English
**[1D-Sync](https://github.com/1Deterministic/1D-Sync)** is an automated unidirectional "synchronization" tool. 
With it, it's possible to do file copy operations between folders in specified time intervals, supporting various configurations and some file filters. It was developed as a continuation of 
**[Fantastic-Five-Star-Music-Copier](https://github.com/1Deterministic/Fantastic-Five-Star-Music-Copier)** but it has some extra features **(see [utilization](#utilization))**.

## My use case
I have a domestic file server, a desktop machine and two smartphones wich I sync data. With **[1D-Sync](https://github.com/1Deterministic/1D-Sync)** I made the server copy certain files between these folders automatically. For instance, the 5 star rating musics are always copied to a phone that I use as a media device and for a phone I use as a daily driver. However, as the second one has very little storage space, I set **[1D-Sync](https://github.com/1Deterministic/1D-Sync)** 
to copy random files until certain size (1.5GB) and change them from time to time, in a way that I don't feel the short storage space so much. I also set it to copy images from the camera and WhatsApp to the folder synchronized with my desktop, and so on. To sync the folders between those devices I use **[syncthing](https://syncthing.net/)**, wich I previously recommended.

## Utilization
The executable will run indefinitely, so it's more apropriate to make it run in background. You can program its initialization using some tool of your distribution or desktop environment or use crontab.

* `crontab -e`
* add the line `@reboot /path/to/executable/1dsync.exe`

Don't program its initialization to the root user, this can affect system folders if some destination parameter was mistaken.

Remember to give execution permission to the file, wich can be done with

* `chmod +x /path/to/executable/1dsync.exe`

Edit the file `Config/config.json`, changing the values on the right according to your preferences. **The values must be between quotes**:

* `check_cooldown`: numerical value, in hours, between synchronization attempts. - [required]

* `save_log`: defines if the log will be saved, must be **True** or **False** - [required]

    * `log_only_if_an_error_occur`:  defines if the log will be written only when a sync error happens, must be **True** or **False** - [required if `save_log` is **True**]

* `send_email`: defines if the email will be sent, must be **True** or **False** - [required]

    * `email_sender`: email address wich will send synchronization reports (only gmail is supported until now, check the account options to enable SMTP access) - [required if `send_email` is **True**]

    * `email_sender_password`: report email account password, is recommended to create an account ony for this porpose, since the password will be in plain text - [required if `send_email` is **True**]

    * `email_addressee`: email address to where the reports are sent - [required if `send_email` is **True**]

    * `email_only_if_an_error_occur`: defines if the email will be sent only when a sync error happens, must be **True** or **False** - [required if `send_email` is **True**]

* `post_sync_script`: script to be executed after the synchronization. It will run once per program loop (once every `check_cooldown` time period), immediately before the log write and sending the email - [optional]

* `logs_folder_maximum_size`: maximum size allowed for the `Logs` folder. If it's exceeded, the older files will be deleted until the maximum size is satisfied. **The exclusion criteria is based on the modified date, must be an integer numerical value greater than or equal to zero, 0 means unlimited and the value is read in MB** - [optional]

The file `Config/control.json` stores dates and times of the synchronizations, it's not necessary to change it. However, if you want to force a sync to run on the next attempt you can remove the respective line from the file or change it to some chosen date and time.

Use the file `Syncs/sync.json.example` as a template 
to create a synchronization. Note that the file, to be considered, must have the `.json` extension, so you have to rename it (recommended to duplicate this file and rename the copy). **The values must be between quotes**:

* `enable`: sets if this sync will be active or not, must be **True** or **False** - [required]

* `source_path`: path to the source folder - [required]

* `source_selection_condition`: selection condition for the files in the source folder, **see [validations](#validations)** - [required]

* `source_maximum_age`: maximum allowed age for a file to be selected in the source folder based on the **modified date**, must be **any age**, that allows for any age, **or an integer numerical value greater than zero**, read in days - [required]

* `source_subfolder_search`: sets if the program will search for files in subfolders of the source folder, must be **True** or **False** - [required]

* `source_filelist_shuffle`: sets if the source file list will be shuffled, must be **True** or **False** - [required]

* `destination_path`: path to the destination folder

* `destination_selection_condition`: selection condition for the files in the destination folder, **see [validations](#validations)** - [required]

* `destination_maximum_age`: maximum allowed age for a file to be selected in the destination folder based on the **modified date**, must be **any age**, that allows for any age, **or an integer numerical value greater than zero**, read in days - [required]

* `destination_subfolder_search`: sets if the program will search for files in subfolders of the destination folder, must be **True** or **False** - [required]

* `destination_filelist_shuffle`: sets if the destination file list will be shuffled, must be **True** or **False** - [required]

* `hierarchy_maintenance`: sets if the directory hierarchy will be preserved on the destination folder for the copied files, must be **True** or **False** - [required]

* `left_files_deletion`: sets if the files on the destination folder that are not on the source file list or did not pass the chosen validation will be removed, must be **True** or **False** - [required]

* `file_override`: sets if the files will be overwritten even if they are already on the destination folder, must be **True** or **False** - [required]

* `size_limit`: sets the size limit of the destination folder, **must be an integer numerical value greater than or equal to zero, 0 means unlimited and the value is read in MB** - [required]

* `sync_cooldown`: sets the time interval where the sync will be sleeping after the execution, **must be an integer numerical value greater than zero** - [required]

To have more than one sync you can just create another file inside the `Syncs` folder, paying attention to the same rules. Files inside folders will be used too, provided that they follow the same rules.

The logs will be created inside the `Logs` folder, with the file name being the date and time of the sync execution. Don't remove this folder.

## Validations
The validations currently available are as follows. To use more than one validation, separate them with a semicolon (`;`). The semicolon (`;`) is equivalent to the logical operator **OR** on the validation.

* `audio`: will select audio files with the extensions **mp3**, **ogg**, **flac**, **wma**, **wav** or **opus**

* `favorite audio`: will select audio files with the **mp3** extension that have a **rating of 5 stars**

* `image`: will select image files with the extensions **jpg**, **jpeg**, **png**, **gif** or **bmp**

* `video`: will select video files with the extensions **mp4**, **mpeg**, **wmv**, **mkv**, **mpg** or **avi**

* `document`: will select document files with the extensions **docx**, **doc**, **rtf**, **odt**, **ott**, **pdf** or **txt**

* `sheet`: will select sheet files with the extensions     **xslx**, **xls**, **ods**, **ots** or **csv**

* `presentation`: will select presentation files with the extensions **pptx**, **pps**, **odp** or **otp**

* `any file`: will select **any file**

* `none`: **will not select any file**. **Be careful when using this function, it may break left files deletion and file override (forcing override even when not asked), for instance**.

## [1Deterministic](https://github.com/1Deterministic), 2018
