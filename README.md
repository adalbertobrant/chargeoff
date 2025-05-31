# 📈 Dashboard de Taxas de Cartão de Crédito - EUA

Um dashboard interativo construído com **Streamlit** que exibe dados históricos das taxas de inadimplência e baixas por prejuízo (charge-off) de cartões de crédito em bancos comerciais dos Estados Unidos, obtidos diretamente do Federal Reserve Economic Data (FRED).

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🚀 Funcionalidades

- **Dados em Tempo Real**: Integração com a API do FRED para dados atualizados
- **Visualizações Interativas**: Gráficos dinâmicos com Plotly
- **Análise Estatística**: Métricas, tendências e comparações históricas
- **Interface Intuitiva**: Dashboard responsivo e fácil de usar
- **Múltiplas Fontes**: API FRED ou dados simulados para demonstração
- **Cache Inteligente**: Otimização de performance com cache de 6 horas

## 📊 Métricas Disponíveis

| Métrica | Série FRED | Descrição |
|---------|------------|-----------|
| **Taxa de Inadimplência** | `DRCCLACBS` | Percentual de empréstimos com 90+ dias em atraso |
| **Taxa de Baixa por Prejuízo** | `CORCCACBS` | Percentual de dívidas consideradas incobráveis |

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework para aplicações web
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados
- **[Plotly](https://plotly.com/)** - Visualizações interativas
- **[FRED API](https://fred.stlouisfed.org/)** - Federal Reserve Economic Data
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** - Gerenciamento de variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.12. ou superior
- Chave da API FRED (gratuita)

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/adalbertobrant/chargeoff.git
cd chargeoff
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a API FRED
1. Obtenha uma chave gratuita em: [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Crie um arquivo `.env` na raiz do projeto:
```bash
# .env
API_FRED=sua_chave_da_api_fred_aqui
```

### 4. Execute o aplicativo
```bash
streamlit run app.py
```

O dashboard estará disponível em: http://localhost:8501

## 📁 Estrutura do Projeto

```
chargeoff/
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências Python
├── .env               # Variáveis de ambiente (não commitado)
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Este arquivo
```

## 🎯 Como Usar

1. **Acesse o Dashboard**: Abra http://localhost:8501 no seu navegador
2. **Configure Período**: Use a barra lateral para selecionar as datas
3. **Escolha a Fonte**: FRED API (dados reais) ou Simulados (demo)
4. **Explore os Dados**: Visualize gráficos, tabelas e estatísticas
5. **Analise Tendências**: Compare períodos e identifique padrões

## 📈 Capturas de Tela

### Dashboard Principal
- Gráfico interativo com séries temporais
- Controles de data na barra lateral
- Indicadores de status da API

### Análise Estatística
- Métricas atuais, médias, máximos e mínimos
- Análise de tendências dos últimos 12 meses
- Comparações com picos históricos (crise 2008-2010)

## 🔧 Configuração Avançada

### Variáveis de Ambiente (.env)
```bash
# Chave da API FRED (obrigatória para dados reais)
API_FRED=sua_chave_aqui

# Configurações opcionais
DEBUG=True
PORT=8501
```

### Personalização
O código é modular e permite fácil personalização:
- Adicionar novas séries do FRED
- Modificar visualizações
- Incluir análises adicionais
- Customizar interface

## 🐛 Resolução de Problemas

### Erro "distutils not found"
Se encontrar erros relacionados ao `distutils`:
```bash
pip install --upgrade setuptools>=65.0.0
```

### API FRED não funciona
- Verifique se a chave está correta no arquivo `.env`
- Confirme se a chave não expirou
- Use "Dados Simulados" como alternativa

### Dependências
Se houver problemas com instalação:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📊 Dados e Fontes

Os dados são obtidos do **Federal Reserve Economic Data (FRED)**, mantido pelo Federal Reserve Bank of St. Louis. As séries utilizadas são:

- **DRCCLACBS**: Delinquency Rate on Credit Card Loans, All Commercial Banks
- **CORCCACBS**: Charge-Off Rate on Credit Card Loans, All Commercial Banks

Ambas as séries são ajustadas sazonalmente e atualizadas trimestralmente.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Ideias para Melhorias

- [ ] Adicionar mais séries econômicas do FRED
- [ ] Implementar alertas de tendências
- [ ] Incluir comparações com outros países
- [ ] Adicionar download de dados em CSV/Excel
- [ ] Criar relatórios automáticos
- [ ] Implementar previsões com ML

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Adalberto Brant**
- GitHub: [@adalbertobrant](https://github.com/adalbertobrant)
- LinkedIn: [adalbertobrant](https://linkedin.com/in/ilha)

## 🙏 Agradecimentos

- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) pelos dados
- [Streamlit](https://streamlit.io/) pelo framework fantástico
- Comunidade Python pelos packages incríveis

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐

## 📞 Suporte

Se você encontrar problemas ou tiver sugestões:
- Abra uma [Issue](https://github.com/adalbertobrant/chargeoff/issues)
- Entre em contato através das redes sociais
- Consulte a [documentação do FRED](https://fred.stlouisfed.org/docs/api/)

---

*Dashboard desenvolvido para análise de risco de crédito e educação financeira. Dados fornecidos pelo Federal Reserve Economic Data (FRED).*
