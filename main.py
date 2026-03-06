import streamlit as st
from docx import Document
import io

# Configuração visual
st.set_page_config(page_title="Consult Center - Emissor", layout="wide")
st.title("📄 Gerador de Contratos")

with st.form("dados_contrato"):
    c1, c2 = st.columns(2)
    with c1:
        razao = st.text_input("Razão Social")
        fantasia = st.text_input("Nome Fantasia")
        cnpj = st.text_input("CNPJ")
        rep = st.text_input("Representante (Cód + Nome)")
    with c2:
        ddd = st.text_input("DDD (Ex: 11)", max_chars=2)
        tel = st.text_input("Telefone")
        cel1 = st.text_input("Celular 01")
        valor = st.text_input("Valor do Plano (R$)")

    if st.form_submit_button("Gerar Contrato Agora"):
        # AQUI ESTÁ O SEGREDO: Usando o nome EXATO do arquivo que você subiu
        doc = Document("CONTRATO.docx") 
        
        # Mapeamento das etiquetas que você colocou no Word
        dados = {
            "{{RAZAO}}": razao, "{{FANTASIA}}": fantasia, "{{CNPJ}}": cnpj,
            "{{REP}}": rep, "{{D1}}": ddd, "{{D2}}": ddd, "{{D3}}": ddd,
            "{{TEL}}": tel, "{{CEL1}}": cel1, "{{VALOR}}": valor
        }

        # Preenchimento sem estragar a diagramação
        for tabela in doc.tables:
            for linha in tabela.rows:
                for celula in linha.cells:
                    for tag, info in dados.items():
                        if tag in celula.text:
                            celula.text = celula.text.replace(tag, info)

        output = io.BytesIO()
        doc.save(output)
        st.success("✅ Contrato preenchido com as 2 páginas!")
        st.download_button("📥 Baixar Contrato", output.getvalue(), f"Contrato_{razao}.docx")
