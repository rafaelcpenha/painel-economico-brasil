// =====================================================
// Painel Econômico Brasil — script principal
// Sub-fase 2.3: gerar cards a partir do dados.json
// =====================================================

// -----------------------------------------------------
// 1. Funções utilitárias de apresentação
// -----------------------------------------------------

/**
 * Formata um número no padrão brasileiro.
 * Ex.: 10.75 → "10,75" | -0.45 → "−0,45"
 */
function formatarNumero(valor) {
    const formatado = Math.abs(valor).toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
    // Usa o sinal de menos tipográfico (−, U+2212) para negativos
    return valor < 0 ? "−" + formatado : formatado;
}

/**
 * Retorna o símbolo da seta conforme a direção da variação.
 * direcao: "alta" → ▲ | "baixa" → ▼
 */
function setaDaVariacao(direcao) {
    if (direcao === "alta") return "▲";
    if (direcao === "baixa") return "▼";
    return "—"; // neutro
}

/**
 * Retorna a classe CSS da variação com base na polaridade do indicador
 * e na direção do movimento.
 *
 * - Se polaridade e direção "concordam" (positiva+alta ou negativa+baixa),
 *   o movimento é BOM → verde.
 * - Se "discordam" (positiva+baixa ou negativa+alta), é RUIM → vermelho.
 * - Se direção é "neutro", é NEUTRO → cinza.
 *
 * polaridade: "positiva" | "negativa"
 * direcao: "alta" | "baixa" | "neutro"
 */
function classeVariacao(polaridade, direcao) {
    if (direcao === "neutro") return "card-variacao-neutro";

    // Fallback: se não houver polaridade definida, assume o comportamento antigo
    // (alta = vermelho, baixa = verde), que era o padrão anterior.
    if (!polaridade) {
        return direcao === "alta" ? "card-variacao-ruim" : "card-variacao-boa";
    }

    const concorda =
        (polaridade === "positiva" && direcao === "alta") ||
        (polaridade === "negativa" && direcao === "baixa");

    return concorda ? "card-variacao-boa" : "card-variacao-ruim";
}

/**
 * Constrói o HTML de um card a partir de um objeto indicador.
 * Retorna uma string de HTML.
 */
function montarCardHTML(indicador) {
    const valorFormatado = formatarNumero(indicador.valor);
    const seta = setaDaVariacao(indicador.variacao.direcao);
    const classe = classeVariacao(indicador.polaridade, indicador.variacao.direcao);

    return `
    <article class="card">
      <h5 class="card-titulo">${indicador.titulo}</h5>
      <p class="card-valor">${valorFormatado}<span class="card-unidade">${indicador.unidade}</span></p>
      <p class="card-variacao ${classe}">${seta} ${indicador.variacao.texto}</p>
      <p class="card-periodo">${indicador.periodo}</p>
    </article>
  `;
}

// -----------------------------------------------------
// 2. Funções de renderização
// -----------------------------------------------------

/**
 * Preenche o título de cada seção a partir do array secoes do JSON.
 */
function renderizarTitulosDasSecoes(secoes) {
    secoes.forEach((secao) => {
        // Título da seção
        const elementoSecao = document.querySelector(`[data-secao="${secao.id}"] .grupo-titulo`);
        if (elementoSecao) {
            elementoSecao.textContent = secao.nome;
        } else {
            console.warn(`⚠️  Seção "${secao.id}" não encontrada no HTML.`);
        }

        // Títulos das subseções (se houver)
        if (secao.subsecoes) {
            secao.subsecoes.forEach((sub) => {
                const elementoSub = document.querySelector(
                    `[data-secao="${secao.id}"] [data-subsecao="${sub.id}"] .subsecao-titulo`
                );
                if (elementoSub) {
                    // Se o nome for vazio, mantém vazio (CSS esconde)
                    elementoSub.textContent = sub.nome || "";
                } else {
                    console.warn(`⚠️  Subseção "${sub.id}" não encontrada no HTML.`);
                }
            });
        }
    });
}

/**
 * Insere cada indicador na seção correta do HTML.
 */
function renderizarIndicadores(indicadores) {
    indicadores.forEach((indicador) => {
        let container;

        if (indicador.subsecao) {
            // Indicador pertence a uma subseção
            container = document.querySelector(
                `[data-secao="${indicador.secao}"] [data-subsecao="${indicador.subsecao}"] .grade-cards`
            );
        } else {
            // Indicador pertence diretamente à seção (sem subseção)
            container = document.querySelector(
                `[data-secao="${indicador.secao}"] > .grade-cards`
            );
        }

        if (!container) {
            console.warn(
                `⚠️  Container para indicador "${indicador.titulo}" não encontrado ` +
                `(seção="${indicador.secao}", subsecao="${indicador.subsecao || 'nenhuma'}").`
            );
            return;
        }

        container.insertAdjacentHTML("beforeend", montarCardHTML(indicador));
    });
}

// -----------------------------------------------------
// 3. Fluxo principal
// -----------------------------------------------------

async function carregarDados() {
    console.log("🔎 Iniciando carregamento de dados.json…");

    const resposta = await fetch("data/dados.json");
    const dados = await resposta.json();

    console.log(`✅ JSON carregado: ${dados.secoes.length} seções, ${dados.indicadores.length} indicadores.`);

    renderizarTitulosDasSecoes(dados.secoes);
    renderizarIndicadores(dados.indicadores);

    console.log("🎉 Renderização concluída.");
}

carregarDados();
