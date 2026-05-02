import streamlit as st
from config.database import SessionLocal
from domain.services.transporter_service import TransporterService
from ui.components.data_table import render_table
from ui.components.form_section import section


def render():
    st.title('Transportadoras')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    svc = TransporterService(db)

    with tabs[0]:
        section('Cadastro de Transportadora')
        with st.form('transp_form'):
            razao_social = st.text_input('Razão Social')
            nome_fantasia = st.text_input('Nome Fantasia')
            cnpj = st.text_input('CNPJ')
            responsavel = st.text_input('Responsável')
            telefone = st.text_input('Telefone')
            email = st.text_input('E-mail')
            cidade = st.text_input('Cidade')
            estado = st.text_input('Estado')
            status = st.selectbox('Status', ['ativo', 'inativo'])
            observacoes = st.text_area('Observações')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                payload = {
                    'razao_social': razao_social,
                    'nome_fantasia': nome_fantasia,
                    'cnpj': cnpj,
                    'responsavel': responsavel,
                    'telefone': telefone,
                    'email': email,
                    'cidade': cidade,
                    'estado': estado,
                    'status': status,
                    'observacoes': observacoes,
                }
                try:
                    tr = svc.create_transporter(payload)
                    db.commit()
                    st.success('Transportadora criada com sucesso')
                except Exception as e:
                    st.error(str(e))

    with tabs[1]:
        section('Listagem')
        filters = {}
        col1, col2, col3 = st.columns(3)
        with col1:
            f_razao = st.text_input('Razão Social filtro')
        with col2:
            f_cnpj = st.text_input('CNPJ filtro')
        with col3:
            f_cidade = st.text_input('Cidade filtro')

        search = st.button('Pesquisar')
        if search:
            filters = {}
            if f_razao:
                filters['razao_social'] = f_razao
            if f_cnpj:
                filters['cnpj'] = f_cnpj
            if f_cidade:
                filters['cidade'] = f_cidade
            rows = [t.to_dict() for t in svc.list_transporters(filters)]
            render_table(rows, columns=['id','razao_social','nome_fantasia','cnpj','responsavel','telefone','cidade','estado','status'])
        else:
            rows = [t.to_dict() for t in svc.list_transporters()]
            render_table(rows, columns=['id','razao_social','nome_fantasia','cnpj','responsavel','telefone','cidade','estado','status'])

    with tabs[2]:
        section('Indicadores')
        rows = [t.to_dict() for t in svc.list_transporters()]
        total = len(rows)
        ativos = len([r for r in rows if r.get('status') == 'ativo'])
        st.metric('Total de transportadoras', total)
        st.metric('Ativas', ativos)
