import streamlit as st
from docx import Document
import io
import re
from datetime import datetime

# --- FUNÇÕES DE VALIDAÇÃO ---
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', str(cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    return True

def validar_cnpj(cnpj):
    cnpj = re.sub(r'[^0-9]', '', str(cnpj))
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14: return False
    return True

# --- INTERFACE ---
st.set_page_config(page_title="Consult Center - Emissor", layout="wide")
st.title("📄 Emissor de Contrato - Final")

if 'conteudo_arquivo' not in st.session_state:
    st.session_state.conteudo_arquivo = None

with st.form("form_final"):
    c1, c2, c3 = st.columns(3)
    with c1:
        razao = st.text_input("Razão Social")
        fantasia = st.text_input("Nome Fantasia")
        cnpj_input = st.text_input("CNPJ (apenas números)")
        rep = st.text_input("Representante (Cód + Nome)")
    with c2:
        endereco = st.text_input("Endereço")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        uf = st.text_input("UF (Ex: SP)")
        cep = st.text_input("CEP")
    with c3:
        ddd = st.text_input("DDD", max_chars=2)
        tel = st.text_input("Telefone Fixo")
        cel1 = st.text_input("Celular 01")
        email = st.text_input("E-mail Financeiro")

    st.divider()
    st.subheader("📊 Valores e Quantidades")
    q1, q2, q3, q4 = st.columns(4)
    with q1: q01 = st.number_input("Qtd: Consulta SERASA", min_value=0)
    with q2: q13 = st.number_input("Qtd: Negativação", min_value=0)
    with q3: q05 = st.number_input("Qtd: Localizador", min_value=0)
    with q4: valor_plano = st.text_input("Valor Mensal R$ (Ex: 99,90)")

    st.subheader("➕ Outros")
    o1, o2 = st.columns(2)
    with o1: op_nome = st.text_input("Número da Opção (Ex: 16)")
    with o2: qout = st.number_input("Quantidade Outros", min_value=0)

    st.divider()
    fiador = st.text_input("Nome do Fiador")
    cpf_fiador = st.text_input("CPF do Fiador")
    
    validar = st.form_submit_button("PROCESSAR CONTRATO")

if validar:
    if not validar_cnpj(cnpj_input) or not validar_cpf(cpf_fiador):
        st.error("❌ Verifique CNPJ ou CPF do Fiador.")
    else:
        try:
            doc = Document("CONTRATO.docx")
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            
            dados = {
                "{{RAZAO}}": razao, "{{FANTASIA}}": fantasia, "{{CNPJ}}": cnpj_input,
                "{{REP}}": rep, "{{ENDERECO}}": endereco, "{{BAIRRO}}": bairro,
                "{{CIDADE}}": cidade, "{{UF}}": uf, "{{CEP}}": cep,
                "{{D1}}": ddd, "{{D2}}": ddd, "{{D3}}": ddd,
                "{{TEL}}": tel, "{{CEL1}}": cel1, "{{EMAIL}}": email,
                "{{VALOR}}": valor_plano, "{{FIADOR}}": fiador, "{{CPF_FIADOR}}": cpf_fiador,
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
            st.success(f"✅ Contrato processado com sucesso! Data: {data_hoje}")
        except Exception as e:
            st.error(f"Erro: {e}")

if st.session_state.conteudo_arquivo:
    st.download_button("📥 BAIXAR CONTRATO AGORA", st.session_state.conteudo_arquivo, f"Contrato_{razao}.docx")
