import aiohttp  # type: ignore
import asyncio
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Label, Button, Entry

async def pegar_cotacoes():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://economia.awesomeapi.com.br/last/USD-BRL") as response:
            requisicao_dic = await response.json()

            cotacao_dolar = requisicao_dic['USDBRL']['bid']

            texto_resposta.config(text=f'''
            Dólar: {cotacao_dolar}''')

def pegar_cotacoes_callback():
    asyncio.run(pegar_cotacoes())

def converter_moeda():
    try:
        valor = float(entrada_valor.get())
        cotacao_dolar = float(texto_resposta.cget("text").split()[1])
        taxa = float(entrada_taxa.get()) / 100

        valor_em_reais = valor * cotacao_dolar * (1 - taxa)

        texto_conversao.config(text=f'''
        Valor em Reais: {valor_em_reais:.2f}''')
    except ValueError:
        texto_conversao.config(text="Insira um valor válido")

# Inicializa o estilo ttkbootstrap com um tema
style = Style(theme="cyborg")

janela = style.master
janela.title("Cotação Atual de Moedas")

texto = Label(janela, text="Puxe a cotação para iniciar", anchor="center", justify="center")
texto.grid(column=0, row=0, columnspan=4, padx=10, pady=10)

botao = Button(janela, text="Cotação Atual", command=pegar_cotacoes_callback, bootstyle="outline")
botao.grid(column=0, row=1, columnspan=4, padx=10, pady=10)

texto_resposta = Label(janela, text="      \n ", anchor="center", justify="center")
texto_resposta.grid(column=0, row=2, columnspan=4, padx=10, pady=10)

entrada_valor = Entry(janela, width=10)
entrada_valor.insert(0, "0")
entrada_valor.grid(column=0, row=3, padx=10, pady=10)

texto_taxa = Label(janela, text="US$ -")
texto_taxa.grid(column=1, row=3, padx=5, pady=10)

entrada_taxa = Entry(janela, width=5)
entrada_taxa.insert(0, "0")
entrada_taxa.grid(column=2, row=3, padx=5, pady=10)

texto_taxa_porcentagem = Label(janela, text="%")
texto_taxa_porcentagem.grid(column=3, row=3, padx=5, pady=10)

botao_converter = Button(janela, text="Converter", command=converter_moeda, bootstyle="outline")
botao_converter.grid(column=0, row=4, columnspan=4, padx=10, pady=10)

texto_conversao = Label(janela, text="R$ 0,00", anchor="center", justify="center")
texto_conversao.grid(column=0, row=5, columnspan=4, padx=10, pady=10)

janela.mainloop()
