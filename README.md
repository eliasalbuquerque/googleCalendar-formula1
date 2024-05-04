# Google Calendar Formula 1

Este projeto é um script Python que sincroniza e otimiza o calendário da 
Fórmula 1 com o Google Calendar. Ele atualiza o nome e a descrição dos eventos 
e configurações de notificações e alarmes. Além disso, remove os eventos de 
dos Treinos livres (*Practice 1, 2 and 3*) das sextas-feiras para diminuir a 
poluição de eventos no calendário do usuário. Utiliza a API do Google Calendar 
para realizar essas operações.


- [Como funciona](#como-funciona)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)



## Como funciona

O script `app.py` se conecta com a API do Google Calendar para editar os 
eventos do calendário da Fórmula 1. 

O calendário da Fórmula 1 é bastante incômodo, pois todos os eventos são 
escritos em letras maiúsculas, vem com todo o nome completo da Fórmula 1, Grand 
Prix, Nome do autódromo, cidade ou país, ano, o tipo do evento 
(*Practice, Sprint, Race*). Além disso, vem com vários links de todas as redes 
sociais da Fórmula 1 na descrição do evento, e por fim, vem com duas 
notificações pré estabelecidas (imagem 1).

Podemos ver que é muito conteúdo para uma simples notificação de evento. Nesse 
caso, minimizei o texto do evento, removi a descrição cheia de links e removi 
as notificações em horários incômodos dos eventos que ocorrem de madrugada 
(imagem 2), ou seja:

Disso:

![imagem 1](image-1.png)

Para isso:

![imagem 2](image-2.png)


## Pré-requisitos

Antes de começar, certifique-se de ter cumprido os seguintes requisitos:

- Você instalou a versão mais recente do **Python**.
- Você instalou a versão mais recente do **pip** (gerenciador de pacotes do Python).
- Você leu a documentação da **API do Google Calendar**.


## Instalação

1. Faça o download do repositório do projeto:
   - https://github.com/eliasalbuquerque/googleCalendar-formula1.git
   - extrair o arquivo no local desejado para o projeto
   - instale as dependências do projeto listadas no arquivo `requirements.txt`
      ```terminal
      pip install -r requirements.txt
      ```

1. No Google Cloud, siga as instruções de configuração e uso do 
   [Python quickstart](https://developers.google.com/calendar/api/quickstart/python)

2. Salve o arquivo `credentials.json` na raíz do projeto

3. No site da [Formula 1](https://www.formula1.com), no menu >**Schedule**, 
   clicar no link **Sync Calendar** e sincronizar com o Google Calendar

4. Abra o Google Calendar e no calendário da Formula 1:
   - abra o menu de opções (3 pontinhos ao lado)
   - copiar o `Calendar ID` em **Integrate calendar**

5. Crie o arquivo `.env` na raíz do projeto e nele escreva: 
   ```txt
   FORMULA1=<cole_o_seu_ID_aqui>
   ```

   Exemplo:
   ```txt
   FORMULA1=c7562a0d52f09...b35fe589bc2e72a3091d4@group.calendar.google.com
   ```

## Uso

1. Abra o terminal na pasta do projeto e rode a aplicação:
   ```terminal
   python app.py
   ```

2. Na primeira vez, o Google irá autenticar a aplicação e irá salvar na raiz do 
   projeto o arquivo `token.json`. Nas próximas vezes não será necessário a 
   permissão de uso da API.

Após o comando o script irá executar:

- renomear o nome dos eventos
- remover descrição
- remover alarmes do período das 23h às 6h
- remover eventos dos treinos livres


## Contribuição

Este é um projeto Python simples que usa a API Google Cloud para usar o Google 
Calendar. Fique à vontade para usar e aplicar em outros serviços do Google, o 
procedimento é basicamente o mesmo.
<!-- 

## Licença

## Contato
 -->