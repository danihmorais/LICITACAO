export const mapearDadosWizard = (dados: any) => {
  const totalItens = dados.itens.reduce((acc: number, i: any) => acc + (Number(i.qtd) * Number(i.valor || 0)), 0);
  
  return {
    "{{OBJETO}}": dados.objeto,
    "{{NECESSIDADE}}": dados.necessidade,
    "{{ITENS}}": JSON.stringify(dados.itens),
    "{{VALOR_ESTIMADO}}": totalItens.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
    "{{EXECUCAO}}": dados.execucao,
    "{{PAC}}": dados.pac === "SIM" ? "Previsto no PAC" : `Não previsto: ${dados.motivoPac}`,
    "{{INSTRUMENTO}}": dados.instrumento,
    "{{GESTOR}}": dados.gestores.join(", "),
    "{{FISCAL}}": dados.fiscais.join(", ")
  };
};