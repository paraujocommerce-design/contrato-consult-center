import streamlit as st
from docx import Document
import io
import re
from datetime import datetime

# --- FUNÇÕES DE VALIDAÇÃO (PRÁTICAS E RÁPIDAS) ---
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
st.set_page_config(page_title="Consult Center - Emissor Seguro", layout="wide")
st.title("📄 Emissor de Contrato com Validação")

with st.form("form_seguro"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🏢 Empresa")
        razao = st.text_input("Razão Social")
        fantasia = st.text_input("Nome Fantasia")
        cnpj_input = st.text_input("CNPJ (apenas números)")
        rep = st.text_input("Representante")
    with c2:
        st.subheader("📞 Contatos")
        email = st.text_input("E-mail Financeiro")
        ddd = st.text_input("DDD", max_chars=2)
        tel = st.text_input("Telefone Fixo")
        cel = st.text_input("Celular 01")
        cep = st.text_input("CEP (apenas números)")
    with c3:
        st.subheader("💰 Plano e Garantia")
        valor = st.text_input("Valor Mensal (R$)")
        fiador = st.text_input("Nome do Fiador")
        cpf_fiador = st.text_input("CPF do Fiador (apenas números)")
        q01 = st.text_input("Qtd Opção 01", "0")

    if st.form_submit_button("VALIDAR E GERAR CONTRATO"):
        erros = []
        
        # Validações Críticas
        if not validar_cnpj(cnpj_input): erros.append("❌ CNPJ da Empresa inválido.")
        if not validar_cpf(cpf_fiador): erros.append("❌ CPF do Fiador inválido.")
        if len(re.sub(r'[^0-9]', '', cep)) != 8: erros.append("❌ CEP deve ter 8 dígitos.")
        if "@" not in email or "." not in email: erros.append("❌ Formato de E-mail inválido.")
        if len(ddd) != 2: erros.append("❌ DDD deve ter 2 dígitos.")

        if erros:
            for erro in erros: st.error(erro)
        else:
            # Se não houver erros, gera o documento
            try:
                doc = Document("CONTRATO.docx")
                data_atual = datetime.now().strftime("%d/%m/%Y")
                
                dados = {
                    "{{RAZAO}}": razao, "{{FANTASIA}}": fantasia, "{{CNPJ}}": cnpj_input,
                    "{{REP}}": rep, "{{D1}}": ddd, "{{TEL}}": tel, "{{CEL1}}": cel, 
                    "{{EMAIL}}": email, "{{VALOR}}": valor, "{{Q01}}": q01, 
                    "{{DATA}}": data_atual, "{{FIADOR}}": fiador, "{{CPF_FIADOR}}": cpf_fiador,
                    "{{CEP}}": cep, "{{D2}}": ddd, "{{D3}}": ddd
                }

                for tabela in doc.tables:
                    for linha in tabela.rows:
                        for celula in linha.cells:
                            for tag, info in dados.items():
                                if tag in celula.text:
                                    celula.text = celula.text.replace(tag, info)

                output = io.BytesIO()
                doc.save(output)
                st.success(f"✅ Dados validados! Contrato de {razao} pronto.")
                st.download_button("📥 Baixar Agora", output.getvalue(), f"Contrato_{razao}.docx")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo CONTRATO.docx: {e}")
