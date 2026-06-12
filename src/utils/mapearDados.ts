export const mapearDadosWizard = (dados: any) => {
  const totalItens = dados.itens.reduce((acc: number, i: any) => acc + (Number(i.qtd) * Number(i.valor || 0)), 0);
  const valorEstimadoFormatado = totalItens.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  
  return {
    "{{OBJETO}}": dados.objeto || "",
    "{{NECESSIDADE}}": dados.necessidade || "",
    "{{ITENS}}": JSON.stringify(dados.itens || []),
    "{{VALOR_ESTIMADO}}": valorEstimadoFormatado,
    "{{EXECUCAO}}": dados.execucao || "",
    "{{PAC}}": dados.pac === "SIM" ? "Previsto no PAC" : `Não previsto: ${dados.motivoPac}`,
    "{{INSTRUMENTO}}": dados.instrumento || "CONTRATO",
    "{{GESTOR}}": dados.gestores?.map((g: any) => g.nome).join(", ") ?? "",
    "{{GESTOR_CARGO}}": dados.gestores?.map((g: any) => g.cargo).join(", ") ?? "",
    "{{FISCAL}}": dados.fiscais?.map((f: any) => f.nome).join(", ") ?? "",
    "{{FISCAL_CARGO}}": dados.fiscais?.map((f: any) => f.cargo).join(", ") ?? "",
    "{{AMOST}}": dados.amostra ? "sim" : "nao",
    "{{VIST}}": dados.vistoria ? "sim" : "nao",
    "{{PRORROGA}}": dados.prorrogar ? "sim" : "nao",
    "{{ME_EPP}}": dados.meepp || "NAO",
    "{{CRITERIOS}}": dados.criterio || "ITEM",
    "{{MOTIVO_CRITERIO}}": dados.motivoCriterio || "",
    "{{MODALIDADE}}": dados.modalidade || "PREGAO_ELETRONICO",
    "{{MOTIVO_MODALIDADE}}": dados.motivoModalidade || "",
    "{{SECRETARIAS}}": dados.secretarias ? dados.secretarias.join(", ") : "",
    "{{VIGENCIA}}": `${dados.vigenciaNum || 1} ${dados.vigenciaUnidade || 'Meses'}`,
    "{{DOTACAO}}": dados.dotacao || "",
    "INSTRUCOES_EXTRAS": dados.instrucoesExtras || "",
    "CAMINHO_IMAGEM_DOTACAO": dados.caminhoImagemDotacao || "",
    "RAW_EXECUCAO": dados.execucao || "",
    "RAW_MOTIVO_CRITERIO": dados.motivoCriterio || "",
    "RAW_MOTIVO_MODALIDADE": dados.motivoModalidade || "",
    "RAW_PAC": dados.pac === "SIM" ? "Previsto no PAC" : `Não previsto: ${dados.motivoPac}`
  };
};