import streamlit as st
from docx import Document
import io
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Consult Center - Emissor", layout="wide")
st.title("📄 Gerador de Contrato - Consult Center")

with st.form("dados_contrato"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏢 Identificação")
        razao = st.text_input("Razão Social")
        fantasia = st.text_input("Nome Fantasia")
        cnpj = st.text_input("CNPJ")
        rep = st.text_input("Representante (Cód + Nome)")
        id_assoc = st.text_input("Nº Associado")

    with col2:
        st.subheader("📞 Contatos")
        ddd = st.text_input("DDD (Ex: 11)", max_chars=2)
        tel = st.text_input("Telefone Fixo")
        cel1 = st.text_input("Celular 01")
        cel2 = st.text_input("Celular 02")
        email = st.text_input("E-mail Faturas")

    with col3:
        st.subheader("💰 Financeiro")
        valor = st.text_input("Valor do Plano (R$)")
        fiador = st.text_input("Nome do Fiador")
        cpf_fiador = st.text_input("CPF do Fiador")
        resp_pag = st.text_input("Responsável Pagamento")

    if st.form_submit_button("Gerar Contrato Completo"):
        doc = Document("CONTRATO.docx")
        
        # Pega a data de hoje formatada: Ex: 06/03/2026
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        
        # Mapa completo de etiquetas (Tags)
        dados = {
            "{{RAZAO}}": razao,
            "{{FANTASIA}}": fantasia,
            "{{CNPJ}}": cnpj,
            "{{REP}}": rep,
            "{{ID_ASSOC}}": id_assoc,
            "{{D1}}": ddd, "{{D2}}": ddd, "{{D3}}": ddd,
            "{{TEL}}": tel,
            "{{CEL1}}": cel1,
            "{{CEL2}}": cel2,
            "{{VALOR}}": valor,
            "{{FIADOR}}": fiador,
            "{{CPF_FIADOR}}": cpf_fiador,
            "{{RESP_PAG}}": resp_pag,
            "{{EMAIL}}": email,
            "{{DATA}}": data_hoje  # <-- A DATA AGORA ESTÁ AQUI
        }

        # Substituição precisa para manter a 2ª página intacta
        for tabela in doc.tables:
            for linha in tabela.rows:
                for celula in linha.cells:
                    for tag, info in dados.items():
                        if tag in celula.text:
                            celula.text = celula.text.replace(tag, info)

        output = io.BytesIO()
        doc.save(output)
        
        st.success(f"✅ Contrato de {razao} gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Contrato (Word/PDF)",
            data=output.getvalue(),
            file_name=f"Contrato_{razao}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
