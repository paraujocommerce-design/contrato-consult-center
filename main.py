import streamlit as st
from docx import Document
import io
import re
from datetime import datetime

# --- VALIDAÇÕES ---
def validar_dados(cpf, cnpj):
    # Simplificado para rapidez, aceita qualquer número com 11 ou 14 dígitos
    c = re.sub(r'[^0-9]', '', str(cpf))
    j = re.sub(r'[^0-9]', '', str(cnpj))
    return len(c) == 11, len(j) == 14

st.set_page_config(page_title="Consult Center", layout="wide")
st.title("📄 Emissor de Contrato")

if 'arquivo_pronto' not in st.session_state:
    st.session_state.arquivo_pronto = None

with st.form("form_final"):
    c1, c2, c3 = st.columns(3)
    with c1:
        razao = st.text_input("Razão Social")
        fantasia = st.text_input("Nome Fantasia")
        cnpj = st.text_input("CNPJ (números)")
        rep = st.text_input("Representante")
    with c2:
        end = st.text_input("Endereço")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        uf = st.text_input("UF")
        cep = st.text_input("CEP")
        ref = st.text_input("Ponto de Referência")
    with c3:
        email = st.text_input("E-mail")
        ddd = st.text_input("DDD")
        tel = st.text_input("Telefone")
        cel1 = st.text_input("Celular 01")
        cel2 = st.text_input("Celular 02")

    st.divider()
    v1, v2, v3, v4 = st.columns(4)
    with v1: q01 = st.number_input("Qtd Serasa", min_value=0)
    with v2: q13 = st.number_input("Qtd Negativação", min_value=0)
    with v3: q05 = st.number_input("Qtd Localizador", min_value=0)
    with v4: valor = st.text_input("Valor Mensal R$")

    st.subheader("Outros Serviços")
    o1, o2 = st.columns(2)
    with o1: op_nome = st.text_input("Opção (Número)")
    with o2: qout = st.number_input("Quantidade Outros", min_value=0)

    st.divider()
    f1, f2, f3 = st.columns(3)
    with f1: fiador = st.text_input("Fiador")
    with f2: cpf_f = st.text_input("CPF Fiador")
    with f3: resp_p = st.text_input("Responsável Pagamento")

    gerar = st.form_submit_button("GERAR CONTRATO")

if gerar:
    try:
        doc = Document("CONTRATO.docx")
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        # Mapa de substituição total
        trocas = {
            "{{RAZAO}}": razao, "{{FANTASIA}}": fantasia, "{{CNPJ}}": cnpj,
            "{{REP}}": rep, "{{ENDERECO}}": end, "{{BAIRRO}}": bairro,
            "{{CIDADE}}": cidade, "{{UF}}": uf, "{{CEP}}": cep, "{{REF}}": ref,
            "{{EMAIL}}": email, "{{D1}}": ddd, "{{D2}}": ddd, "{{D3}}": ddd,
            "{{TEL}}": tel, "{{CEL1}}": cel1, "{{CEL2}}": cel2,
            "{{VALOR}}": valor, "{{FIADOR}}": fiador, "{{CPF_FIADOR}}": cpf_f,
            "{{RESP_PAG}}": resp_p, "{{Q01}}": str(q01), "{{Q13}}": str(q13),
            "{{Q05}}": str(q05), "{{OPCAO_NOME}}": op_nome, "{{QOUT}}": str(qout),
            "{{DATA}}": hoje
        }

        for tabela in doc.tables:
            for linha in tabela.rows:
                for celula in linha.cells:
                    for tag, info in trocas.items():
                        if tag in celula.text:
                            celula.text = celula.text.replace(tag, info)

        output = io.BytesIO()
        doc.save(output)
        st.session_state.arquivo_pronto = output.getvalue()
        st.success(f"✅ Contrato de {razao} pronto para baixar!")
    except Exception as e:
        st.error(f"Erro: {e}")

if st.session_state.arquivo_pronto:
    st.download_button("📥 BAIXAR CONTRATO AGORA", st.session_state.arquivo_pronto, f"Contrato_{razao}.docx")
