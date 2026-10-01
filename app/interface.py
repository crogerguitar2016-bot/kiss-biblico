# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.metrics import dp
from kivy.utils import platform
from kivy.core.window import Window

from kivy.uix.screenmanager import (
    ScreenManager,
    Screen
)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from app.controlador import ControladorJornada
from app.jornada_estado import EstadoJornada
from app.recompensas import Recompensas

from app.tema import (
    aplicar_fundo_anil,
    criar_logo,
    Botao3D,
    CampoNome3D,
    Bloco3D,
    BRANCO,
    VERDE,
    VERDE_SOMBRA,
    VERMELHO,
    VERMELHO_SOMBRA,
)


if platform != "android":

    Window.size = (
        410,
        800
    )


# ======================================================
# LABEL
# ======================================================

def criar_credito_autor():

    return label_branco(
        "Autor do aplicativo, Carlos Rogério.",
        "13sp",
        24,
        False
    )


def label_branco(
    texto="",
    tamanho="17sp",
    altura=40,
    bold=False
):

    label = Label(
        text=texto,
        color=BRANCO,
        font_size=tamanho,
        bold=bold,
        size_hint_y=None,
        height=dp(altura),
        halign="center",
        valign="middle"
    )

    label.bind(
        size=lambda obj, valor:
        setattr(
            obj,
            "text_size",
            valor
        )
    )

    return label


# ======================================================
# AVISO
# ======================================================

def mostrar_aviso(
    titulo,
    texto
):

    caixa = BoxLayout(
        orientation="vertical",
        padding=dp(16),
        spacing=dp(12)
    )

    mensagem = Label(
        text=texto,
        color=BRANCO,
        font_size="17sp",
        halign="center",
        valign="middle"
    )

    mensagem.bind(
        size=lambda obj, valor:
        setattr(
            obj,
            "text_size",
            (
                valor[0] - dp(20),
                None
            )
        )
    )

    caixa.add_widget(
        mensagem
    )

    fechar = Botao3D(
        text="FECHAR",
        size_hint_y=None,
        height=dp(55)
    )

    caixa.add_widget(
        fechar
    )

    popup = Popup(
        title=titulo,
        content=caixa,
        size_hint=(
            0.88,
            0.43
        ),
        auto_dismiss=False
    )

    fechar.bind(
        on_release=
            popup.dismiss
    )

    popup.open()


# ======================================================
# NOME
# ======================================================

class TelaNome(Screen):

    def __init__(
        self,
        controlador,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.controlador = controlador

        aplicar_fundo_anil(
            self
        )

        raiz = BoxLayout(
            orientation="vertical",
            padding=dp(22),
            spacing=dp(14)
        )

        raiz.add_widget(
            criar_logo(
                300
            )
        )

        raiz.add_widget(
            criar_credito_autor()
        )

        raiz.add_widget(
            label_branco(
                "COMO VOCÊ GOSTARIA\n"
                "DE SER CHAMADO?",
                "19sp",
                65,
                True
            )
        )

        self.nome = CampoNome3D(
            hint_text="Digite seu nome",
            size_hint_y=None,
            height=dp(58),
            padding=[
                dp(18),
                dp(16)
            ]
        )

        raiz.add_widget(
            self.nome
        )

        iniciar = Botao3D(
            text="INICIAR JORNADA",
            size_hint_y=None,
            height=dp(62)
        )

        iniciar.bind(
            on_release=
                self.salvar_nome
        )

        raiz.add_widget(
            iniciar
        )

        raiz.add_widget(
            Widget()
        )

        self.add_widget(
            raiz
        )


    def salvar_nome(
        self,
        *args
    ):

        try:

            self.controlador.definir_nome(
                self.nome.text
            )

        except ValueError as erro:

            mostrar_aviso(
                "Nome",
                str(erro)
            )

            return

        self.manager.current = (
            "inicio"
        )


# ======================================================
# INÍCIO
# ======================================================

class TelaInicio(Screen):

    def __init__(
        self,
        controlador,
        estado_jornada,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.controlador = controlador
        self.estado_jornada = estado_jornada

        aplicar_fundo_anil(
            self
        )

        raiz = BoxLayout(
            orientation="vertical",
            padding=[
                dp(16),
                dp(12),
                dp(16),
                dp(18)
            ],
            spacing=dp(12)
        )

        raiz.add_widget(
            criar_logo(
                245
            )
        )

        raiz.add_widget(
            criar_credito_autor()
        )


        self.botao_nome = Botao3D(
            text="",
            size_hint_y=None,
            height=dp(58)
        )

        raiz.add_widget(
            self.botao_nome
        )

        self.botao_nome.bind(
            on_release=
                self.editar_nome
        )


        grade = GridLayout(
            cols=2,
            spacing=dp(12),
            row_default_height=dp(82),
            row_force_default=True,
            size_hint_y=None,
            height=dp(270)
        )


        continuar = Botao3D(
            text="CONTINUAR\nJORNADA"
        )

        erros = Botao3D(
            text="PERGUNTAS\nQUE ERREI"
        )

        livros = Botao3D(
            text="LIVROS\nDA BÍBLIA"
        )

        progresso = Botao3D(
            text="MEU\nPROGRESSO"
        )

        desafio = Botao3D(
            text="DESAFIO\nDIÁRIO"
        )

        conquistas = Botao3D(
            text="CONQUISTAS"
        )


        for botao in [
            continuar,
            erros,
            livros,
            progresso,
            desafio,
            conquistas
        ]:

            grade.add_widget(
                botao
            )


        raiz.add_widget(
            grade
        )


        self.resumo = label_branco(
            "",
            "14sp",
            38
        )

        raiz.add_widget(
            self.resumo
        )


        continuar.bind(
            on_release=
                self.continuar_jornada
        )


        livros.bind(
            on_release=
                lambda *_:
                setattr(
                    self.manager,
                    "current",
                    "livros"
                )
        )


        progresso.bind(
            on_release=
                lambda *_:
                setattr(
                    self.manager,
                    "current",
                    "progresso"
                )
        )


        erros.bind(
            on_release=
                self.abrir_erros
        )


        desafio.bind(
            on_release=
                self.abrir_desafio
        )


        conquistas.bind(
            on_release=
                lambda *_:
                setattr(
                    self.manager,
                    "current",
                    "conquistas"
                )
        )


        self.add_widget(
            raiz
        )


    def on_pre_enter(
        self,
        *args
    ):

        nome = (
            self.controlador
            .nome_jogador()
        )

        self.botao_nome.text = (
            nome
            if nome
            else "JOGADOR"
        )


        r = (
            self.controlador
            .meu_progresso()
        )


        self.resumo.text = (
            f'{r["livros_concluidos"]}/66 LIVROS'
            f'   •   {r["xp"]} XP'
            f'   •   {r["moedas"]} MOEDAS'
        )


    def editar_nome(
        self,
        *args
    ):

        caixa = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12)
        )

        campo = CampoNome3D(
            text=
                self.controlador
                .nome_jogador(),

            hint_text=
                "Nome do jogador",

            size_hint_y=None,
            height=dp(58),

            padding=[
                dp(16),
                dp(16)
            ]
        )

        caixa.add_widget(
            campo
        )

        salvar = Botao3D(
            text="SALVAR NOME",
            size_hint_y=None,
            height=dp(58)
        )

        caixa.add_widget(
            salvar
        )

        popup = Popup(
            title="Nome do jogador",
            content=caixa,
            size_hint=(
                0.88,
                None
            ),
            height=dp(235),
            auto_dismiss=False
        )

        def confirmar(
            *args
        ):

            try:

                self.controlador.definir_nome(
                    campo.text
                )

            except ValueError as erro:

                mostrar_aviso(
                    "Nome",
                    str(erro)
                )

                return

            self.botao_nome.text = (
                self.controlador
                .nome_jogador()
            )

            popup.dismiss()

        salvar.bind(
            on_release=
                confirmar
        )

        popup.open()


    def continuar_jornada(
        self,
        *args
    ):

        posicao = (
            self.estado_jornada
            .continuar()
        )


        if posicao is None:

            mostrar_aviso(
                "Jornada concluída",
                (
                    "Você já concluiu "
                    "os 66 livros!"
                )
            )

            return


        abrir_livro_em_pergunta(
            self.manager,
            self.controlador,
            self.estado_jornada,
            posicao["livro"],
            posicao["pergunta"],
            retomar=True
        )


    def abrir_erros(
        self,
        *args
    ):

        total = (
            self.controlador
            .revisao
            .total_pendentes()
        )


        if total == 0:

            mostrar_aviso(
                "Perguntas que errei",
                (
                    "Você não possui perguntas "
                    "pendentes para revisar."
                )
            )

            return


        resultado = (
            self.controlador
            .abrir_revisao()
        )


        if (
            resultado["estado"]
            != "revisao_aberta"
        ):

            mostrar_aviso(
                "Perguntas que errei",
                "Nenhuma pergunta disponível."
            )

            return


        tela = (
            self.manager
            .get_screen(
                "pergunta"
            )
        )

        tela.atualizar()

        self.manager.current = (
            "pergunta"
        )


    def abrir_desafio(
        self,
        *args
    ):

        resultado = (
            self.controlador
            .abrir_desafio()
        )


        if (
            resultado["estado"]
            != "desafio_aberto"
        ):

            mostrar_aviso(
                "Desafio Diário",
                "Não foi possível abrir o desafio."
            )

            return


        tela = (
            self.manager
            .get_screen(
                "pergunta"
            )
        )

        tela.atualizar()

        self.manager.current = (
            "pergunta"
        )


    def aviso_conquistas(
        self,
        *args
    ):

        mostrar_aviso(
            "Conquistas",
            (
                "Selos, estrelas e "
                "pergaminhos serão mostrados "
                "na próxima subetapa."
            )
        )


# ======================================================
# FUNÇÃO CENTRAL PARA ABRIR LIVRO
# ======================================================

def abrir_livro_em_pergunta(
    manager,
    controlador,
    estado_jornada,
    livro,
    numero,
    retomar=False
):

    resultado = (
        controlador
        .abrir_livro(
            livro
        )
    )


    if (
        resultado["estado"]
        != "livro_aberto"
    ):

        mostrar_aviso(
            "Erro",
            "Livro não encontrado."
        )

        return


    numero = max(
        1,
        min(
            30,
            int(numero)
        )
    )


    controlador.motor.indice_pergunta = (
        numero - 1
    )

    controlador.motor.resposta_selecionada = None
    controlador.motor.resposta_confirmada = False


    if retomar:

        restaurado = (
            estado_jornada
            .restaurar_no_motor(
                controlador.motor,
                livro
            )
        )

        if not restaurado:

            controlador.motor.acertos = 0
            controlador.motor.erros = 0

            estado_jornada.iniciar_livro(
                livro,
                numero
            )

    else:

        controlador.motor.acertos = 0
        controlador.motor.erros = 0

        estado_jornada.iniciar_livro(
            livro,
            numero
        )


    tela = manager.get_screen(
        "pergunta"
    )

    tela.atualizar()

    manager.current = (
        "pergunta"
    )


# ======================================================
# LIVROS
# ======================================================

class TelaLivros(Screen):

    def __init__(
        self,
        controlador,
        estado_jornada,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.controlador = controlador
        self.estado_jornada = estado_jornada

        aplicar_fundo_anil(
            self
        )


        raiz = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(10)
        )


        voltar = Botao3D(
            text="VOLTAR",
            size_hint_y=None,
            height=dp(54)
        )

        voltar.bind(
            on_release=
                lambda *_:
                setattr(
                    self.manager,
                    "current",
                    "inicio"
                )
        )


        raiz.add_widget(
            voltar
        )


        raiz.add_widget(
            label_branco(
                "LIVROS DA BÍBLIA",
                "24sp",
                55,
                True
            )
        )


        self.scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=[
                "content",
                "bars"
            ],
            bar_width=dp(10)
        )


        self.grade = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(4),
            size_hint_y=None
        )

        self.grade.bind(
            minimum_height=
                self.grade.setter(
                    "height"
                )
        )


        self.scroll.add_widget(
            self.grade
        )

        raiz.add_widget(
            self.scroll
        )

        self.add_widget(
            raiz
        )


    def on_pre_enter(
        self,
        *args
    ):

        self.montar()


    def montar(self):

        self.grade.clear_widgets()


        livros = (
            self.controlador
            .motor
            .listar_livros()
        )


        for numero, nome in enumerate(
            livros,
            start=1
        ):

            dados = (
                self.controlador
                .progresso
                .dados
                .get(
                    "livros",
                    {}
                )
                .get(
                    nome,
                    {}
                )
            )


            concluido = dados.get(
                "concluido",
                False
            )


            marca = (
                "  ✓"
                if concluido
                else ""
            )


            botao = Botao3D(
                text=(
                    f"{numero}. "
                    f"{nome}"
                    f"{marca}"
                ),
                size_hint_y=None,
                height=dp(62)
            )


            botao.bind(
                on_release=
                    lambda obj,
                    livro=nome:
                    abrir_livro_em_pergunta(
                        self.manager,
                        self.controlador,
                        self.estado_jornada,
                        livro,
                        1
                    )
            )


            self.grade.add_widget(
                botao
            )


# ======================================================
# PERGUNTA
# ======================================================

class TelaPergunta(Screen):

    def __init__(
        self,
        controlador,
        estado_jornada,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.controlador = controlador
        self.estado_jornada = estado_jornada

        self.alternativas = {}

        aplicar_fundo_anil(
            self
        )


        # ==================================================
        # RAIZ
        # ==================================================

        raiz = BoxLayout(
            orientation="vertical",

            padding=[
                dp(10),
                dp(8),
                dp(10),
                dp(10)
            ],

            spacing=dp(6)
        )


        # ==================================================
        # TOPO
        # ==================================================

        topo = BoxLayout(
            size_hint_y=None,
            height=dp(42),
            spacing=dp(7)
        )


        voltar = Botao3D(
            text="VOLTAR",

            size_hint_x=None,
            width=dp(84)
        )


        voltar.bind(
            on_release=
                lambda *_:
                setattr(
                    self.manager,
                    "current",
                    "inicio"
                )
        )


        self.contador = label_branco(
            "",
            "15sp",
            42,
            True
        )


        topo.add_widget(
            voltar
        )

        topo.add_widget(
            self.contador
        )


        raiz.add_widget(
            topo
        )


        # ==================================================
        # NOME DO LIVRO
        # ==================================================

        self.livro = label_branco(
            "",
            "21sp",
            40,
            True
        )

        raiz.add_widget(
            self.livro
        )


        # ==================================================
        # ÁREA CENTRAL ROLÁVEL
        #
        # Se os textos forem muito grandes,
        # nada sairá da tela.
        # ==================================================

        self.scroll_central = ScrollView(
            do_scroll_x=False,
            bar_width=dp(10),
            scroll_type=[
                "content",
                "bars"
            ],

            size_hint=(
                1,
                1
            )
        )


        self.conteudo_central = BoxLayout(
            orientation="vertical",

            size_hint_y=None,

            spacing=dp(8),

            padding=[
                0,
                dp(2),
                0,
                dp(10)
            ]
        )


        self.conteudo_central.bind(
            minimum_height=
                self.conteudo_central.setter(
                    "height"
                )
        )


        # ==================================================
        # QUADRADO DO ENUNCIADO
        # ==================================================

        self.painel_pergunta = Bloco3D(
            orientation="vertical",

            size_hint_y=None,

            height=dp(94),

            padding=[
                dp(12),
                dp(8)
            ]
        )


        self.enunciado = Label(
            text="",

            color=BRANCO,

            font_size="16sp",

            halign="center",
            valign="middle"
        )


        def ajustar_enunciado(
            obj,
            tamanho
        ):

            obj.text_size = (
                max(
                    dp(40),
                    tamanho[0] - dp(18)
                ),

                max(
                    dp(30),
                    tamanho[1] - dp(12)
                )
            )


        self.enunciado.bind(
            size=ajustar_enunciado
        )


        self.painel_pergunta.add_widget(
            self.enunciado
        )


        self.conteudo_central.add_widget(
            self.painel_pergunta
        )


        # ==================================================
        # ALTERNATIVAS
        # ==================================================

        self.area_alternativas = BoxLayout(
            orientation="vertical",

            size_hint_y=None,

            spacing=dp(7)
        )


        self.area_alternativas.bind(
            minimum_height=
                self.area_alternativas.setter(
                    "height"
                )
        )


        self.conteudo_central.add_widget(
            self.area_alternativas
        )


        self.scroll_central.add_widget(
            self.conteudo_central
        )


        raiz.add_widget(
            self.scroll_central
        )


        # ==================================================
        # RESULTADO
        # ==================================================

        self.feedback = label_branco(
            "",
            "14sp",
            54
        )


        raiz.add_widget(
            self.feedback
        )


        # ==================================================
        # DICA / PRÓXIMA
        # ==================================================

        inferior = BoxLayout(
            size_hint_y=None,

            height=dp(52),

            spacing=dp(8)
        )


        self.botao_dica = Botao3D(
            text="DICA"
        )


        self.botao_proxima = Botao3D(
            text="PRÓXIMA"
        )


        self.botao_proxima.disabled = True
        self.botao_proxima.opacity = 0


        self.botao_dica.bind(
            on_release=
                self.mostrar_dica
        )


        self.botao_proxima.bind(
            on_release=
                self.proxima
        )


        inferior.add_widget(
            self.botao_dica
        )

        inferior.add_widget(
            self.botao_proxima
        )


        raiz.add_widget(
            inferior
        )


        self.add_widget(
            raiz
        )


    # ==================================================
    # ALTURA AUTOMÁTICA DO ENUNCIADO
    # ==================================================

    def altura_enunciado(
        self,
        texto
    ):

        tamanho = len(
            texto.strip()
        )


        if tamanho <= 70:

            return dp(88)


        if tamanho <= 120:

            return dp(105)


        if tamanho <= 180:

            return dp(125)


        if tamanho <= 250:

            return dp(145)


        return dp(165)


    # ==================================================
    # ALTURA AUTOMÁTICA DA ALTERNATIVA
    # ==================================================

    def altura_alternativa(
        self,
        texto
    ):

        tamanho = len(
            texto.strip()
        )


        if tamanho <= 45:

            return dp(58)


        if tamanho <= 80:

            return dp(72)


        if tamanho <= 120:

            return dp(86)


        if tamanho <= 165:

            return dp(102)


        return dp(118)


    # ==================================================
    # QUEBRA DE TEXTO DO BOTÃO
    # ==================================================

    def preparar_texto_botao(
        self,
        botao
    ):

        botao.halign = "left"
        botao.valign = "middle"


        def atualizar(
            obj,
            tamanho
        ):

            obj.text_size = (
                max(
                    dp(40),
                    tamanho[0] - dp(18)
                ),

                max(
                    dp(30),
                    tamanho[1] - dp(10)
                )
            )


        botao.bind(
            size=atualizar
        )


    # ==================================================
    # ATUALIZAR PERGUNTA
    # ==================================================

    def atualizar(self):

        pergunta = (
            self.controlador
            .pergunta_atual()
        )


        if pergunta is None:

            return


        livro = (
            self.controlador
            .nome_livro_sessao
            or pergunta.get(
                "livro",
                ""
            )
        )


        self.livro.text = livro


        self.contador.text = (
            f'PERGUNTA '
            f'{pergunta["posicao"]}'
            f'/{pergunta["total_sessao"]}'
        )


        texto_pergunta = (
            pergunta[
                "pergunta"
            ]
        )


        self.enunciado.text = (
            texto_pergunta
        )


        # O quadrado do enunciado fica pequeno
        # quando a pergunta é curta e cresce
        # somente quando necessário.

        self.painel_pergunta.height = (
            self.altura_enunciado(
                texto_pergunta
            )
        )


        self.feedback.text = ""


        self.botao_proxima.disabled = True
        self.botao_proxima.opacity = 0


        self.area_alternativas.clear_widgets()

        self.alternativas = {}


        for letra in "ABCD":

            texto = (
                pergunta[
                    "alternativas"
                ][
                    letra
                ]
            )


            altura = (
                self.altura_alternativa(
                    texto
                )
            )


            linha = BoxLayout(
                size_hint_y=None,

                height=altura,

                spacing=dp(7)
            )


            # ------------------------------------------
            # QUADRADO PEQUENO A / B / C / D
            # ------------------------------------------

            letra_botao = Botao3D(
                text=letra,

                size_hint_x=None,

                width=dp(52),

                font_size="18sp"
            )


            letra_botao.halign = "center"
            letra_botao.valign = "middle"


            # ------------------------------------------
            # QUADRADO GRANDE COM O TEXTO
            # ------------------------------------------

            texto_botao = Botao3D(
                text=texto,

                font_size="13sp"
            )


            self.preparar_texto_botao(
                texto_botao
            )


            letra_botao.bind(
                on_release=
                    lambda obj,
                    l=letra:
                    self.selecionar(
                        l
                    )
            )


            texto_botao.bind(
                on_release=
                    lambda obj,
                    l=letra:
                    self.selecionar(
                        l
                    )
            )


            linha.add_widget(
                letra_botao
            )

            linha.add_widget(
                texto_botao
            )


            self.area_alternativas.add_widget(
                linha
            )


            self.alternativas[
                letra
            ] = (
                letra_botao,
                texto_botao
            )


        # Sempre começa mostrando o topo.
        self.scroll_central.scroll_y = 1


    # ==================================================
    # SELEÇÃO
    # ==================================================

    def selecionar(
        self,
        letra
    ):

        for par in (
            self.alternativas
            .values()
        ):

            for botao in par:

                botao.normal()


        for botao in (
            self.alternativas[
                letra
            ]
        ):

            botao.selecionado()


        self.controlador.selecionar_resposta(
            letra
        )


        caixa = BoxLayout(
            orientation="vertical",

            padding=dp(16),

            spacing=dp(14)
        )


        caixa.add_widget(
            label_branco(
                "Deseja mudar sua resposta?",
                "18sp",
                65,
                True
            )
        )


        botoes = BoxLayout(
            size_hint_y=None,

            height=dp(58),

            spacing=dp(10)
        )


        sim = Botao3D(
            text="SIM"
        )


        nao = Botao3D(
            text="NÃO"
        )


        botoes.add_widget(
            sim
        )

        botoes.add_widget(
            nao
        )


        caixa.add_widget(
            botoes
        )


        popup = Popup(
            title="Resposta",

            content=caixa,

            size_hint=(
                0.88,
                None
            ),

            height=dp(240),

            auto_dismiss=False
        )


        sim.bind(
            on_release=
                lambda *_:
                self.decisao(
                    popup,
                    True
                )
        )


        nao.bind(
            on_release=
                lambda *_:
                self.decisao(
                    popup,
                    False
                )
        )


        popup.open()


    # ==================================================
    # SIM / NÃO
    # ==================================================

    def decisao(
        self,
        popup,
        mudar
    ):

        popup.dismiss()


        if mudar:

            self.controlador.decidir_mudar(
                "SIM"
            )


            for par in (
                self.alternativas
                .values()
            ):

                for botao in par:

                    botao.normal()


            return


        resultado = (
            self.controlador
            .decidir_mudar(
                "NÃO"
            )
        )


        if (
            self.controlador.modo
            == "livro"
        ):

            self.estado_jornada.registrar_resposta(
                resultado["livro"],
                resultado["numero"],
                resultado["acertou"]
            )


        for par in (
            self.alternativas
            .values()
        ):

            for botao in par:

                botao.disabled = True


        correta = resultado[
            "correta"
        ]


        for botao in (
            self.alternativas[
                correta
            ]
        ):

            botao.correto()


        if resultado[
            "acertou"
        ]:

            self.feedback.text = (
                "RESPOSTA CORRETA\n"
                f'+{resultado["xp_ganho"]} XP'
                f'  •  +{resultado["moedas_ganhas"]} MOEDA'
            )


        else:

            escolhida = resultado[
                "escolhida"
            ]


            for botao in (
                self.alternativas[
                    escolhida
                ]
            ):

                botao.errado()


            self.feedback.text = (
                "RESPOSTA INCORRETA\n"
                "Correta: "
                + resultado[
                    "resposta_correta"
                ]
            )


        self.botao_proxima.disabled = False
        self.botao_proxima.opacity = 1


    # ==================================================
    # DICA
    # ==================================================

    def mostrar_dica(
        self,
        *args
    ):

        pergunta = (
            self.controlador
            .pergunta_atual()
        )


        if pergunta is None:

            return


        mostrar_aviso(
            "Dica",

            pergunta[
                "dica"
            ]
        )


    # ==================================================
    # PRÓXIMA
    # ==================================================

    def proxima(
        self,
        *args
    ):

        modo = (
            self.controlador
            .modo
        )

        livro_atual = (
            self.controlador
            .nome_livro_sessao
        )


        resultado = (
            self.controlador
            .proxima_pergunta()
        )


        estado = (
            resultado[
                "estado"
            ]
        )


        # ==============================================
        # PRÓXIMA PERGUNTA
        # ==============================================

        if estado == "proxima_pergunta":

            if (
                modo == "livro"
                and livro_atual
            ):

                numero = (
                    self.controlador
                    .motor
                    .pergunta_atual()[
                        "numero"
                    ]
                )

                self.estado_jornada.salvar_posicao(
                    livro_atual,
                    numero
                )


            self.atualizar()

            return


        # ==============================================
        # LIVRO CONCLUÍDO
        # ==============================================

        if estado == "livro_concluido":

            recompensa = (
                resultado[
                    "recompensa"
                ]
            )


            self.estado_jornada.proximo_livro(
                livro_atual
            )


            texto = (
                recompensa[
                    "mensagem"
                ]
                + "\n\n"
                + recompensa[
                    "estrelas_texto"
                ]
                + "\n"
                + recompensa[
                    "selo"
                ]
            )


            self.popup_resultado(
                "Livro concluído!",
                texto
            )

            return


        # ==============================================
        # REVISÃO CONCLUÍDA
        # ==============================================

        if estado == "revisao_concluida":

            texto = (
                "Revisão concluída!\n\n"
                f'Acertos: {resultado["acertos"]}\n'
                f'Erros: {resultado["erros"]}\n\n'
                f'Perguntas ainda pendentes: '
                f'{resultado["pendentes"]}'
            )


            self.popup_resultado(
                "Perguntas que errei",
                texto
            )

            return


        # ==============================================
        # DESAFIO DIÁRIO CONCLUÍDO
        # ==============================================

        if estado == "desafio_concluido":

            dados = (
                resultado[
                    "resultado"
                ]
            )


            texto = (
                "Desafio Diário concluído!\n\n"
                f'Acertos: {resultado["acertos"]}/10\n'
                f'Erros: {resultado["erros"]}\n'
                f'Aproveitamento: '
                f'{dados["percentual"]}%'
            )


            self.popup_resultado(
                "Desafio Diário",
                texto
            )

            return


    def popup_resultado(
        self,
        titulo,
        texto
    ):

        caixa = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12)
        )


        mensagem = Label(
            text=texto,
            color=BRANCO,
            font_size="17sp",
            halign="center",
            valign="middle"
        )


        mensagem.bind(
            size=lambda obj, valor:
            setattr(
                obj,
                "text_size",
                (
                    valor[0] - dp(20),
                    None
                )
            )
        )


        caixa.add_widget(
            mensagem
        )


        fechar = Botao3D(
            text="CONTINUAR",
            size_hint_y=None,
            height=dp(58)
        )


        caixa.add_widget(
            fechar
        )


        popup = Popup(
            title=titulo,
            content=caixa,
            size_hint=(
                0.90,
                0.60
            ),
            auto_dismiss=False
        )


        fechar.bind(
            on_release=
                lambda *_:
                self.fechar_conclusao(
                    popup
                )
        )


        popup.open()


    def fechar_conclusao(
        self,
        popup
    ):

        popup.dismiss()

        self.manager.current = (
            "inicio"
        )




# ======================================================
# PROGRESSO
# ======================================================

class TelaProgresso(Screen):

    def __init__(
        self,
        controlador,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.controlador = controlador

        aplicar_fundo_anil(
            self
        )


        raiz = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(14)
        )


        voltar = Botao3D(
            text="VOLTAR",
            size_hint_y=None,
            height=dp(55)
        )


        voltar.bind(
            on_release=
                lambda *_:
                setattr(
                    self.manager,
                    "current",
                    "inicio"
                )
        )


        raiz.add_widget(
            voltar
        )


        raiz.add_widget(
            label_branco(
                "MEU PROGRESSO",
                "25sp",
                58,
                True
            )
        )


        painel = Bloco3D(
            orientation="vertical",
            padding=dp(20)
        )


        self.texto = Label(
            text="",
            color=BRANCO,
            font_size="18sp",
            halign="left",
            valign="middle"
        )


        self.texto.bind(
            size=lambda obj, valor:
            setattr(
                obj,
                "text_size",
                (
                    valor[0] - dp(20),
                    None
                )
            )
        )


        painel.add_widget(
            self.texto
        )

        raiz.add_widget(
            painel
        )

        self.add_widget(
            raiz
        )


    def on_pre_enter(
        self,
        *args
    ):

        r = (
            self.controlador
            .meu_progresso()
        )


        self.texto.text = (
            f'JOGADOR\n{r["jogador"]}\n\n'
            f'XP: {r["xp"]}\n'
            f'MOEDAS: {r["moedas"]}\n\n'
            f'LIVROS: {r["livros_concluidos"]}/66\n\n'
            f'PERGUNTAS APRENDIDAS: '
            f'{r["perguntas_aprendidas"]}/1980\n\n'
            f'PARA REVISAR: '
            f'{r["perguntas_para_revisar"]}\n\n'
            f'ACERTOS: {r["acertos"]}\n'
            f'ERROS: {r["erros"]}\n\n'
            f'SEQUÊNCIA: '
            f'{r["sequencia_atual"]} DIA(S)'
        )



# ======================================================
# CONQUISTAS
# ======================================================

class TelaConquistas(Screen):

    def __init__(
        self,
        controlador,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.controlador = controlador

        aplicar_fundo_anil(
            self
        )


        raiz = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(10)
        )


        # ----------------------------------------------
        # VOLTAR
        # ----------------------------------------------

        voltar = Botao3D(
            text="VOLTAR",
            size_hint_y=None,
            height=dp(54)
        )


        voltar.bind(
            on_release=
                lambda *_:
                setattr(
                    self.manager,
                    "current",
                    "inicio"
                )
        )


        raiz.add_widget(
            voltar
        )


        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        raiz.add_widget(
            label_branco(
                "CONQUISTAS",
                "25sp",
                50,
                True
            )
        )


        self.resumo = label_branco(
            "",
            "15sp",
            38,
            True
        )


        raiz.add_widget(
            self.resumo
        )


        # ----------------------------------------------
        # LISTA
        # ----------------------------------------------

        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(10),
            scroll_type=[
                "content",
                "bars"
            ]
        )


        self.grade = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(4),
            size_hint_y=None
        )


        self.grade.bind(
            minimum_height=
                self.grade.setter(
                    "height"
                )
        )


        scroll.add_widget(
            self.grade
        )


        raiz.add_widget(
            scroll
        )


        self.add_widget(
            raiz
        )


    # ==================================================
    # ATUALIZAR AO ENTRAR
    # ==================================================

    def on_pre_enter(
        self,
        *args
    ):

        self.montar()


    # ==================================================
    # MONTAR OS 66 LIVROS
    # ==================================================

    def montar(self):

        self.grade.clear_widgets()


        livros = (
            self.controlador
            .motor
            .listar_livros()
        )


        dados_livros = (
            self.controlador
            .progresso
            .dados
            .get(
                "livros",
                {}
            )
        )


        concluidos = sum(
            1
            for nome in livros
            if dados_livros
            .get(
                nome,
                {}
            )
            .get(
                "concluido",
                False
            )
        )


        self.resumo.text = (
            f"{concluidos}/66 "
            "LIVROS CONCLUÍDOS"
        )


        for numero, livro in enumerate(
            livros,
            start=1
        ):

            dados = (
                dados_livros
                .get(
                    livro,
                    {}
                )
            )


            concluido = (
                dados.get(
                    "concluido",
                    False
                )
            )


            # ==========================================
            # LIVRO CONCLUÍDO
            # ==========================================

            if concluido:

                melhor = int(
                    dados.get(
                        "melhor_acertos",
                        0
                    )
                )


                recompensa = (
                    Recompensas
                    .montar_recompensa(
                        self.controlador
                        .nome_jogador(),

                        livro,

                        melhor
                    )
                )


                botao = Botao3D(
                    text=(
                        f"{numero}. {livro}\n"
                        f'{recompensa["selo"]}\n'
                        f'ESTRELAS: '
                        f'{recompensa["estrelas"]}/3'
                        f'   •   MELHOR: '
                        f'{melhor}/30'
                    ),

                    size_hint_y=None,
                    height=dp(94)
                )


                botao.font_size = "15sp"


                botao.bind(
                    on_release=
                        lambda obj,
                        r=recompensa:
                        self.abrir_pergaminho(
                            r
                        )
                )


            # ==========================================
            # LIVRO NÃO CONCLUÍDO
            # ==========================================

            else:

                botao = Botao3D(
                    text=(
                        f"{numero}. {livro}\n"
                        "BLOQUEADO"
                    ),

                    size_hint_y=None,
                    height=dp(72)
                )


                botao.disabled = True
                botao.opacity = 0.55


            self.grade.add_widget(
                botao
            )


    # ==================================================
    # PERGAMINHO
    # ==================================================

    def abrir_pergaminho(
        self,
        recompensa
    ):

        caixa = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(12)
        )


        scroll = ScrollView(
            do_scroll_x=False
        )


        texto = (
            recompensa[
                "pergaminho"
            ][
                "texto"
            ]
            + "\n\n"
            + recompensa[
                "mensagem"
            ]
        )


        label = Label(
            text=texto,
            color=BRANCO,
            font_size="17sp",
            halign="center",
            valign="top",
            size_hint_y=None
        )


        label.bind(
            width=lambda obj, valor:
            setattr(
                obj,
                "text_size",
                (
                    valor - dp(20),
                    None
                )
            )
        )


        label.bind(
            texture_size=lambda obj, valor:
            setattr(
                obj,
                "height",
                valor[1] + dp(30)
            )
        )


        scroll.add_widget(
            label
        )


        caixa.add_widget(
            scroll
        )


        fechar = Botao3D(
            text="FECHAR",
            size_hint_y=None,
            height=dp(58)
        )


        caixa.add_widget(
            fechar
        )


        popup = Popup(
            title="PERGAMINHO DE CONQUISTA",
            content=caixa,
            size_hint=(
                0.92,
                0.78
            ),
            auto_dismiss=False
        )


        fechar.bind(
            on_release=
                popup.dismiss
        )


        popup.open()


# ======================================================
# APP
# ======================================================

class JornadaBiblicaApp(App):

    def build(self):

        self.title = "Kiss"


        controlador = (
            ControladorJornada()
        )


        estado_jornada = (
            EstadoJornada(
                controlador.progresso,
                controlador.motor.listar_livros()
            )
        )


        gerente = ScreenManager()


        gerente.add_widget(
            TelaNome(
                controlador,
                name="nome"
            )
        )


        gerente.add_widget(
            TelaInicio(
                controlador,
                estado_jornada,
                name="inicio"
            )
        )


        gerente.add_widget(
            TelaLivros(
                controlador,
                estado_jornada,
                name="livros"
            )
        )


        gerente.add_widget(
            TelaPergunta(
                controlador,
                estado_jornada,
                name="pergunta"
            )
        )


        gerente.add_widget(
            TelaProgresso(
                controlador,
                name="progresso"
            )
        )


        gerente.add_widget(
            TelaConquistas(
                controlador,
                name="conquistas"
            )
        )


        if (
            controlador
            .progresso
            .jogador_tem_nome()
        ):

            gerente.current = (
                "inicio"
            )

        else:

            gerente.current = (
                "nome"
            )


        return gerente
