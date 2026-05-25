import json
from providers.openrouter_provider import gerar_texto_openrouter
from providers.gemini_provider import gerar_texto_gemini
from providers.utils import extrair_json

CHAVES_OBRIGATORIAS = [
    "OBJETO",
    "TIPO_OBJ",
    "JUSTIFICATIVA",
    "ESTIMATIVA_QUANTIDADES",
    "RESULTADOS_ESPERADOS",
    "REQUISITOS_ETP",
    "SUBCONTRATACAO_ETP",
    "ME_EPP_ETP",
    "PAC",
    "MERCADO",
    "SOLUCAO",
    "CRITERIOS_JUSTIFICATIVA_ETP",
    "CRITERIOS_SUSTENTABILIDADE",
    "MODALIDADE_JUSTIFICATIVA_ETP",
    "PROVIDENCIAS_CONT",
    "CORRELATAS_INTER",
    "JUSTIFICATIVA_ESTIMATIVA",
    "GARANTIAS_ETP",
    "VISTORIA_ETP",
    "AMOSTRA_ETP",
    "CONCLUSAO",
    "REQUISITOS_TR",
    "OBRIGACOES_CONTRATADA",
    "OBRIGACOES_CONTRANTE",
    "QUALIFICACAO_TECNICA",
    "GARANTIAS_TR",
    "EXECUCAO",
    "PRAZO_EXEC",
    "LOCAL",
    "VALOR_ESTIMADO_APROXIMADO",
    "PARCELAMENTO",
    "AMOSTRA_TR",
]

STAGE_CHAVES = {
    "DFD": [
        "OBJETO",
        "TIPO_OBJ",
        "JUSTIFICATIVA",
        "ESTIMATIVA_QUANTIDADES",
        "RESULTADOS_ESPERADOS",
    ],
    "ETP": [
        "REQUISITOS_ETP",
        "SUBCONTRATACAO_ETP",
        "ME_EPP_ETP",
        "PAC",
        "MERCADO",
        "SOLUCAO",
        "CRITERIOS_JUSTIFICATIVA_ETP",
        "CRITERIOS_SUSTENTABILIDADE",
        "MODALIDADE_JUSTIFICATIVA_ETP",
        "PROVIDENCIAS_CONT",
        "CORRELATAS_INTER",
        "JUSTIFICATIVA_ESTIMATIVA",
        "GARANTIAS_ETP",
        "VISTORIA_ETP",
        "AMOSTRA_ETP",
        "VALOR_ESTIMADO_APROXIMADO",
        "PARCELAMENTO",
        "CONCLUSAO",
    ],
    "TR": [
        "REQUISITOS_TR",
        "OBRIGACOES_CONTRATADA",
        "OBRIGACOES_CONTRANTE",
        "QUALIFICACAO_TECNICA",
        "GARANTIAS_TR",
        "EXECUCAO",
        "PRAZO_EXEC",
        "LOCAL",
        "AMOSTRA_TR",
    ],
}

REGRAS_MINIMAS_TEXTO = {
    "JUSTIFICATIVA": "Mínimo de 4 parágrafos com no mínimo 5 linhas cada, levando em consideração os aspectos legais, técnicos e econômicos, amparados pela CF/1988, sob o prisma do interesse público envolvido.",
    "ESTIMATIVA_QUANTIDADES": "Mínimo de 1 parágrafo com fundamentação técnica e memória metodológica. Como você não sabe os itens, deve sempre tentar dizer que foi considerada a estimativa de quantidades do processo anterior mais recente, ou seja, do processo que tratou do mesmo objeto e que foi concluído mais recentemente. Caso não haja processo anterior, deve justificar a estimativa com base em dados de mercado, histórico de consumo, ou outras fontes confiáveis de informação.",
    "RESULTADOS_ESPERADOS": "Mínimo de 3 parágrafos detalhando economicidade, eficiência, continuidade e interesse público.",
    "REQUISITOS_ETP": "Você deve elaborar requisitos técnicos, objetivos e proporcionais, evitando exigências excessivas de qualificação técnica. Já foi informado que serão solicitaos toda a habilitação jurídica; técnica; fiscal, social e trabalhista; econômico-financeira, e ainda, demais declarações previstas na Lei 14.133/21. Assim, se for o caso, se concentre primeiro em declarações excepcionais que deveriam ser solicitar, e, depois, em documentos adicionais que deveriam ser solicitados, mas que não comprometam a competitividade. Se decidir algum, você deve justificar cada um deles, com pelo menos 1 parágrafo de fundamentação técnica, legal e administrativa para cada requisito adicional sugerido. Se não decidir por nenhum requisito adicional, você deve justificar tecnicamente a ausência de requisitos adicionais, reforçando a adequação dos requisitos previstos na Lei 14.133/21 para o caso concreto. Depois disso, deve considerar os requisitos necessários e suficientes à escolha da solução.",
    "SUBCONTRATACAO_ETP": "Mínimo de 1 parágrafo justificando, mas sempre será que não é permitido.",
    "ME_EPP_ETP": "Mínimo de 3 parágrafos com fundamento na LC 123/2006.",
    "PAC": "Mínimo de 1 parágrafo caso estivesse previsto, caso contrário justificar excepcionalidade da contratação.",
    "MERCADO": "Mínimo de 3 parágrafos comparando soluções e práticas de mercado.",
    "SOLUCAO": "Mínimo de 3 parágrafos. Você deve focar na contratação como um todo, como a modalidade escolhida, o tipo de julgamento adotado, as condições de execução, a necessidade, o objeto, assitência técnica e garantias, e não abordar aspéctos técnicos de itens específicos, que serão abordados posteriormente. O foco deve ser na solução de contratação como um todo, e não em aspectos técnicos de itens específicos.",
    "CRITERIOS_JUSTIFICATIVA_ETP": "Mínimo de 3 parágrafos.",
    "CRITERIOS_SUSTENTABILIDADE": "Mínimo de 3 parágrafos.",
    "MODALIDADE_JUSTIFICATIVA_ETP": "Mínimo de 4 parágrafos com fundamentação legal.",
    "PROVIDENCIAS_CONT": "Mínimo de 2 parágrafo. Fale sobre instrução de fiscais, planejamento de fiscalização, e demais providências relacionadas à fiscalização e controle da execução contratual, bem como à mitigação de riscos relacionados à contratação e diálogo com a autoridade competente (Prefeito) para adoção de providências em caso de necessidade de revisão contratual, aplicação de sanções, ou outras medidas administrativas relacionadas à contratação.",
    "CORRELATAS_INTER": "Mínimo de 1 parágrafo. Quase sempre será não, a não ser que outra instrução tenha sido dada nas instruções extras.",
    "JUSTIFICATIVA_ESTIMATIVA": "Mínimo de 1 parágrafo, em complementação à ESTIMATIVA_QUANTIDADES, que será incluída após a tabela de itens.",
    "GARANTIAS_ETP": "Mínimo de 3 parágrafos, um cada tipo de garantia, devendo abordar tanto a garantia contratual quanto a garantia de proposta, considerando aspectos de proporcionalidade, economicidade e segurança jurídica (devendo ter o viés de nunca pedir essas garantias) e por fim garantia no sentido de assistência técnica, suporte, manutenção, atualização, e demais aspectos relacionados à garantia de solução adequada ao longo da execução contratual, considerando o objeto da contratação.",
    "VISTORIA_ETP": "Mínimo de 1 parágrafo, podendo ser resumido caso se trate de aquisição de bens.",
    "AMOSTRA_ETP": "Mínimo de 1 parágrafo, podendo ser resumido caso se trate de prestação de serviços. Caso se tenha optado por exigir amostra, apenas justifique a exigência, sem detalhar as características técnicas da amostra, que serão abordadas posteriormente no termo de referência.",
    "CONCLUSAO": "Mínimo de 3 parágrafos.",
    "REQUISITOS_TR": "Você deve apenas enumerar cada um dos documentos adicionais solicitados nos REQUISITOS_ETP, separadamente, em ordem crescente, a partir do Documento 13, sempre colocando no formato (Documento XX) Yyyyyyyyyyyyyyyyyyyyy, em que XX é o número do documento adicional sugerido, e Yyyyyyyyyyyyyyyyyyyyy é o nome do documento sugerido. Se não houver nenhum documento adicional sugerido, escreva 'Não há documentos adicionais'.",
    "OBRIGACOES_CONTRATADA": "Mínimo de 15 obrigações separadas por quebra de linha.",
    "OBRIGACOES_CONTRANTE": "Mínimo de 10 obrigações separadas por quebra de linha.",
    "QUALIFICACAO_TECNICA": "Mínimo de 3 parágrafos.",
    "GARANTIAS_TR": "Mínimo de 2 parágrafos. Deve ser um resumo de GARANTIAS_ETP",
    "TIPO_OBJ": (
        "Você deve escolher entre:\n"
        "( ) Serviço não continuado\n"
        "( ) Serviço continuado SEM dedicação exclusiva de mão de obra\n"
        "( ) Serviço continuado COM dedicação exclusiva de mão de obra\n"
        "( ) Material de Consumo\n"
        "( ) Material Permanente/Equipamento\n\n"
        "Reescreva as opções e insira um X na opção escolhida."
    ),
    "PARCELAMENTO": "Mínimo de 1 parágrafo. Você deve analisar a possibilidade de parcelamento da contratação, considerando aspectos como economicidade, eficiência, vantajosidade, planejamento, e jurisprudência do TCU sobre o tema. Considere a opção escolhida e detalhe a forma de parcelamento (parcelamento por item, por lote, ou outro critério), justificando tecnicamente a escolha do critério de parcelamento escolhido. Reforce os aspectos de economicidade, eficiência, vantajosidade e planejamento envolvidos, independente da opção escolhida.",
    "EXECUCAO": "Mínimo de 4 parágrafos. Você deve aprimorar o texto base fornecido, detalhando condições de execução, prazos, cronogramas, etapas, e demais aspectos operacionais relevantes para a execução contratual. Não permita prazos de entrega inexequíveis ou condições de execução genéricas. O texto deve ser completo, detalhado e operacional, garantindo clareza e exequibilidade.",
    "PRAZO_EXEC": "Texto completo contendo prazo por extenso e em algarismos.",
    "VALOR_ESTIMADO_APROXIMADO": "Calcule algum valor aproximado a {{VALOR_ESTIMADO}}, considerando o objeto, a necessidade, as condições de execução, o mercado, a solução adotada e demais aspectos relevantes. O valor deve ser apresentado por extenso e em algarismos, e deve ser justificado com base em dados de mercado, histórico de consumo, ou outras fontes confiáveis de informação. Deve ser informado apenas o R$ XX,XX",
    "LOCAL": "Mínimo de 1 parágrafo completo. Sempre será em algum endereço do Município de São Francisco/SP, mas detalhe o local de entrega ou execução, considerando aspectos logísticos e operacionais relevantes para a contratação. Horário quase sempre das 08h às 11h ou das 13h às 17h, salvo se outro tiver sido informado nas condições de execução.",
    "AMOSTRA_TR": "Mínimo de 4 parágrafos, detalhando a parte prática da exigência de amostra, como a forma de apresentação, as características técnicas a serem observadas, o processo de avaliação da amostra, e demais aspectos operacionais relacionados à exigência de amostra. Caso se trate de prestação de serviços, o texto pode ser mais resumido, mas ainda assim deve detalhar a parte prática da exigência de amostra, como a forma de apresentação, o processo de avaliação da amostra, e demais aspectos operacionais relacionados à exigência de amostra. Deve se basear mais ou menos nisso: Deverão ser entregues amostras de todos os itens pelos licitantes provisoriamente vencedores no prazo máximo de 07 (sete) dias úteis, contadas da data de convocação via e-mail, que serão testadas e avaliadas pela comissão de avaliação definida pelo Departamento de XXXXXXXXX. As amostras postadas por correio ou transportadora não serão aceitas fora do prazo, e, desta maneira, a empresa que necessitar do envio por esses meios, deve ter o cuidado de enviar em tempo hábil, vez que o prazo máximo de entrega é extremamente razoável. Os itens deverão ser entregues em sua embalagem ORIGINAL da marca que for cotada pelo licitante. As amostras deverão ser entregues, junto ao Setor de Licitação na Prefeitura Municipal, no endereço Av. Oscar Antônio da Costa, 1187, CEP 15710-011, São Francisco/SP, qual seja das 8h às 11h e 13h às 17h. A empresa participante que não realizar a entrega das amostras dentro do prazo concedido será desclassificada dos itens que necessitam de apresentação de amostra. Serão exigidos como critério de avaliação aquilo que consta do descritivo de cada item, e avaliados por comissão de avaliação, qual seja: {{fiscal}}, {{fiscal_cargo}}; {{gestor}}, {{gestor_cargo}}.",
}

def processar_dados_ia(dados_usuario, api_key, provider, meepp_exclusivo, etapa):
    prompt = _construir_prompt_por_etapa(
        dados_usuario,
        meepp_exclusivo,
        etapa
    )

    if provider == "openrouter":
        resposta = gerar_texto_openrouter(prompt, api_key)
    elif provider == "gemini":
        resposta = gerar_texto_gemini(prompt, api_key)
    else:
        raise ValueError(f"Provedor IA não suportado: {provider}")

    return extrair_json(resposta)

def _montar_regras_minimas(chaves_etapa):
    regras = []

    for chave in chaves_etapa:
        regra = REGRAS_MINIMAS_TEXTO.get(chave)
        if regra:
            regras.append(f"- {chave}: {regra}")

    return "\n".join(regras)

def _construir_prompt_por_etapa(dados_usuario, meepp_exclusivo, etapa):
    objeto = dados_usuario.get("{{OBJETO}}", "")
    execucao_raw = dados_usuario.get("RAW_EXECUCAO", "")
    instrucoes_extras = dados_usuario.get("INSTRUCOES_EXTRAS", "")
    exclusividade_texto = "Sim" if meepp_exclusivo else "Não"
    necessidade = dados_usuario.get("{{NECESSIDADE}}", "")
    criterio_tipo = dados_usuario.get("{{CRITERIOS}}", "ITEM")
    motivo_criterio_raw = dados_usuario.get("RAW_MOTIVO_CRITERIO", "")
    modalidade_tipo = dados_usuario.get("{{MODALIDADE}}", "PREGAO_ELETRONICO")
    motivo_modalidade_raw = dados_usuario.get("RAW_MOTIVO_MODALIDADE", "")
    pac_raw = dados_usuario.get("RAW_PAC", "")
    instrumento = dados_usuario.get("{{INSTRUMENTO}}", "")
    vigencia = dados_usuario.get("{{VIGENCIA}}", "")
    secretaria = dados_usuario.get("{{SECRETARIA}}", "")
    amostra_opt = dados_usuario.get("{{AMOST}}", "nao")
    vistoria_opt = dados_usuario.get("{{VIST}}", "nao")

    amostra_formatada = "Sim" if amostra_opt.lower() in ["sim", "s", "x"] else "Não"
    vistoria_formatada = "Sim" if vistoria_opt.lower() in ["sim", "s", "x"] else "Não"

    regras_gerais = (
        "Você é um especialista sênior em licitações e contratos administrativos para a Prefeitura de São Francisco - SP.\n"
        "Atue conforme a Lei Federal nº 14.133/2021, jurisprudência consolidada do TCU, "
        "jurisprudência do TCE-SP, doutrina majoritária e boas práticas de governança pública.\n"
        "Os textos devem possuir linguagem técnica, formal, impessoal, jurídica e administrativa.\n"
        "Não gere textos genéricos, superficiais ou resumidos.\n"
        "Os textos devem possuir fundamentação técnica robusta, coerência lógica e profundidade argumentativa.\n"
        "Priorize ampla competitividade, economicidade, eficiência, planejamento, motivação administrativa, "
        "segregação de funções, vantajosidade e segurança jurídica.\n"
        "Observe especialmente:\n"
        "- Lei 14.133/2021;\n"
        "- LC 123/2006;\n"
        "- Súmulas e jurisprudência do TCU;\n"
        "- Jurisprudência do TCE-SP;\n"
        "- Boas práticas de governança e planejamento das contratações públicas.\n"
        "Evite exigências restritivas ou cláusulas potencialmente limitadoras da competitividade.\n"
        "Não utilize markdown.\n"
        "Não utilize listas numeradas salvo quando expressamente necessário.\n"
        "Não explique o JSON.\n"
        "Retorne exclusivamente um objeto JSON válido.\n"
        "Cada chave deve conter apenas o texto correspondente.\n"
        "Nenhum campo pode ser vazio.\n"
        "Não utilize placeholders.\n"
        "Não resuma conteúdos.\n"
        "Os textos devem ser completos, extensos e aprofundados.\n"
    )

    base_prompt = (
        f"OBJETO BASE DA CONTRATAÇÃO: {objeto}\n"
        f"NECESSIDADE ADMINISTRATIVA: {necessidade}\n"
        f"CONDIÇÕES DE EXECUÇÃO INFORMADAS: {execucao_raw}\n"
        f"EXCLUSIVIDADE ME/EPP: {exclusividade_texto}\n"
        f"CRITÉRIO DE JULGAMENTO: {criterio_tipo}\n"
        f"MODALIDADE INFORMADA: {modalidade_tipo}\n"
        f"SITUAÇÃO DO PAC: {pac_raw}\n"
        f"INSTRUMENTO: {instrumento}\n"
        f"VIGÊNCIA: {vigencia}\n"
        f"SECRETARIA/SETOR SOLICITANTE: {secretaria}\n"
        f"EXIGÊNCIA DE AMOSTRA: {amostra_formatada}\n"
        f"EXIGÊNCIA DE VISTORIA: {vistoria_formatada}\n"
    )

    if instrucoes_extras:
        base_prompt += (
            f"\nINSTRUÇÕES COMPLEMENTARES OBRIGATÓRIAS:\n"
            f"{instrucoes_extras}\n"
        )

    if etapa == "DFD":
        chaves = (
            '{\n'
            '  "OBJETO": "",\n'
            '  "TIPO_OBJ": "",\n'
            '  "JUSTIFICATIVA": "",\n'
            '  "ESTIMATIVA_QUANTIDADES": "",\n'
            '  "RESULTADOS_ESPERADOS": ""\n'
            '}'
        )

        diretriz_etapa = (
            "ETAPA: DOCUMENTO DE FORMALIZAÇÃO DE DEMANDA.\n"
            "O OBJETO deve:\n"
            "1 - Se o instrumento for ARP, iniciar obrigatoriamente com "
            "'Registro de preços para futura e eventual aquisição'.\n"
            "2 - Para aquisições comuns sem ARP, iniciar com 'Aquisição'.\n"
            "3 - Para serviços, iniciar com 'Contratação de empresa especializada'.\n"
            "4 - Informar obrigatoriamente o Município de São Francisco/SP.\n"
            "5 - Informar vigência.\n"
            "6 - Informar secretaria/setor destinatário.\n"
            "7 - Caso existam diversos setores, utilizar a expressão 'diversos setores da Administração Municipal'.\n"
            "8 - Caso haja convênio, recurso vinculado ou programa governamental, mencionar expressamente.\n"
            "A JUSTIFICATIVA deve conter motivação administrativa detalhada, demonstração do interesse público, "
            "necessidade institucional, impactos da não contratação, alinhamento ao planejamento e continuidade administrativa.\n"
        )

    elif etapa == "ETP":
        chaves = (
            '{\n'
            '  "REQUISITOS_ETP": "",\n'
            '  "SUBCONTRATACAO_ETP": "",\n'
            '  "ME_EPP_ETP": "",\n'
            '  "PAC": "",\n'
            '  "MERCADO": "",\n'
            '  "SOLUCAO": "",\n'
            '  "CRITERIOS_JUSTIFICATIVA_ETP": "",\n'
            '  "CRITERIOS_SUSTENTABILIDADE": "",\n'
            '  "MODALIDADE_JUSTIFICATIVA_ETP": "",\n'
            '  "PROVIDENCIAS_CONT": "",\n'
            '  "CORRELATAS_INTER": "",\n'
            '  "JUSTIFICATIVA_ESTIMATIVA": "",\n'
            '  "GARANTIAS_ETP": "",\n'
            '  "VISTORIA_ETP": "",\n'
            '  "AMOSTRA_ETP": "",\n'
            '  "CONCLUSAO": ""\n'
            '}'
        )

        if criterio_tipo == "ITEM":
            diretriz_criterio = (
                "Na justificativa de parcelamento, priorize adjudicação por item "
                "como regra geral para ampliar competitividade, conforme jurisprudência do TCU."
            )
        else:
            diretriz_criterio = (
                f"Utilize como motivação técnica do agrupamento/lote: {motivo_criterio_raw}"
            )

        if modalidade_tipo == "PREGAO_ELETRONICO":
            diretriz_modalidade = (
                "Justifique a adoção do Pregão Eletrônico como modalidade preferencial "
                "para bens e serviços comuns, priorizando competitividade e transparência."
            )
        elif modalidade_tipo in ["DISPENSA_EMAIL", "DISPENSA_BLL"]:
            diretriz_modalidade = (
                f"Justifique tecnicamente a contratação direta utilizando como base: {motivo_modalidade_raw}"
            )
        elif modalidade_tipo == "PREGAO_PRESENCIAL":
            diretriz_modalidade = (
                f"Justifique a excepcionalidade do pregão presencial utilizando como base: {motivo_modalidade_raw}"
            )
        else:
            diretriz_modalidade = ""

        diretriz_etapa = (
            "ETAPA: ESTUDO TÉCNICO PRELIMINAR.\n"
            "Todos os textos devem possuir análise técnica aprofundada.\n"
            "Utilize fundamentos legais, técnicos e administrativos.\n"
            "Demonstre motivação adequada dos atos administrativos.\n"
            "Observe economicidade, eficiência, vantajosidade e planejamento.\n"
            "Para ME/EPP, observar LC 123/2006 e jurisprudência aplicável.\n"
            "Para PAC, se não houver previsão, justificar excepcionalidade da contratação.\n"
            "Para sustentabilidade, abordar impactos ambientais, logística reversa, descarte, durabilidade, eficiência e sustentabilidade econômica.\n"
            "Se a EXIGÊNCIA DE AMOSTRA for 'Não', o campo AMOSTRA_ETP deve retornar expressamente 'Não há necessidade de exigência de amostra para esta contratação, justificando tecnicamente a desnecessidade e ausência de risco relevante.'\n"
            "Se a EXIGÊNCIA DE VISTORIA for 'Não', o campo VISTORIA_ETP deve retornar expressamente 'Não há necessidade de exigência de vistoria prévia para esta contratação, justificando tecnicamente a desnecessidade.'\n"
            f"{diretriz_criterio}\n"
            f"{diretriz_modalidade}"
        )

    elif etapa == "TR":
        chaves = (
            '{\n'
            '  "REQUISITOS_TR": "",\n'
            '  "OBRIGACOES_CONTRATADA": "",\n'
            '  "OBRIGACOES_CONTRANTE": "",\n'
            '  "QUALIFICACAO_TECNICA": "",\n'
            '  "GARANTIAS_TR": "",\n'
            '  "EXECUCAO": "",\n'
            '  "PRAZO_EXEC": "",\n'
            '  "LOCAL": "",\n'
            '  "AMOSTRA_TR": ""\n'
            '}'
        )

        diretriz_execucao = (
            f"O campo EXECUCAO deve obrigatoriamente aprimorar o seguinte texto base: {execucao_raw}"
            if execucao_raw and execucao_raw != "[Condições de execução não informadas]"
            else "Elabore condições completas de execução compatíveis com o objeto."
        )

        diretriz_etapa = (
            "ETAPA: TERMO DE REFERÊNCIA.\n"
            "Os textos devem possuir caráter normativo e operacional.\n"
            "Os requisitos devem ser objetivos, proporcionais e compatíveis com o objeto.\n"
            "É vedada exigência excessiva de qualificação técnica.\n"
            "Para aquisições comuns, evitar exigência de atestado de capacidade técnica sem justificativa robusta.\n"
            "Observe jurisprudência do TCE-SP, especialmente TC-017136.989.25-8.\n"
            "As obrigações devem ser claras, fiscalizáveis e compatíveis com execução contratual.\n"
            "Se a EXIGÊNCIA DE AMOSTRA for 'Não', o campo AMOSTRA_TR deve retornar expressamente 'Não há exigência de amostra para esta contratação.'\n"
            f"{diretriz_execucao}"
        )

    else:
        chaves = "{}"
        diretriz_etapa = ""

    regras_minimas = _montar_regras_minimas(
        STAGE_CHAVES.get(etapa, [])
    )

    return (
        f"{regras_gerais}\n\n"
        f"{base_prompt}\n\n"
        f"{diretriz_etapa}\n\n"
        f"REGRAS MÍNIMAS OBRIGATÓRIAS DE TAMANHO E PROFUNDIDADE:\n"
        f"{regras_minimas}\n\n"
        f"ESTRUTURA JSON OBRIGATÓRIA:\n"
        f"{chaves}\n\n"
        f"RETORNE APENAS O JSON VÁLIDO."
    )

construir_prompt = _construir_prompt_por_etapa
