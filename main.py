import streamlit as st
from docx import Document
import io

st.set_page_config(page_title="Consult Center - Gerador PDF", layout="wide")

st.title("📄 Gerador de Contrato - Consult Center")
st.info("Preencha os dados abaixo. O PDF gerado conterá as duas páginas do contrato original.")

with st.form("form_contrato"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Localização e Contato")
        razao = st.text_input("Razão Social")
        cnpj = st.text_input("CNPJ")
        endereco = st.text_input("Endereço (Rua/Nº)")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        cep = st.text_input("CEP")
        ponto_ref = st.text_input("Ponto de Referência")
        tel_fixo = st.text_input("Telefone Fixo (com DDD)")
        cel_01 = st.text_input("Celular 01 (com DDD)")
        cel_02 = st.text_input("Celular 02 (com DDD)")

    with col2:
        st.subheader("💰 Financeiro e Garantia")
        email_fat = st.text_input("E-mail para Faturas")
        resp_pagamento = st.text_input("Responsável pelo Pagamento")
        fiador = st.text_input("Nome do Fiador")
        cpf_fiador = st.text_input("CPF do Fiador")
        valor_total = st.text_input("Valor Total do Plano (R$)")
        vencimento = st.selectbox("Vencimento", ["10", "15", "20", "25"])

    st.subheader("📊 Quantitativos (Serasa/Localizador)")
    c3, c4, c5 = st.columns(3)
    with c3:
        q_serasa = st.text_input("Qtd: Consulta SERASA (Op 01)", "0")
    with c4:
        q_negat = st.text_input("Qtd: Negativação (Op 13)", "0")
    with c5:
        q_local = st.text_input("Qtd: Localizador (Op 05)", "0")
    
    st.subheader("➕ Outros Serviços")
    outros_nome = st.text_input("Nome da Opção")
    outros_qtd = st.text_input("Quantidade Outros")

    btn = st.form_submit_button("Gerar Contrato em PDF")

if btn:
    # Carrega o arquivo original (que tem as 2 páginas)
    doc = Document("NOVO.CONTRATO PADRÃO - VERSÃO 02.2026.docx")
    
    # Mapeamento de substituição
    # Nota: O código procura o texto exato que está no Word e substitui mantendo o restante
    mapa = {
        "Razão Social:": f"Razão Social: {razao}",
        "CNPJ:": f"CNPJ: {cnpj}",
        "Endereço:": f"Endereço: {endereco}",
        "Bairro:": f"Bairro: {bairro}",
        "Cidade:": f"Cidade: {cidade}",
        "CEP:": f"CEP: {cep}",
        "Ponto de referência:": f"Ponto de referência: {ponto_ref}",
        "Telefone fixo:": f"Telefone fixo: {tel_fixo}",
        "Celular 01:": f"Celular 01: {cel_01}",
        "Celular 02:": f"Celular 02: {cel_02}",
        "E-mail para recebimento das faturas:": f"E-mail: {email_fat}",
        "Responsável pelos pagamentos:": f"Responsável: {resp_pagamento}",
        "Responsável pela assinatura do contrato (fiador):": f"Fiador: {fiador}",
        "CPF do responsável (fiador):": f"CPF: {cpf_fiador}",
        "R$ _______________": f"R$ {valor_total}",
        "QUANTIDADE: ________, ( OPÇÃO 01)": f"QUANTIDADE: {q_serasa}, ( OPÇÃO 01)",
        "QUANTIDADE: ________, ( OPÇÃO 13)": f"QUANTIDADE: {q_negat}, ( OPÇÃO 13)",
        "QUANTIDADE: ________, ( OPÇÃO 05)": f"QUANTIDADE: {q_local}, ( OPÇÃO 05)",
        "OPÇÃO: ______________": f"OPÇÃO: {outros_nome}",
        "QUANTIDADE: ________": f"QUANTIDADE: {outros_qtd}" # Para o campo "Outros"
    }

    # Substituição em tabelas (onde estão os campos de preenchimento)
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for alvo, novo in mapa.items():
                    if alvo in celula.text:
                        celula.text = celula.text.replace(alvo, novo)

    # Salva o resultado
    target_stream = io.BytesIO()
    doc.save(target_stream)
    
    st.success("✅ Documento processado!")
    
    # IMPORTANTE: Como o Streamlit Cloud não converte PDF nativamente de forma estável,
    # o botão abaixo entrega o Word preenchido com as 2 páginas.
    # Para o PDF imediato, recomendo que o representante use "Salvar como PDF" ao abrir.
    
    st.download_button(
        label="📥 Baixar Contrato Preenchido (2 Páginas)",
        data=target_stream.getvalue(),
        file_name=f"Contrato_{razao}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    st.warning("⚠️ Ao abrir o arquivo, clique em 'Arquivo > Salvar como PDF' para enviar ao cliente. Isso mantém a 2ª página intacta e protegida.")
