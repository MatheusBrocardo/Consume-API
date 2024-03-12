
# Automatização do Consumo de Dados de Pessoas Jurídicas: Uma Integração com CNPJA
Este script em Python foi desenvolvido para consumir informações de pessoas jurídicas através da API fornecida pela empresa CNPJA. Ele permite consultar estabelecimentos, contribuintes, informações sobre o Simples Nacional e MEI, e também fornece detalhes sobre os créditos disponíveis.

## Stack utilizada

**Back-end:** Python




## Deploy

Execute o script principal main.py. Ele irá realizar consultas aos estabelecimentos e contribuintes listados em uma fila, armazenados em um banco de dados. Além disso, irá atualizar os detalhes sobre os créditos disponíveis na API da CNPJA.

```bash
  python3 main.py
```


## Limitações e Considerações

O script está sujeito a limitações impostas pela API da CNPJA, incluindo o número de requisições permitidas por minuto e o consumo de créditos.
É necessário ter uma chave de API válida da CNPJA para realizar consultas.
As consultas são feitas de acordo com as configurações de estratégia, idade máxima do cache e limite de dados estabelecidos no script.


## Referência

 - [CNPJA](https://cnpja.com/?gad_source=1&gclid=CjwKCAjw17qvBhBrEiwA1rU9wypULmYElFqwUJ0ZUBS6pa2Y2OMDJwS1MEO3PrVaY6ozyBj9rUV_NhoC32UQAvD_BwE)


