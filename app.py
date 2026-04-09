
from flask import Flask, render_template, request, flash, redirect, url_for


app = Flask(__name__)


app.secret_key = 'chave-secreta-calculadora-gorjeta'

def classificar_gorjeta(percentual):
    """
    Classifica o pagador conforme o percentual de gorjeta informado.
    
    Parâmetros:
        percentual (float): o percentual de gorjeta (ex: 10.0 para 10%)
    
    Retorna:
        str: a classificação ('Mão de vaca', 'Legal' ou 'Generoso')
    """

    if percentual < 5:
        return 'Mão de vaca'

    elif percentual <= 15:
        return 'Legal'

    else:
        return 'Generoso'



@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Função da rota principal. Responsável por:
    - Exibir o formulário (GET)
    - Processar os dados do formulário e exibir os resultados (POST)
    """

    
    if request.method == 'GET':
        return render_template('index.html',
    valor_conta = '',
    quantidade_pessoas = '',
    percentual_gorjeta = '')

    
    erros = []

    
    if not valor_conta:
        erros.append('O valor da conta é obrigatório.')
    else:
       
        try:
            valor_conta_num = float(valor_conta)
            if valor_conta_num <= 0:
                erros.append('O valor da conta deve ser maior que zero.')
        except ValueError:
            erros.append('O valor da conta deve ser um número válido.')

   
 
    if not quantidade_pessoas:
        erros.append('A quantidade de pessoas é obrigatória.')
    else:
        try:
           
            quantidade_pessoas_num = int(quantidade_pessoas)
          
            if quantidade_pessoas_num <= 0:
                erros.append('A quantidade de pessoas deve ser um número inteiro maior que zero.')
        except ValueError:
           
            erros.append('A quantidade de pessoas deve ser um número inteiro válido.')

 
    if not percentual_gorjeta:
        erros.append('O percentual de gorjeta é obrigatório.')
    else:
        try:
           
            percentual_gorjeta_num = float(percentual_gorjeta)
      
            if percentual_gorjeta_num < 0:
                erros.append('O percentual de gorjeta deve ser maior ou igual a zero.')
        except ValueError:
            erros.append('O percentual de gorjeta deve ser um número válido.')

    if erros:
       
        for erro in erros:
            flash(erro, 'danger')
        
      
        return render_template(
            'index.html',
            valor_conta=valor_conta,               
            quantidade_pessoas=quantidade_pessoas,   
            percentual_gorjeta=percentual_gorjeta    
        )


    valor_gorjeta = valor_conta_num * (percentual_gorjeta_num / 100)

    
    valor_total = valor_conta_num + valor_gorjeta


    valor_por_pessoa = valor_total / quantidade_pessoas_num


    classificacao = classificar_gorjeta(percentual_gorjeta_num)


    return render_template(
        'resultado.html',                          
        valor_conta=valor_conta_num,                
        quantidade_pessoas=quantidade_pessoas_num,  
        percentual_gorjeta=percentual_gorjeta_num,
        valor_gorjeta=valor_gorjeta,                
        valor_total=valor_total,                    
        valor_por_pessoa=valor_por_pessoa,         
        classificacao=classificacao                  
    )



    app.run(debug=True)
