# Tratamento de medidas de gravidade com pêndulo simples

_[Read in English](README.md)_

Um script Python the linha de comando que analisa e trata dados experimentais reais coletados por alunos do ensino médio, medindo a aceleração da gravidade local (_g_) usando um pêndulo simples. Este foi meu projeto de conclusão da fase de fundamentos de Python dos meus estudos autônomos em Ciência de Dados.

## Sobre os dados

O tataset (`data/pendulum_measurements.csv`) contém medições reais coletas pelos meus próprios alunos ,em uma aula de física que ministrei em uma escola pública em Juiz de Fora, MG. Cada grupo cronometrou as oscilações de um pêndulo, calculou sua estimativa de _g_, e comparou com o valor teórico local (9,78 m/s²) para calcular um erro percentual. Os identificadores dos grupos foram anonimizados (`G01`, `G02`, ...).

Os dados são propositalmente "reais" e imperfeitos: incluem uma linha com valor faltante (que o grupo não calculou) e uma medição extremamente destoante (outlier), que o script precisa tratar de forma robusta em vez de simplesmente travar.

## O que o script faz

1. **Lê** o arquivo CSV e valida cada linha (ignora valores malformados ou faltantes sem interromper o programa inteiro).
2. **Separa outliers**: qualquer grupo com erro percentual acima de um limite configurável (10% por padrão) é excluído das estatísticas, mas ainda listado separadamente, por transparência.
3. **Calcula estatísticas**: média de _g_ medido pelos grupos, desvio em relação ao valor esperado, grupos mais e menos precisos.
4. **Classifica a precisão de cada grupo** como `Excelent`, `Good`ou `Needs review`, com base no erro percentual.
5. **Gera um relatório formatado**, impressono console e salvo em `pendulum_report.txt`

## Como rodar

```bash
python3 pendulum_analyzer.py
```

Não possui dependências externas — construído inteiramente com a biblioteca padrão do Python (`csv`).

## Estrutura do projeto

```
pendulum-gravity-analyzer/
├── pendulum_analyzer.py         # script principal
├── data/
│   └── pendulum_measurements.csv
├── README.md
└── README.pt-br.md
```

## Exemplo de saída

```
==================================================
REPORT - GRAVITY MEASUREMENT WITH SIMPLE PENDULUM
==================================================
Theoretical reference value: 9.78 m/s²
Outlier error threshold: 10%
Total valid groups: 14
Total excluded groups (outliers): 13

Results per group (valid):
--------------------------------------------------
G02        g = 9.46 m/s²  error = 3.3%  -> Good
G07        g = 9.60 m/s²  error = 1.8%  -> Excellent
...

Overall statistics (valid groups only):
--------------------------------------------------
Mean measured g: 10.025 m/s²
Deviation of the mean from the theoretical value: +0.245 m/s²
Most precise group: G07 (error of 1.8%)
Least precise group: G09 (error of 9.9%)
==================================================
```

## O que aprendi enquanto codava

Este foi o projeto final da primeira fase do meu plano de estudos de Python para Ciência de Dados, pensado para reunir tudo que estudei nessa fase em uma ferramenta única, funcional e com dados reais — em vez de exercícios isolados:

- **Variáveis, tipos de dados e operadores** — trabalhando com floats para medições físicas e percentuais
- **Estruturas de controle** (`if`/`elif`/`else`) — classificando a precisão de cada grupo
- **Estruturas de dados** — representando cada grupo como um dicionário, e o dataset inteiro como uma lista de dicionários
- **Funções** — dividindo o programa em etapas de responsabilidade única: ler → validar → separar outliers → calcular estatísticas → formatar → salvar
- **List comprehensions** — filtrando dados válidos vs. outliers em uma linha
- **Manipulação de strings e f-strings** — montando um relatório alinhado e legível, com números formatados (`.2f`, `+.3f`, padding)
- **Tratamento de erros (`try`/`except`)** — o dataset tem um valor faltante e um outlier extremo; o script precisou continuar rodando e reportar claramente o que aconteceu, em vez de travar
- **Leitura/escrita de arquivos** — lendo o CSV com `csv.DictReader` e escrevendo o relatório final em um arquivo `.txt`

## Próximos passos

Esse mesmo datased vai ser reutilizado em uma fase posterior do meu plano de estudos, onde vou refazer a análise usando **pandas** em vez da biblioteca padrão — uma comparação deliberada entre a abordagem "manual" e a abordagem com biblioteca, para o mesmo problema real.

Além disso, também pretendo tratar e analisar os dados com ferramentas estatísticas mais robustas para entender melhor a relevância dos resultados obtidos pelos estudantes.

---

_Parte do meu percurso de estudos autônomos em Python para Ciência de Dados. Feedbacks são bem-vindos!_
