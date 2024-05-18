import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_extras.add_vertical_space import add_vertical_space
import locale

# =================== Set Locale ===========================#
locale.setlocale(locale.LC_MONETARY, "Portuguese_Brazil.1252") 

#==================== Carregando Dados =====================#
df = st.session_state['data']
df.sort_values(['Date'])
df['Month'] = df['Date'].apply(lambda x: x.month)

#==================== Auxiliares ===========================#
deparaeixo ={
    'Tipo de cliente':'Customer type', 
    'Gênero':'Gender',
    'Tipo de produto':'Product line',
}

deparaanalise = {
    'Faturamento': 'Total', 
    'Margem': 'gross income'
}


# ==================== PLOT FUNCTIONS ======================#
def pie_plot(dataframe, cities: list):
    specs = [[{'type':'domain'},{'type':'domain'}, {'type':'domain'}]]
    fig = make_subplots(rows=1, cols=len(cities), specs=specs)
    for i, city in enumerate(cities):
        df = dataframe[dataframe['City'] == city]
        fig.add_trace(
            go.Pie(
                values=df['Total'].tolist(),
                labels=df['Product line'].unique().tolist(),
                title=city
            ),
            row=1, col=i+1
        )

    fig.update_traces(textposition='inside', textinfo='value+percent')
    fig = go.Figure(fig)
    return fig

# ====================== Sidebar ========================== #
with st.sidebar:
    st.caption('**Filtros**')
    eixo = st.selectbox(
        label='Selecione o eixo', 
        options=['Gênero', 'Tipo de cliente', 'Tipo de produto'],
        index=0
        )
    choice = st.multiselect(
        label='Período', 
        options=df['Month'].sort_values().unique().tolist(),
        placeholder="Todo o período",
        default=df['Month'].sort_values().unique().tolist()[-1],
    )

# ===================== DATASETs =========================== #


df_filtered_period = df if not choice else df[df['Month'].isin(choice)]
df_evolucao = df_filtered_period.groupby(['Date', 'City'])[['Total']].sum().reset_index().set_index('Date')
# ----------------------- DF TM ----------------------------#
df_sum = df.groupby(['City', 'Month','Product line'])['Total'].sum().reset_index().set_index(['City', 'Month','Product line'])
df_count = df.groupby(['City', 'Month','Product line'])['Invoice ID'].count().reset_index().set_index(['City', 'Month','Product line'])
df_tm = df_sum.join(df_count)
df_tm['Ticket Medio'] = df_tm['Total'] / df_tm['Invoice ID']
df_tm.reset_index(inplace=True)
df_tm_all = df_tm.groupby(['City','Product line'])[['Total','Invoice ID']].sum().reset_index()
df_tm_all['Ticket Medio'] = df_tm_all['Total'] / df_tm_all['Invoice ID']
df_tm_period = df_tm_all if not choice else df_tm[df_tm['Month'].isin(choice)]

# --------------------- METRICS ----------------------------#
profit = locale.currency(df_filtered_period['Total'].sum(), grouping=True)
tm = locale.currency(df_tm_period['Total'].sum() / df_tm_period['Invoice ID'].sum(), grouping=True)
quantity = df_filtered_period['Quantity'].sum()


col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='Faturamento', value=f'{profit}')

with col2:
    st.metric(label='Ticket Medio', value=f'{tm}')

with col3:
    st.metric(label='Itens Vendidos', value=f'{quantity}')

add_vertical_space(5)

############################### AREA DOS GRÁFICOS #############################
# ============================= EVOLUÇÃO FATURAMENTO =========================== #
st.markdown(f'### ***Evolução*** do Faturamento')
fig_line = px.line(
    data_frame=df_evolucao,
    x=df_evolucao.index,
    y='Total',
    color='City'
   
)
st.plotly_chart(fig_line, use_container_width=True)


# ================================ FATURAMENTO POR CATEGORIA  ================== #
st.markdown(f'### ***Faturamento*** por categoria')
st.plotly_chart(
    pie_plot(
        dataframe=df_filtered_period, 
        cities=df_filtered_period['City'].unique().tolist()
    ),
    use_container_width=True
)


# ================================ Ticket Médio ==================================#
st.markdown('#### Ticket Médio por Categoria')
st.plotly_chart(
    px.histogram(
        data_frame=df_tm_period,
        x='Product line',
        y='Ticket Medio',
        barmode='group',
        color='City'       
    ),
    use_container_width=True
)

#============================ Análise =========================================== #
st.markdown(f'### Faturamento por ***{eixo.lower()}***')
fig_one = px.histogram(
    data_frame=df_filtered_period, 
    x=deparaeixo[eixo], 
    y='Total',
    color='City',
    barmode='group', 

    )
st.plotly_chart(fig_one, use_container_width=True)



