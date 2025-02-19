import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Embed
from discord.ui import TextInput, Modal
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Pegar o token do bot a partir da variável de ambiente
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento para quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f'{bot.user} está conectado ao Discord!')

# Modal para pegar o nome do canal
class CanalModal(Modal):
    def __init__(self):
        super().__init__(title="Nome do Canal")

        # Campo de input para nome do canal
        self.nome_canal = TextInput(
            label="Qual o nome do canal?",
            placeholder="Digite o nome do canal",
            required=True,
            max_length=100
        )
        self.add_item(self.nome_canal)

    async def on_submit(self, interaction: discord.Interaction):
        nome = self.nome_canal.value
        guild = interaction.guild

        # Encontrar a categoria "Canais" (ou qualquer outra que você queira)
        category = discord.utils.get(guild.categories, name="═════ •『BATE PONTO』• ═════")

        if category is None:
            await interaction.response.send_message("Não encontrei a categoria 'Canais'. Certifique-se de que ela existe!", ephemeral=True)
            return

        # Adicionar o prefixo fixo antes do nome personalizado
        nome_com_prefixo = f"『📑』{nome}"

        # Permissões
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Nenhum membro pode ver o canal por padrão
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),  # Permissões para quem criou o canal
        }

        # Permitir que os administradores vejam e enviem mensagens
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        try:
            # Criar o canal com o nome fornecido na categoria "Canais"
            new_channel = await guild.create_text_channel(nome_com_prefixo, category=category, overwrites=overwrites)

            # Mensagem a ser enviada no canal criado
            mensagem = f"QRA:\n\nINICIO:\n\nPAUSA:\n\nCONTINUIDADE:\n\nFINAL:\n\nTOTAL:\n\nPRINTS:\n\n(OBs: A partir de hoje, É obrigatório que se pôr acaso vocês derem um intervalo de tempo no patrulhamento, marquem o início da pausa e o horário da continuação, caso não haja a constatação do mesmo, o relatório estará sujeita a anulação)"

            # Enviar a mensagem no canal criado
            await new_channel.send(mensagem)

            # Enviar a menção do usuário após a mensagem
            await new_channel.send(f"\n{interaction.user.mention}")

            # Resposta final com o canal criado
            await interaction.response.send_message(f'Canal "{new_channel.name}" criado com sucesso na categoria "Canais"!', ephemeral=True)

        except Exception as e:
            # Em caso de erro, enviar uma mensagem com o erro
            await interaction.response.send_message(f'Ocorreu um erro ao criar o canal: {str(e)}', ephemeral=True)

# Comando para criar o botão que permite criar um canal
@bot.command()
async def criar_canal(ctx):
    # Embed de apresentação
    embed = Embed(
        title="Criar Canal Personalizado",
        description="Clique no botão abaixo para criar um canal com nome personalizado!",
        color=discord.Color.blue()
    )

    # Botão que irá acionar a criação do canal
    button = Button(label="Criar Canal", style=discord.ButtonStyle.green)

    # Função que será chamada quando o botão for pressionado
    async def button_callback(interaction):
        # Criar o Modal para inserir o nome do canal
        modal = CanalModal()
        await interaction.response.send_modal(modal)

    # Adiciona a função ao botão
    button.callback = button_callback

    # Adiciona o botão à view
    view = View()
    view.add_item(button)

    # Envia a mensagem com o embed e o botão
    await ctx.send(embed=embed, view=view)

# Rodar o bot com seu token
bot.run(token)
