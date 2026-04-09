# ==============================================================================
# app.py — Arquivo principal da aplicação Flask (Calculadora de Gorjeta)
# ==============================================================================
# Este arquivo é o "coração" da aplicação. Ele é responsável por:
#   1. Criar a aplicação Flask
#   2. Definir as rotas (URLs) que o usuário pode acessar
#   3. Receber os dados do formulário enviados pelo usuário
#   4. Validar se os dados são válidos (ex: não estão vazios, são números, etc.)
#   5. Realizar os cálculos de gorjeta, total e valor por pessoa
#   6. Classificar o pagador (Mão de vaca, Legal ou Generoso)
#   7. Enviar os resultados para o template HTML que será exibido ao usuário
# ==============================================================================

# --- Importações ---
# Flask: classe principal que cria a aplicação web
# render_template: função que renderiza (processa) arquivos HTML da pasta templates/
# request: objeto que contém os dados enviados pelo navegador (formulário, URL, etc.)
# flash: função que armazena mensagens temporárias para exibir ao usuário (feedback)
# redirect: função que redireciona o usuário para outra página
# url_for: função que gera URLs dinamicamente a partir do nome da função da rota
from flask import Flask, render_template, request, flash, redirect, url_for

# --- Criação da Aplicação ---
# Flask(__name__) cria uma instância da aplicação Flask
# __name__ é uma variável especial do Python que contém o nome do módulo atual
# O Flask usa isso para saber onde encontrar os templates e arquivos estáticos
app = Flask(__name__)

# --- Chave Secreta ---
# A chave secreta é obrigatória para usar flash messages e sessões no Flask
# Ela é usada para assinar (proteger) os cookies de sessão do navegador
# Em produção, deve ser uma string longa, aleatória e mantida em segredo
app.secret_key = 'chave-secreta-calculadora-gorjeta'


# ==============================================================================
# Função auxiliar: classificar_gorjeta
# ==============================================================================
# Esta função recebe o percentual de gorjeta informado pelo usuário
# e retorna uma string com a classificação do pagador.
#
# Regras de classificação:
#   - Abaixo de 5%        → "Mão de vaca" (gorjeta muito baixa)
#   - De 5% até 15%       → "Legal" (gorjeta dentro do padrão)
#   - Acima de 15%        → "Generoso" (gorjeta acima do esperado)
#
# Atenção: 5% e 15% são considerados "Legal" (limites inclusivos)
# ==============================================================================
def classificar_gorjeta(percentual):
    """
    Classifica o pagador conforme o percentual de gorjeta informado.
    
    Parâmetros:
        percentual (float): o percentual de gorjeta (ex: 10.0 para 10%)
    
    Retorna:
        str: a classificação ('Mão de vaca', 'Legal' ou 'Generoso')
    """
    # Se o percentual é menor que 5, o pagador é "Mão de vaca"
    if percentual < 5:
        return 'Mão de vaca'
    # Se o percentual está entre 5 e 15 (inclusive), o pagador é "Legal"
    # O elif (else if) só é verificado se a condição anterior for falsa
    elif percentual <= 15:
        return 'Legal'
    # Se nenhuma das condições anteriores foi verdadeira,
    # significa que o percentual é maior que 15, então é "Generoso"
    else:
        return 'Generoso'


# ==============================================================================
# Rota Principal: "/" (página inicial)
# ==============================================================================
# @app.route() é um "decorador" — ele registra a função abaixo como responsável
# por responder quando o usuário acessar a URL especificada.
#
# methods=['GET', 'POST'] significa que esta rota aceita dois tipos de requisição:
#   - GET: quando o usuário acessa a página digitando a URL ou clicando em um link
#          (apenas exibe o formulário vazio)
#   - POST: quando o usuário clica no botão "Calcular" e envia o formulário
#           (os dados do formulário são enviados para processamento)
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Função da rota principal. Responsável por:
    - Exibir o formulário (GET)
    - Processar os dados do formulário e exibir os resultados (POST)
    """

    # --- Tratamento do método GET ---
    # Se o usuário apenas acessou a página (sem enviar formulário),
    # renderiza o template index.html com o formulário vazio
    if request.method == 'GET':
        return render_template('index.html',
    valor_conta = '',
    quantidade_pessoas = '',
    percentual_gorjeta = '')

    # --- Lista de erros ---
    # Criamos uma lista vazia para acumular todas as mensagens de erro encontradas
    # Se ao final a lista estiver vazia, significa que todos os dados são válidos
    erros = []

    # ===================================================================
    # VALIDAÇÃO DO CAMPO: Valor da conta
    # ===================================================================
    # Primeiro verificamos se o campo foi preenchido (não está vazio)
    if not valor_conta:
        erros.append('O valor da conta é obrigatório.')
    else:
        # O campo foi preenchido, agora tentamos converter para número decimal (float)
        # Usamos try/except para capturar erros caso o usuário digite texto
        try:
            # float() converte a string "150.00" para o número 150.0
            valor_conta_num = float(valor_conta)
            # Verificamos se o valor é positivo (maior que zero)
            if valor_conta_num <= 0:
                erros.append('O valor da conta deve ser maior que zero.')
        except ValueError:
            # Se float() falhar (ex: o usuário digitou "abc"), cai aqui
            erros.append('O valor da conta deve ser um número válido.')

    # ===================================================================
    # VALIDAÇÃO DO CAMPO: Quantidade de pessoas
    # ===================================================================
    if not quantidade_pessoas:
        erros.append('A quantidade de pessoas é obrigatória.')
    else:
        try:
            # int() converte a string "4" para o número inteiro 4
            # Usamos int() em vez de float() porque não faz sentido ter 2.5 pessoas
            quantidade_pessoas_num = int(quantidade_pessoas)
            # Deve haver pelo menos 1 pessoa para dividir a conta
            if quantidade_pessoas_num <= 0:
                erros.append('A quantidade de pessoas deve ser um número inteiro maior que zero.')
        except ValueError:
            # Se int() falhar (ex: "abc" ou "2.5"), cai aqui
            erros.append('A quantidade de pessoas deve ser um número inteiro válido.')

    # ===================================================================
    # VALIDAÇÃO DO CAMPO: Percentual de gorjeta
    # ===================================================================
    if not percentual_gorjeta:
        erros.append('O percentual de gorjeta é obrigatório.')
    else:
        try:
            # float() porque o percentual pode ser decimal (ex: 7.5%)
            percentual_gorjeta_num = float(percentual_gorjeta)
            # Gorjeta pode ser 0% (sem gorjeta), mas não pode ser negativa
            if percentual_gorjeta_num < 0:
                erros.append('O percentual de gorjeta deve ser maior ou igual a zero.')
        except ValueError:
            erros.append('O percentual de gorjeta deve ser um número válido.')

    # ===================================================================
    # VERIFICAÇÃO DE ERROS
    # ===================================================================
    # Se a lista de erros não estiver vazia, significa que há problemas nos dados
    if erros:
        # Percorremos cada mensagem de erro e a adicionamos como flash message
        # O segundo parâmetro 'danger' é a categoria, que o Bootstrap usa
        # para estilizar o alerta com cor vermelha (classe alert-danger)
        for erro in erros:
            flash(erro, 'danger')
        
        # Re-renderizamos o formulário, passando os valores que o usuário
        # já tinha digitado para que ele não precise preencher tudo de novo
        return render_template(
            'index.html',
            valor_conta=valor_conta,               # Preserva o valor digitado
            quantidade_pessoas=quantidade_pessoas,   # Preserva o valor digitado
            percentual_gorjeta=percentual_gorjeta    # Preserva o valor digitado
        )

    # ===================================================================
    # CÁLCULOS — Se chegou aqui, todos os dados são válidos
    # ===================================================================

    # 1. Calcula o valor da gorjeta em reais
    #    Fórmula: valor_conta × (percentual / 100)
    #    Exemplo: 100.00 × (10 / 100) = 100.00 × 0.10 = R$ 10.00
    valor_gorjeta = valor_conta_num * (percentual_gorjeta_num / 100)

    # 2. Calcula o valor total da conta (valor original + gorjeta)
    #    Exemplo: 100.00 + 10.00 = R$ 110.00
    valor_total = valor_conta_num + valor_gorjeta

    # 3. Calcula quanto cada pessoa deve pagar (total ÷ quantidade de pessoas)
    #    Exemplo: 110.00 ÷ 2 = R$ 55.00
    valor_por_pessoa = valor_total / quantidade_pessoas_num

    # 4. Determina a classificação do pagador usando a função auxiliar
    #    Exemplo: 10% → "Legal"
    classificacao = classificar_gorjeta(percentual_gorjeta_num)

    # ===================================================================
    # RENDERIZAÇÃO DA PÁGINA DE RESULTADOS
    # ===================================================================
    # render_template() processa o arquivo resultado.html e substitui
    # as variáveis do Jinja2 ({{ variavel }}) pelos valores calculados
    # Cada parâmetro nomeado (ex: valor_gorjeta=valor_gorjeta) torna a
    # variável disponível dentro do template HTML
    return render_template(
        'resultado.html',                           # Nome do arquivo template
        valor_conta=valor_conta_num,                # Valor original da conta
        quantidade_pessoas=quantidade_pessoas_num,  # Número de pessoas
        percentual_gorjeta=percentual_gorjeta_num,  # Percentual informado
        valor_gorjeta=valor_gorjeta,                # Valor da gorjeta em reais
        valor_total=valor_total,                    # Total (conta + gorjeta)
        valor_por_pessoa=valor_por_pessoa,          # Valor que cada pessoa paga
        classificacao=classificacao                  # Classificação do pagador
    )


# ==============================================================================
# Execução da Aplicação
# ==============================================================================
# Esta condição verifica se o arquivo está sendo executado diretamente
# (python app.py) e não apenas importado por outro módulo.
# Se for executado diretamente, inicia o servidor de desenvolvimento do Flask.
#
# debug=True ativa o modo de depuração, que:
#   - Reinicia o servidor automaticamente quando o código é alterado
#   - Exibe mensagens de erro detalhadas no navegador
#   - NÃO deve ser usado em produção (apenas em desenvolvimento)
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)
