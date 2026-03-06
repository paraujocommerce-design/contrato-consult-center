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

with st.form("form_final"):
    # Organização em Colunas para facilitar o preenchimento
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
    
    # Seção de Serviços e Valores
    st.subheader("📊 Quantitativos e Financeiro")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        q01 = st.number_input("Qtd: Consulta SERASA (Op 01)", min_value=0, step=1)
    with q2:
        q13 = st.number_input("Qtd: Negativação (Op 13)", min_value=0, step=1)
    with q3:
        q05 = st.number_input("Qtd: Localizador (Op 05)", min_value=0, step=1)
    with q4:
        valor = st.text_input("Valor Mensal (R$)", placeholder="00,00")

    st.subheader("➕ Outros Serviços")
    o1, o2 = st.columns(2)
    with o1:
        op_nome = st.text_input("Nome da Opção (Ex: Opção 16 - Veicular)")
    with o2:
        qout = st.number_input("Quantidade (Outros)", min_value=0, step=1)

    st.divider()
    st.subheader("🛡️ Garantia")
    g1, g2, g3 = st.columns(3)
    with g1:
        fiador = st.text_input("Nome do Fiador")
    with g2:
        cpf_fiador = st.text_input("CPF do Fiador (apenas números)")
    with g3:
        resp_pag = st.text_input("Responsável Pagamento")

    # BOTÃO DE AÇÃO
    if st.form_submit_button("VALIDAR E GERAR CONTRATO"):
        erros = []
        if not validar_cnpj(cnpj_input): erros.append("❌ CNPJ inválido.")
        if not validar_cpf(cpf_fiador): erros.append("❌ CPF do Fiador inválido.")
        if not email or "@" not in email: erros.append("❌ Verifique o E-mail.")
        
        if erros:
            for erro in erros: st.error(erro)
        else:
            try:
                # O arquivo deve estar no GitHub com este nome exato
                doc = Document("CONTRATO.docx")
                data_atual = datetime.now().strftime("%d/%m/%Y")
                
                # Mapa de substituição completo
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
                    "{{DATA}}": data_atual
                }

                # Executa a substituição em todas as tabelas (onde estão os campos )
                for tabela in doc.tables:
                    for linha in tabela.rows:
                        for celula in linha.cells:
                            for tag, info in dados.items():
                                if tag in celula.text:
                                    celula.text = celula.text.replace(tag, info)

                output = io.BytesIO()
                doc.save(output)
                
                st.success(f"✅ Sucesso! Contrato de {razao} gerado com data de {data_atual}.")
                st.download_button(
                    label="📥 Baixar Contrato Agora",
                    data=output.getvalue(),
                    file_name=f"Contrato_{razao}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}")
