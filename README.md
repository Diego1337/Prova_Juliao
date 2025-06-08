Pré-requisitos

Antes de começar, certifique-se de que possui:
Uma instância EC2 Ubuntu configurada. 
Acesso SSH à instância com uma chave privada válida .pem 

1. Conectar à Instância EC2
Abra o PowerShell (Windows) ou o terminal (Linux/Mac).
Conecte-se via SSH à sua instância EC2:

ssh -i "C:\Users\usuario\Desktop\Prova_Juliao\suachave.pem" ubuntu@<SEU_IP_PUBLICO>
ssh -i "suachave.pem" root@ec2-00-000-000-000.compute-1.amazonaws.com

2. Atualizar o Sistema
Após conectar-se à instância, atualize os pacotes do sistema:

sudo apt update 
sudo apt upgrade 

3. Instalar Dependências
Instale as principais ferramentas necessárias:

sudo apt install mysql-server -y
sudo apt install git -y
sudo apt install python3.13 python3.13-venv python3.13-pip -y
pip install streamlit pandas plotly

4. Clonar o Repositório do Projeto
Baixe o código diretamente do GitHub:

cd ~
git clone https://github.com/Diego1337/Prova_Juliao.git
cd Prova_Juliao

Se já houver uma pasta existente, remova-a antes do clone:
rm -rf Prova_Juliao

5. Criar e Ativar um Ambiente Virtual
Para evitar conflitos, use um ambiente virtual para instalar as dependências

python3 -m venv myenv
source myenv/bin/activate

Se estiver no Windows (PowerShell):
powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1

6. Instalar as Dependências do Projeto
Recomendado atualizar o pip e reinstalar as bibliotecas para evitar erros

pip install --upgrade pip
pip install streamlit pandas plotly

7. Configurar Grupo de Segurança na EC2 (Porta 8501)
Antes de rodar o Streamlit, é necessário liberar a porta 8501 para acesso externo.

Acesse o Console da AWS e vá para EC2.
No menu esquerdo, clique em Grupos de segurança.
Encontre o grupo de segurança da sua instância EC2 e clique nele.
Vá até a aba Regras de entrada e clique em Editar.
Adicione uma nova regra com os seguintes parâmetros:
Tipo: TCP personalizado
Porta: 8501
Origem: Qualquer IPv4 (0.0.0.0/0)
Salve as alterações.

8. Executar a Aplicação
Rodando a aplicação Streamlit:

streamlit run main.py
Caso deseje manter a aplicação rodando mesmo após fechar o terminal:

9. Acessar a Aplicação no Navegador
Configurar regras de segurança no EC2: Libere a porta 8501 para acesso externo.

10.Acesse o Streamlit via navegador:

http://<SEU_IP_PUBLICO>:8501

#EXTRA
Comandos Rápidos para Referência

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install git -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-pip -y

# Clonar repositório
cd ~
git clone https://github.com/Diego1337/Prova_Juliao.git
cd Prova_Juliao

# Criar ambiente virtual
python3.13 -m venv myenv
source myenv/bin/activate

# Instalar bibliotecas
pip install --upgrade pip
pip install streamlit pandas plotly

# Configurar segurança na EC2 (porta 8501)
# Vá até AWS -> EC2 -> Grupo de Segurança -> Adicione regra de entrada
# Tipo: TCP personalizado | Porta: 8501 | Origem: Qualquer IPv4 (0.0.0.0/0)

# Executar aplicação
streamlit run main.py
