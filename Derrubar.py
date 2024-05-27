import os
import subprocess
import re

# Obtém o nome do usuário do sistema operacional Windows
ns = os.getenv('USERNAME')

# Comando para obter endereços IP e portas
comando_netstat = 'netstat -ano | find "3389"'

# Função para obter endereços IP e portas
def obter_enderecos_ip_porta(resultado):
    # Utiliza expressão regular para extrair o endereço IP e a porta
    padrao = re.compile(r'(\d+\.\d+\.\d+\.\d+):3389')
    correspondencias = padrao.findall(resultado)
    return correspondencias

# Função para executar comando
def execute_comando(cmd):
    try:
        # Executa o comando no shell e captura a saída
        resultado = subprocess.check_output(cmd, shell=True, text=True)
        return resultado
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return None

# Chama a função com o comando desejado
resultado_netstat = execute_comando(comando_netstat)

# Verifica se o resultado do netstat é válido antes de processar
if resultado_netstat:
    # Obtém o endereço IP e a porta
    enderecos_ip_porta = obter_enderecos_ip_porta(resultado_netstat)

    # Filtra os resultados que não são "0.0.0.0"
    enderecos_diferentes_zero = [endereco for endereco in enderecos_ip_porta if endereco != '0.0.0.0']

    # Verifica se existem endereços diferentes de zero antes de prosseguir
    if enderecos_diferentes_zero:
        # Itera sobre os endereços diferentes de zero
        for endereco in enderecos_diferentes_zero:
            # Comando qwinsta para obter informações do usuário
            comando_qwinsta = f'qwinsta /server:{endereco} | find "{ns}"'
            
            # Chama a função com o comando qwinsta
            resultado_qwinsta = execute_comando(comando_qwinsta)

            # Verifica se o resultado do qwinsta é válido antes de imprimir
            if resultado_qwinsta:
                # Utiliza expressão regular para extrair o número depois do nome do usuário
                numero_usuario = re.search(r'(\d+)\s+Ativo', resultado_qwinsta)
                numero_usuario = numero_usuario.group(1) if numero_usuario else "Número não encontrado."

                # Exibe o resultado
                print(f"Nome do Usuário: {ns}, Endereço IP e Porta: {endereco}, Número do Usuário: {numero_usuario}")

                # Executa o comando rwinsta com os parâmetros
                comando_rwinsta = f'rwinsta /server:{endereco} {numero_usuario}'
                resultado_rwinsta = execute_comando(comando_rwinsta)

                # Verifica se a execução do comando rwinsta foi bem-sucedida
                if resultado_rwinsta:
                    print(f"Resultado do comando rwinsta: {resultado_rwinsta}")
                else:
                    print("Erro ao executar o comando rwinsta.")
            else:
                print(f"Nenhum resultado encontrado para {endereco}")
    else:
        print("Nenhum endereço diferente de 0.0.0.0 encontrado.")