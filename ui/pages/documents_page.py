import streamlit as st
import math
from config.database import SessionLocal
from domain.services.document_service import DocumentService
from ui.components.data_table import render_table
from ui.components.query_params import get_query_params
from ui.components.form_section import section
from datetime import date


def render():
    st.title('Documentos')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    dsvc = DocumentService(db)

    # Checar se há query param de edição
    params = get_query_params()
    edit_doc_id = None
    edit_doc_obj = None
    if params.get('edit_document'):
        try:
            edit_doc_id = int(params.get('edit_document')[0])
            edit_doc_obj = dsvc.get_document(edit_doc_id)
        except Exception:
            edit_doc_id = None
            edit_doc_obj = None

    with tabs[0]:
        section('Cadastro de Documento')
        with st.form('document_form'):
            tipo = st.text_input('Tipo de documento', value=edit_doc_obj.tipo_documento if edit_doc_obj else '')
            categoria = st.text_input('Categoria referência', value=edit_doc_obj.categoria_referencia if edit_doc_obj else '')
            referencia_id = st.number_input('ID referência', value=edit_doc_obj.referencia_id or 0 if edit_doc_obj else 0, min_value=0, step=1)
            numero = st.text_input('Número', value=edit_doc_obj.numero if edit_doc_obj else '')
            data_emissao = st.date_input('Data emissão', value=edit_doc_obj.data_emissao if edit_doc_obj and edit_doc_obj.data_emissao else date.today())
            data_vencimento = st.date_input('Data vencimento', value=edit_doc_obj.data_vencimento if edit_doc_obj and edit_doc_obj.data_vencimento else None)
            status = st.selectbox('Status', ['vigente', 'vencido', 'cancelado'], index=0 if (edit_doc_obj and edit_doc_obj.status == 'vigente') else 0)
            observacoes = st.text_area('Observações', value=edit_doc_obj.observacoes if edit_doc_obj else '')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                payload = {
                    'tipo_documento': tipo,
                    'categoria_referencia': categoria or None,
                    'referencia_id': referencia_id if referencia_id and referencia_id > 0 else None,
                    'numero': numero,
                    'data_emissao': data_emissao,
                    'data_vencimento': data_vencimento,
                    'status': status,
                    'observacoes': observacoes,
                }
                try:
                    if edit_doc_obj:
                        dsvc.update_document(edit_doc_obj.id, payload)
                        db.commit()
                        try:
                            st.query_params.clear()
                        except Exception:
                            pass
                        st.success('Documento atualizado')
                        try:
                            st.rerun()
                        except Exception:
                            pass
                    else:
                        dsvc.create_document(payload)
                        db.commit()
                        st.success('Documento registrado')
                except Exception as e:
                    db.rollback()
                    st.error(str(e))

    with tabs[1]:
        section('Listagem de Documentos')
        col1, col2, col3 = st.columns([3, 3, 2])
        with col1:
            f_tipo = st.text_input('Tipo filtro')
        with col2:
            f_numero = st.text_input('Número filtro')
        with col3:
            f_status = st.selectbox('Status filtro', ['Todos', 'vigente', 'vencido', 'cancelado'])

        date_from = st.date_input('Data emissão de', value=None)
        date_to = st.date_input('Data emissão até', value=None)

        if st.button('Pesquisar'):
            filters = {}
            if f_tipo:
                filters['tipo_documento'] = f_tipo
            if f_numero:
                filters['numero'] = f_numero
            if f_status and f_status != 'Todos':
                filters['status'] = f_status
            if date_from:
                filters['date_from'] = date_from
            if date_to:
                filters['date_to'] = date_to
            docs = dsvc.list_documents(filters)
        else:
            docs = dsvc.list_documents()

        # Paginação
        rows_all = [d.to_dict() for d in docs]
        page_size = 10
        page_key = 'page_document'
        if page_key not in st.session_state:
            st.session_state[page_key] = 1
        params = get_query_params()
        if params.get(page_key):
            try:
                st.session_state[page_key] = int(params.get(page_key)[0])
            except Exception:
                pass

        total_pages = max(1, math.ceil(len(rows_all) / page_size))
        if total_pages > 1:
            cols_pag = st.columns(total_pages)
            for i, c in enumerate(cols_pag):
                with c:
                    if st.button(str(i + 1), key=f'page_document_btn_{i+1}'):
                        st.session_state[page_key] = i + 1
                        try:
                            st.rerun()
                        except Exception:
                            pass

        page = max(1, min(st.session_state.get(page_key, 1), total_pages))
        start = (page - 1) * page_size
        paginated = docs[start:start + page_size]

        render_table([d.to_dict() for d in paginated], columns=['id','tipo_documento','categoria_referencia','referencia_id','numero','data_emissao','data_vencimento','status'], entity='document')

        params = get_query_params()
        edit_id = None
        if params.get('edit_document'):
            try:
                edit_id = int(params.get('edit_document')[0])
            except Exception:
                edit_id = None

        # Se vier edit_id, mostrar formulário de edição diretamente abaixo da tabela
        if edit_id is not None:
            sel_id = edit_id
            doc = dsvc.get_document(sel_id)
            if doc:
                st.markdown('### Editar Documento')
                with st.form('edit_doc_form_inline'):
                    e_tipo = st.text_input('Tipo de documento', value=doc.tipo_documento or '')
                    e_categoria = st.text_input('Categoria referência', value=doc.categoria_referencia or '')
                    e_referencia = st.number_input('ID referência', value=doc.referencia_id or 0, min_value=0, step=1)
                    e_numero = st.text_input('Número', value=doc.numero or '')
                    e_data_emissao = st.date_input('Data emissão', value=doc.data_emissao)
                    e_data_vencimento = st.date_input('Data vencimento', value=doc.data_vencimento)
                    e_status = st.selectbox('Status', ['vigente', 'vencido', 'cancelado'], index=0 if doc.status == 'vigente' else (1 if doc.status == 'vencido' else 2))
                    e_obs = st.text_area('Observações', value=doc.observacoes or '')
                    updated = st.form_submit_button('Salvar alterações')
                    if updated:
                        payload = {
                            'tipo_documento': e_tipo,
                            'categoria_referencia': e_categoria or None,
                            'referencia_id': e_referencia if e_referencia and e_referencia > 0 else None,
                            'numero': e_numero,
                            'data_emissao': e_data_emissao,
                            'data_vencimento': e_data_vencimento,
                            'status': e_status,
                            'observacoes': e_obs,
                        }
                        try:
                            dsvc.update_document(sel_id, payload)
                            db.commit()
                            try:
                                st.query_params.clear()
                            except Exception:
                                pass
                            st.success('Documento atualizado')
                            try:
                                st.rerun()
                            except Exception:
                                pass
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))
        else:
            # Campo de edição padrão abaixo da tabela
            options = [f"{d.id} - {d.tipo_documento or '-'} | {d.numero or ''}" for d in docs]
            if options:
                index = 0
                sel = st.selectbox('Selecionar documento para editar', options, index=index, key='sel_document')
                sel_id = int(sel.split(' - ')[0])
                doc = dsvc.get_document(sel_id)
                if doc:
                    st.markdown('### Editar Documento')
                    with st.form('edit_doc_form'):
                        e_tipo = st.text_input('Tipo de documento', value=doc.tipo_documento or '')
                        e_categoria = st.text_input('Categoria referência', value=doc.categoria_referencia or '')
                        e_referencia = st.number_input('ID referência', value=doc.referencia_id or 0, min_value=0, step=1)
                        e_numero = st.text_input('Número', value=doc.numero or '')
                        e_data_emissao = st.date_input('Data emissão', value=doc.data_emissao if doc.data_emissao else date.today())
                        e_data_vencimento = st.date_input('Data vencimento', value=doc.data_vencimento if doc.data_vencimento else None)
                        e_status = st.selectbox('Status', ['vigente', 'vencido', 'cancelado'], index=0 if doc.status == 'vigente' else (1 if doc.status == 'vencido' else 2))
                        e_obs = st.text_area('Observações', value=doc.observacoes or '')
                        updated = st.form_submit_button('Salvar alterações')
                        if updated:
                            payload = {
                                'tipo_documento': e_tipo,
                                'categoria_referencia': e_categoria or None,
                                'referencia_id': e_referencia if e_referencia and e_referencia > 0 else None,
                                'numero': e_numero,
                                'data_emissao': e_data_emissao,
                                'data_vencimento': e_data_vencimento,
                                'status': e_status,
                                'observacoes': e_obs,
                            }
                            try:
                                dsvc.update_document(sel_id, payload)
                                db.commit()
                                st.success('Documento atualizado')
                            except Exception as e:
                                db.rollback()
                                st.error(str(e))

                    if st.button('Remover documento'):
                        try:
                            dsvc.delete_document(sel_id)
                            db.commit()
                            st.success('Documento removido')
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))

    with tabs[2]:
        section('Indicadores')
        docs = dsvc.list_documents()
        total = len(docs)
        vigentes = len([d for d in docs if d.status == 'vigente'])
        st.metric('Total de documentos', total)
        st.metric('Vigentes', vigentes)
