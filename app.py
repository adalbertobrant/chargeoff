import streamlit as st
import pandas as pd
import yfinance as yf  # Alternativa ao pandas_datareader
import datetime
import plotly.express as px
import requests
import warnings
import os
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard Cartão de Crédito EUA", layout="wide")

st.title("📈 Dashboard de Taxas de Cartão de Crédito nos EUA")
st.markdown("""
Este painel exibe dados históricos do Federal Reserve (FRED) sobre taxas de inadimplência
e baixas por prejuízo de cartões de crédito em bancos comerciais nos Estados Unidos.
""")

# --- FUNÇÃO PARA BUSCAR DADOS DO FRED VIA API ---
@st.cache_data(ttl=6*60*60)  # Cache por 6 horas
def fetch_fred_data_api(series_id, start_date, end_date, api_key=None):
    """
    Busca dados do FRED via API REST.
    Args:
        series_id (str): ID da série FRED
        start_date (str): Data de início no formato YYYY-MM-DD
        end_date (str): Data de fim no formato YYYY-MM-DD
        api_key (str): Chave da API FRED (opcional)
    Returns:
        pandas.DataFrame: DataFrame com os dados
    """
    try:
        # URL da API do FRED
        if api_key:
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
        else:
            # Usando sem API key (limitado)
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&file_type=json&observation_start={start_date}&observation_end={end_date}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'observations' in data:
                df = pd.DataFrame(data['observations'])
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df.set_index('date')
                return df[['value']]
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados via API: {e}")
        return pd.DataFrame()

# --- FUNÇÃO ALTERNATIVA USANDO YFINANCE PARA DADOS ECONÔMICOS ---
@st.cache_data(ttl=6*60*60)
def fetch_economic_data_yf(start_date, end_date):
    """
    Busca dados econômicos usando yfinance como alternativa.
    Nota: Esta é uma solução de contorno - os dados específicos do FRED 
    podem não estar disponíveis via yfinance.
    """
    try:
        # Exemplo com índices relacionados ao setor financeiro
        tickers = ['^GSPC', 'XLF']  # S&P 500 e Financial Sector
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        return data
    except Exception as e:
        st.error(f"Erro ao buscar dados via yfinance: {e}")
        return pd.DataFrame()

# --- FUNÇÃO PARA DADOS SIMULADOS EM CASO DE FALHA ---
@st.cache_data(ttl=6*60*60)
def create_sample_data(start_date, end_date):
    """
    Cria dados de exemplo para demonstração.
    """
    import numpy as np
    
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    np.random.seed(42)
    
    # Simular taxas de inadimplência e baixa por prejuízo
    base_delinquency = 3.5
    base_chargeoff = 4.2
    
    delinquency_rates = base_delinquency + np.random.normal(0, 1.5, len(dates))
    chargeoff_rates = base_chargeoff + np.random.normal(0, 1.8, len(dates))
    
    # Adicionar picos durante períodos de crise (2008-2010, 2020)
    for i, date in enumerate(dates):
        if 2008 <= date.year <= 2010:
            delinquency_rates[i] += 2.5
            chargeoff_rates[i] += 3.0
        elif date.year == 2020:
            delinquency_rates[i] += 1.5
            chargeoff_rates[i] += 2.0
    
    # Garantir valores positivos
    delinquency_rates = np.maximum(delinquency_rates, 0.5)
    chargeoff_rates = np.maximum(chargeoff_rates, 0.5)
    
    df = pd.DataFrame({
        'Taxa de Inadimplência (%)': delinquency_rates,
        'Taxa de Baixa por Prejuízo (%)': chargeoff_rates
    }, index=dates)
    
    return df

# --- CONFIGURAÇÃO DOS DADOS E INTERFACE ---

# IDs das séries do FRED
SERIES_IDS = {
    "Taxa de Inadimplência (%)": "DRCCLACBS",
    "Taxa de Baixa por Prejuízo (%)": "CORCCACBS"
}

st.sidebar.header("Opções do Gráfico")

# Chave da API FRED do arquivo .env
fred_api_key = os.getenv('API_FRED')

# Mostrar status da API na sidebar
if fred_api_key:
    st.sidebar.success("✅ Chave da API FRED carregada do .env")
else:
    st.sidebar.warning("⚠️ Chave da API FRED não encontrada no .env")
    # Opção para inserir manualmente se não estiver no .env
    fred_api_key = st.sidebar.text_input(
        "Chave da API FRED (manual)", 
        type="password",
        help="Obtém uma chave gratuita em https://fred.stlouisfed.org/docs/api/api_key.html"
    )

# Seletores de data
default_start_date = datetime.date(1990, 1, 1)
default_end_date = datetime.date.today()

start_date = st.sidebar.date_input(
    "Data de Início", 
    default_start_date, 
    min_value=datetime.date(1980,1,1), 
    max_value=default_end_date
)
end_date = st.sidebar.date_input(
    "Data de Fim", 
    default_end_date, 
    min_value=start_date, 
    max_value=default_end_date
)

# Opção de fonte de dados (automática baseada na disponibilidade da API)
if fred_api_key:
    data_source = st.sidebar.selectbox(
        "Fonte de Dados",
        ["FRED API", "Dados Simulados (Demo)"],
        index=0,  # FRED API como padrão quando a chave está disponível
        help="FRED API selecionada automaticamente (chave encontrada)"
    )
else:
    data_source = st.sidebar.selectbox(
        "Fonte de Dados",
        ["Dados Simulados (Demo)", "FRED API"],
        index=0,  # Dados simulados como padrão quando não há chave
        help="Configure API_FRED no arquivo .env para usar dados reais"
    )

# Botão para atualizar
if st.sidebar.button("Atualizar Dados Agora"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Fonte dos Dados:** [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)
**Séries FRED Utilizadas:**
- `DRCCLACBS`: Taxa de Inadimplência
- `CORCCACBS`: Taxa de Baixa por Prejuízo

**Configuração:**
- Adicione `API_FRED=sua_chave_aqui` no arquivo `.env`
- Obtenha uma chave gratuita em: [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
""")

# --- BUSCAR E EXIBIR DADOS ---
if start_date <= end_date:
    data = pd.DataFrame()
    
    if data_source == "FRED API":
        if fred_api_key:
            # Buscar cada série individualmente
            all_series = {}
            for name, series_id in SERIES_IDS.items():
                series_data = fetch_fred_data_api(
                    series_id, 
                    start_date.strftime('%Y-%m-%d'), 
                    end_date.strftime('%Y-%m-%d'),
                    fred_api_key
                )
                if not series_data.empty:
                    all_series[name] = series_data['value']
            
            if all_series:
                data = pd.DataFrame(all_series)
        else:
            st.warning("⚠️ Chave da API FRED não fornecida. Usando dados simulados para demonstração.")
            data = create_sample_data(start_date, end_date)
    else:
        # Usar dados simulados
        data = create_sample_data(start_date, end_date)

    if not data.empty:
        st.subheader("Gráfico das Taxas de Cartão de Crédito")

        # Criar o gráfico com Plotly Express
        fig = px.line(
            data, 
            x=data.index, 
            y=data.columns,
            labels={"value": "Taxa (%)", "variable": "Métrica", "index": "Data"},
            markers=True
        )

        fig.update_layout(
            hovermode="x unified",
            legend_title_text='Métricas',
            xaxis_title="Data",
            yaxis_title="Taxa (%)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Mostrar dados em tabela
        st.subheader("Dados Recentes")
        recent_data = data.tail(12).sort_index(ascending=False)
        st.dataframe(
            recent_data.style.format("{:.2f}%"),
            use_container_width=True
        )

        # Análise estatística
        st.subheader("Estatísticas do Período")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Taxa de Inadimplência (%)**")
            if "Taxa de Inadimplência (%)" in data.columns:
                delinq_col = data["Taxa de Inadimplência (%)"].dropna()
                st.metric("Atual", f"{delinq_col.iloc[-1]:.2f}%")
                st.metric("Média", f"{delinq_col.mean():.2f}%")
                st.metric("Máximo", f"{delinq_col.max():.2f}%")
                st.metric("Mínimo", f"{delinq_col.min():.2f}%")
        
        with col2:
            st.markdown("**Taxa de Baixa por Prejuízo (%)**")
            if "Taxa de Baixa por Prejuízo (%)" in data.columns:
                chargeoff_col = data["Taxa de Baixa por Prejuízo (%)"].dropna()
                st.metric("Atual", f"{chargeoff_col.iloc[-1]:.2f}%")
                st.metric("Média", f"{chargeoff_col.mean():.2f}%")
                st.metric("Máximo", f"{chargeoff_col.max():.2f}%")
                st.metric("Mínimo", f"{chargeoff_col.min():.2f}%")

        # Análise de tendência
        st.subheader("Análise de Tendência")
        if len(data) >= 12:
            recent_12m = data.tail(12)
            previous_12m = data.iloc[-24:-12] if len(data) >= 24 else data.head(12)
            
            for col in data.columns:
                if col in recent_12m.columns and col in previous_12m.columns:
                    recent_avg = recent_12m[col].mean()
                    previous_avg = previous_12m[col].mean()
                    change = recent_avg - previous_avg
                    
                    trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    st.write(f"{trend} **{col}**: Mudança de {change:+.2f}% nos últimos 12 meses")

    else:
        st.warning("Não foi possível carregar os dados. Verifique a configuração ou tente novamente.")
else:
    st.error("A data de início deve ser anterior ou igual à data de fim.")

# Rodapé
st.markdown("---")
st.markdown("""
**Desenvolvido com Python e Streamlit**

*Nota: Este é um painel de demonstração. Para dados oficiais e atualizados, 
visite [FRED - Federal Reserve Economic Data](https://fred.stlouisfed.org/)*
""")
