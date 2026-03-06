import streamlit as st
from docx import Document
import io

st.set_page_config(page_title="Consult Center - Gerador")
st.title("📄 Emissor de Contratos")

with st.form("formulario_contrato"):
    st.subheader("Dados do Contratante")
    razao = st.text_input("Razão Social")
    cnpj = st.text_input("CNPJ")
    endereco = st.text_input("Endereço")
    cidade = st.text_input("Cidade")
    email_fatura = st.text_input("E-mail para faturas")
    
    st.subheader("Plano e Valores")
    plano_nome = st.text_input("Nome do Plano (Ex: OPÇÃO 01)")
    valor_mensal = st.text_input("Valor Mensal (R$)")
    
    st.subheader("Responsável / Fiador")
    fiador = st.text_input("Nome do Fiador")
    cpf_fiador = st.text_input("CPF do Fiador")
    
    btn_gerar = st.form_submit_button("Gerar Contrato")

if btn_gerar:
    # Nome exato do arquivo que você subiu
    doc = Document("NOVO.CONTRATO PADRÃO - VERSÃO 02.2026.docx")
    
    # Dicionário de trocas baseado no seu texto original
    trocas = {
        "Razão Social:": f"Razão Social: {razao}",
        "CNPJ:": f"CNPJ: {cnpj}",
        "Endereço:": f"Endereço: {endereco}",
        "Cidade:": f"Cidade: {cidade}",
        "E-mail para recebimento das faturas:": f"E-mail: {email_fatura}",
        "PLANO MENSAL CONTRATADO:": f"PLANO: {plano_nome}",
        "R$ _______________": f"R$ {valor_mensal}",
        "Responsável pela assinatura do contrato (fiador):": f"Fiador: {fiador}",
        "CPF do responsável (fiador):": f"CPF: {cpf_fiador}"
    }

    # Procura e substitui nas tabelas (onde estão os campos vazios) 
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for alvo, novo_texto in trocas.items():
                    if alvo in celula.text:
                        celula.text = celula.text.replace(alvo, novo_texto)

    # Prepara o download
    buffer = io.BytesIO()
    doc.save(buffer)
    st.success("Tudo pronto!")
    st.download_button(label="📥 Baixar Contrato", 
                       data=buffer.getvalue(), 
                       file_name=f"Contrato_{razao}.docx")
