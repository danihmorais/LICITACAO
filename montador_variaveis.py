import config

INSTRUMENTO_TEXTO = {
    "CONTRATO": "Contrato Administrativo",
    "ATA": "Ata de Registro de Preços",
    "SEM_CONTRATO": "Dispensa de Licitação (Pequeno Valor)",
}

MODALIDADE_TEXTO = {
    "PREGAO_ELETRONICO": "Pregão Eletrônico",
    "DISPENSA_EMAIL": "Dispensa Eletrônica por E-mail",
    "DISPENSA_BLL": "Dispensa Eletrônica com Lances (BLL)",
    "PREGAO_PRESENCIAL": "Pregão Presencial",
}

CRITERIOS_TEXTO = {
    "ITEM": "Menor Preço por Item",
    "GLOBAL": "Menor Preço Global",
    "LOTE": "Menor Preço por Lote",
}

CHAVES_RAW = {
    "RAW_EXECUCAO",
    "RAW_MOTIVO_CRITERIO",
    "RAW_MOTIVO_MODALIDADE",
    "INSTRUCOES_EXTRAS",
}

SIM_VALORES = {"sim", "s", "x"}
NAO_VALORES = {"não", "nao", "n", ""}


def _normalizar_sim_nao(valor: str) -> str:
    return str(valor).strip().casefold()


def _converter_para_sim(valor: str) -> bool:
    return _normalizar_sim_nao(valor) in SIM_VALORES


def _formatar_lista_assinaturas(nomes_str: str, cargos_str: str):
    nomes = [nome.strip() for nome in nomes_str.split(",") if nome.strip()]
    cargos = [cargo.strip() for cargo in cargos_str.split(",") if cargo.strip()]
    resultado = []
    for index, nome in enumerate(nomes):
        cargo = cargos[index] if index < len(cargos) else ""
        resultado.append(f"{nome} ({cargo})" if cargo else nome)
    return resultado


def montar_variaveis_fixas(dados_usuario: dict) -> dict:
    resultado = {}

    for chave, valor in dados_usuario.items():
        chave_limpa = chave.strip("{}")
        if chave_limpa in CHAVES_RAW or chave in CHAVES_RAW:
            continue
        resultado[chave] = valor
    
    amostra_opt = dados_usuario.get("{{AMOST}}", "nao")
    if _converter_para_sim(amostra_opt):
        resultado["{{AMOSTRA}}"] = config.TEXTOS.get("amostra_tr", "")
    else:
        resultado["{{AMOSTRA}}"] = ""

    vistoria_opt = dados_usuario.get("{{VIST}}", "nao")
    if _converter_para_sim(vistoria_opt):
        resultado["{{VISTORIA}}"] = config.TEXTOS.get("vistoria_tr", "")
    else:
        resultado["{{VISTORIA}}"] = ""

    instrumento_raw = dados_usuario.get("{{INSTRUMENTO}}", "CONTRATO")
    resultado["{{INSTRUMENTO}}"] = INSTRUMENTO_TEXTO.get(instrumento_raw, instrumento_raw)

    modalidade_raw = dados_usuario.get("{{MODALIDADE}}", "PREGAO_ELETRONICO")
    resultado["{{MODALIDADE}}"] = MODALIDADE_TEXTO.get(modalidade_raw, modalidade_raw)

    criterio_raw = dados_usuario.get("{{CRITERIOS}}", "ITEM")
    resultado["{{CRITERIOS}}"] = CRITERIOS_TEXTO.get(criterio_raw, criterio_raw)

    prorroga = dados_usuario.get("{{PRORROGA}}", "NÃO")
    if _converter_para_sim(prorroga):
        clausula_prorroga = config.TEXTOS.get("clausula_padrao", "")
    else:
        clausula_prorroga = ""
    resultado["{{PRORROGA_CLAUS}}"] = clausula_prorroga

    meepp = dados_usuario.get("{{ME_EPP}}", "NAO")
    if _converter_para_sim(meepp):
        texto_meepp = config.TEXTOS.get("meepp_exclusivo", "")
    else:
        texto_meepp = config.TEXTOS.get("meepp_nao_exclusivo", "")
    resultado["{{ME_EPP_TR}}"] = texto_meepp

    resultado["{{PRORROGA}}"] = "Sim" if _converter_para_sim(prorroga) else "Não"

    resultado["{{ME_EPP}}"] = (
        "Exclusiva para ME/EPP" if _converter_para_sim(meepp)
        else "Não exclusiva para ME/EPP"
    )

    gestores_str = dados_usuario.get("{{GESTOR}}", "")
    cargos_gestores_str = dados_usuario.get("{{GESTOR_CARGO}}", "")
    fiscais_str = dados_usuario.get("{{FISCAL}}", "")
    cargos_fiscais_str = dados_usuario.get("{{FISCAL_CARGO}}", "")

    assinaturas_blocos = []

    if gestores_str and gestores_str != "[Não informado]":
        gestores_formatados = _formatar_lista_assinaturas(gestores_str, cargos_gestores_str)
        nomes_g = [n.strip() for n in gestores_str.split(",") if n.strip()]
        cargos_g = [c.strip() for c in cargos_gestores_str.split(",") if c.strip()]
        for i, nome in enumerate(nomes_g):
            cargo = cargos_g[i] if i < len(cargos_g) else ""
            linha = f"____________________________\n{nome}"
            if cargo:
                linha += f"\n{cargo}\n\n\n"
            assinaturas_blocos.append(linha)

    if fiscais_str and fiscais_str != "[Não informado]":
        nomes_f = [n.strip() for n in fiscais_str.split(",") if n.strip()]
        cargos_f = [c.strip() for c in cargos_fiscais_str.split(",") if c.strip()]
        for i, nome in enumerate(nomes_f):
            cargo = cargos_f[i] if i < len(cargos_f) else ""
            linha = f"____________________________\n{nome}"
            if cargo:
                linha += f"\n{cargo}"
            assinaturas_blocos.append(linha)

    resultado["{{ASSINATURAS}}"] = "\n\n".join(assinaturas_blocos) if assinaturas_blocos else ""
    resultado["{{GESTORES}}"] = (
        "; ".join(_formatar_lista_assinaturas(gestores_str, cargos_gestores_str))
        if gestores_str and gestores_str != "[Não informado]"
        else "[Não informado]"
    )

    return resultado


def filtrar_chaves_docx(dados: dict) -> dict:
    return {k: v for k, v in dados.items() if k.startswith("{{") and k.endswith("}}")}