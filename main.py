import streamlit as st
from docx import Document
import io
import re
from datetime import datetime

# --- FUNÇÕES DE VALIDAÇÃO ---
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', str(cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]): return False
    return True

def validar_cnpj(cnpj):
    cnpj = re.sub(r'[^0-9]', '', str(cnpj))
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14: return False
    tamanho = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12, 14):
        soma = sum(int(cnpj[num]) * tamanho[len(tamanho)-i+num] for num in range(i))
        digito = 11 - (soma % 11)
        if digito >= 10: digito = 0
        if digito != int(cnpj[i]): return False
    return True

# --- INTERFACE ---
st.set_page_config(page_title="Consult Center - Sistema Oficial", layout="wide")
st.title("📄 Emissor de Contrato Profissional")

# Inicializa o estado para o download
if 'conteudo_arquivo' not in st.session_state:
    st.session_state.conteudo_arquivo = None
    st.session_state.nome_cliente = ""

with st.form("form_final"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🏢 Identificação")
        razao = st.text_input("Razão Social")
        fantasia = st.text_input("Nome Fantasia")
        cnpj_input = st.text_input("CNPJ (apenas números)")
        rep = st.text_input("Representante (Cód + Nome)")
        id_assoc = st.text_input("Nº Associado")
    with c2:
        st.subheader("📍 Localização")
        endereco = st.text_input("Endereço")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        cep = st.text_input("CEP")
        ref = st.text_input("Ponto de Referência")
    with c3:
        st.subheader("📞 Contatos")
        email = st.text_input("E-mail Financeiro")
        ddd = st.text_input("DDD", max_chars=2)
        tel = st.text_input("Telefone Fixo")
        cel1 = st.text_input("Celular 01")
        cel2 = st.text_input("Celular 02")

    st.divider()
    st.subheader("📊 Quantitativos e Financeiro")
    q1, q2, q3, q4 = st.columns(4)
    with q1: q01 = st.number_input("Qtd: Consulta SERASA (Op 01)", min_value=0, step=1)
    with q2: q13 = st.number_input("Qtd: Negativação (Op 13)", min_value=0, step=1)
    with q3: q05 = st.number_input("Qtd: Localizador (Op 05)", min_value=0, step=1)
    with q4: valor = st.text_input("Valor Mensal (R$)", value="0,00")

    st.subheader("➕ Outros Serviços")
    o1, o2 = st.columns(2)
    with o1: op_nome = st.text_input("Nome da Opção (Ex: Opção 16)")
    with o2: qout = st.number_input("Quantidade (Outros)", min_value=0, step=1)

    st.divider()
    st.subheader("🛡️ Garantia")
    g1, g2, g3 = st.columns(3)
    with g1: fiador = st.text_input("Nome do Fiador")
    with g2: cpf_fiador = st.text_input("CPF do Fiador (apenas números)")
    with g3: resp_pag = st.text_input("Responsável Pagamento")

    validar = st.form_submit_button("PROCESSAR CONTRATO")

# Lógica fora do formulário para evitar o erro
if validar:
    erros = []
    if not validar_cnpj(cnpj_input): erros.append("❌ CNPJ inválido.")
    if not validar_cpf(cpf_fiador): erros.append("❌ CPF do Fiador inválido.")
    
    if erros:
        for erro in erros: st.error(erro)
    else:
        try:
            doc = Document("CONTRATO.docx")
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            
            dados = {
                "{{RAZAO}}": razao, "{{FANTASIA}}": fantasia, "{{CNPJ}}": cnpj_input,
                "{{REP}}": rep, "{{ID_ASSOC}}": id_assoc, "{{ENDERECO}}": endereco,
                "{{BAIRRO}}": bairro, "{{CIDADE}}": cidade, "{{CEP}}": cep, "{{REF}}": ref,
                "{{EMAIL}}": email, "{{D1}}": ddd, "{{D2}}": ddd, "{{D3}}": ddd,
                "{{TEL}}": tel, "{{CEL1}}": cel1, "{{CEL2}}": cel2,
                "{{VALOR}}": valor, "{{FIADOR}}": fiador, "{{CPF_FIADOR}}": cpf_fiador,
                "{{RESP_PAG}}": resp_pag, 
                "{{Q01}}": str(q01), "{{Q13}}": str(q13), "{{Q05}}": str(q05),
                "{{OPCAO_NOME}}": op_nome, "{{QOUT}}": str(qout),
                "{{DATA}}": data_hoje
            }

            for tabela in doc.tables:
                for linha in tabela.rows:
                    for celula in linha.cells:
                        for tag, info in dados.items():
                            if tag in celula.text:
                                celula.text = celula.text.replace(tag, info)

            output = io.BytesIO()
            doc.save(output)
            st.session_state.conteudo_arquivo = output.getvalue()
            st.session_state.nome_cliente = razao
            st.success(f"✅ Sucesso! Contrato de {razao} processado com data de {data_hoje}.")
            
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")

# O botão de download aparece aqui, fora do formulário
if st.session_state.conteudo_arquivo:
    st.download_button(
        label="📥 BAIXAR CONTRATO AGORA",
        data=st.session_state.conteudo_arquivo,
        file_name=f"Contrato_{st.session_state.nome_cliente}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
