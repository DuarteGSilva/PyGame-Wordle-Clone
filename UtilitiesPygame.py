import pygame
from pygame.locals import *
from os import PathLike
from typing import Union, Callable, Any, Iterable, Mapping, Optional, IO, Type

__all__ = ('Button', 'ScrollButton', 'TextButton', 'Text', 'Interface')
# version = 1.1


class Text(object):
    def __init__(self,
                 superficie: pygame.Surface,
                 cor: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] = 0,
                 tamanho: int = 26,
                 texto: str = None,
                 coords: Union[list[int, int], list[float, float],
                               tuple[int, int], tuple[float, float], pygame.Vector2] = None,
                 fonte: Union[str, bytes, PathLike[str], PathLike[bytes], IO] = 'freesansbold.ttf'
                 ) -> None:
        self.superficie = superficie
        if isinstance(cor, int):
            self.cor = (cor, cor, cor)
        else:
            self.cor = cor
        self.texto = texto
        self.coords = coords
        self.fonte = pygame.font.Font(fonte, tamanho)

    def text(self,
             texto: str = None,
             coords: Union[list[int, int], list[float, float],
                           tuple[int, int], tuple[float, float], pygame.Vector2] = None,
             cor: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] = None,
             ) -> None:
        if self.texto is None and texto is None:
            raise ValueError("Missing Value: text")
        elif texto is None:
            texto = self.texto
        if self.coords is None and coords is None:
            raise ValueError("Missing Value: Coords")
        elif coords is None:
            coords = self.coords
        if self.cor is None and cor is None:
            raise ValueError("Missing Value: Cor")
        elif cor is None:
            cor = self.cor
        else:
            if isinstance(cor, int):
                cor = (cor, cor, cor)
        self.superficie.blit(self.fonte.render(texto, True, cor), coords)



"""
BUTTON USAGE:

gameloop:
    # first init 
    Button.init()

    # then .button/.box
    text_box.box(events)
    but.button()

    # finally click_event()
    Button.click_event(events)
    ...
"""
class Button(object):
    """
    classe para fácilmente construir botões para pygame

    informações / instruções de uso da classe Button
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                                                                         ║
    ║ Para utilizar esta classe deve ser chamado o 'Button.init()' no início  ║
    ║ do loop de jogo da página em que se pretende renderizar os botões e     ║
    ║ depois chamar cada objeto Button depois de criado e atribuído a uma     ║
    ║ variável [b = Button('args')] na forma 'b.button()', e o botão será     ║
    ║ renderizado e selecionável. Para acionar a função evento quando este    ║
    ║ for pressionado pode usar-se uma de três maneiras, o método de classe   ║
    ║ [Button.click_event()] que verifica se algum dos botões renderizados é  ║
    ║ pressionado e ativa o respetivo evento, um dos métodos de instância     ║
    ║ [b.click() ou b.self_click_event()] que fazem o mesmo mas apenas para o ║
    ║ próprio, com ou sem o loop de enventos para ser assim possível defenir  ║
    ║ outras maneiras de ativar o botão sem ser com um clique do botão do rato║
    ║ ou de forma manual, detetando se o botão em específico está selecionado ║
    ║ [utilizando o método '__bool__'] e escrevendo depois o evento que será  ║
    ║ acionado [ex.: if b: / pause = False], isto é util para eventos simples ║
    ║ para que não seja necessário defenir uma função para o 'b.evento()'     ║
    ║ NOTA: O método .click() e o __bool__ têm de ser chamados dentro de um   ║
    ║ loop de eventos do pygame [for e in pygame.event.get()], e para os      ║
    ║ restantes tem de ser passada uma variável correspondente a 'pygame.event║
    ║ .get()'. Qualquer dúvida consulte as respetivas docstrings/help(classe) ║
    ║                                                                         ║
    ║ Os objetos botão podem ser costumizados de diversas maneiras, desde a   ║
    ║ cor ao formato e até é possível criar botões com imagens em vez de      ║
    ║ 'pygame.draw.Rect's, o método '__init__' é muito complexo, sendo com    ║
    ║ este possível defenir uma enorme variedade de características do botão, ║
    ║ no entanto a maior parte delas pode ser mudada a qualquer altura        ║
    ║ acedendo a cada uma como uma variável normal [ex.: b.texto = 'x'].      ║
    ║                                                                         ║
    ║ Qualquer outra dúvida que surja será provavelmente exclarecida nos      ║
    ║ docstrings de cada método desta classe [especialmente no '__init__'].   ║
    ║                                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    """
    mousex = 0.0
    mousey = 0.0
    select = 0
    listed = []

    def __init__(self,
                 superficie: pygame.Surface,
                 coords: Union[list[int, int], list[float, float],
                               tuple[int, int], tuple[float, float], pygame.Vector2],
                 texto: str = None,
                 tamanho_rect: Union[list[int, int], tuple[int, int], int,
                                     list[float, float], tuple[float, float], float] = None,
                 tamanho_texto: int = 26,
                 cor_texto: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] = 0,
                 cor_select: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str, None] = 100,
                 cor_fundo: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] = None,
                 arredondamento: int = -1,
                 select_transparente: int = 0,
                 imagem: pygame.Surface = None,
                 imagem_fundo: pygame.Surface = None,
                 img_select_incr: float = 1.10,
                 evento: Callable[..., Any] = None,
                 args: Iterable[Any] = (),
                 kwargs: Mapping[str, Any] = None,
                 fonte: Union[str, bytes, PathLike[str], PathLike[bytes], IO] = 'freesansbold.ttf',
                 custom_properties: Optional[Any] = None
                 ) -> None:
        """
        Construtor de objetos botão

        :param superficie: superfície do pygame onde renderizar o botão
        :param coords: coordenadas do canto superior esquerdo do botão
        :param texto: texto escrito dentro do botão (se omitido em conjunto com 'tamanho_rect' o botão ficará um
                      quadrado com lado = self.rect[0] ou self.tamanho_texto*(3/2))
        :param tamanho_rect: largura e altura do retângulo, se a altura for omitida irá ser igual a tamanho_texto*(3/2)
                             e se for omitido na sua totalidade, será calculado em relação ao texto
        :param tamanho_texto: altura da fonte 'freesansbold.ttf'
        :param cor_texto: cor do texto, se indicada apenas como um valor 'int' o construtor irá transformá-lo numa lista
                          com três valores iguais ao valor indicado
        :param cor_select: cor do retângulo desenhado quando o botão está selecionado, se for 'None' não é desenhado, se
                           indicada apenas como um valor 'int' o construtor irá transformá-lo numa lista com três
                           valores iguais ao valor indicado
        :param cor_fundo: cor do retângulo desenhado quando o butão não está selecionado, se indicada apenas como um
                         valor 'int' o construtor irá transformá-lo numa lista com três valores iguais ao valor indicado
        :param arredondamento: quantos pixeis de arredondamento nos cantos do botão
        :param imagem: imagem renderizada por cima do botão, ou se imagem_fundo não for 'None', a imagem é renderizada
                       em vez da imagem_fundo quando o botão está selecionado
        :param imagem_fundo: se não for 'None' vai substituir o retângulo de fundo e select por esta
        :param img_select_incr: fator de aumento de tamanho da imagem quando o botão estiver selecionado
        :param evento: função executada ao carregar no botão (com init 1) (se omitida nada acontece)
        :param args: argumentos passados para a função evento()
        :param kwargs: argumentos keyword passados para a função evento()
        """
        self.id = id(self)
        self.superficie = superficie
        self.coords = coords
        self.texto = texto
        self.tamanho_texto = tamanho_texto
        self.fonte = pygame.font.Font(fonte, tamanho_texto)
        if isinstance(cor_texto, int):
            self.cor_texto = (cor_texto, cor_texto, cor_texto)
        else:
            self.cor_texto = cor_texto
        if isinstance(cor_select, int):
            self.cor_select = (cor_select, cor_select, cor_select)
        else:
            self.cor_select = cor_select
        if isinstance(cor_fundo, int):
            self.cor_fundo = (cor_fundo, cor_fundo, cor_fundo)
        else:
            self.cor_fundo = cor_fundo
        self.event = evento
        self.coords_texto = (int(coords[0] + tamanho_texto * (1 / 4) + tamanho_texto // 10),
                             int(coords[1] + tamanho_texto * (1 / 4)))
        if texto is None and tamanho_rect is None and imagem_fundo is None:
            self.rect = (tamanho_texto * (3 / 2), tamanho_texto * (3 / 2))
        elif tamanho_rect is None and imagem_fundo is None:
            textoX = pygame.font.Font('freesansbold.ttf', tamanho_texto).size(texto)[0]
            self.rect = (textoX + (tamanho_texto * (1 / 4) + tamanho_texto // 10) * 2, tamanho_texto * (3 / 2))
        elif tamanho_rect is None and imagem_fundo is not None:
            self.rect = None
        elif isinstance(tamanho_rect, (list, tuple)):
            self.rect = tamanho_rect
            self.coords_texto = (int(coords[0] + tamanho_texto * (1 / 4) + tamanho_texto // 10),
                                 int(coords[1] + tamanho_rect[1] / 2 - tamanho_texto * (1 / 2)))
        else:
            self.rect = (tamanho_rect, tamanho_texto * (3 / 2))
        self.arredondamento = arredondamento
        Button.listed.append(self)
        self.args = args
        if kwargs is None:
            self.kwargs = {}
        else:
            self.kwargs = kwargs
        self.imagem = imagem
        if self.imagem is not None:
            self.img_rect = self.imagem.get_rect()
        if imagem_fundo is not None:
            if self.rect is None:
                self.rect = (imagem_fundo.get_width(), imagem_fundo.get_height())
            self._imagem_fundo = pygame.transform.smoothscale(imagem_fundo,
                                                              (int(self.rect[0]), int(self.rect[1]))).convert_alpha()
            self._imagem_fundo_select = pygame.transform.smoothscale(imagem_fundo,
                                                                     (int(self.rect[0] * img_select_incr),
                                                                      int(self.rect[1] * img_select_incr))
                                                                     ).convert_alpha()
        else:
            self._imagem_fundo = None
            self._imagem_fundo_select = None
        self.select_coords = (self.coords[0] - (((self.rect[0] * img_select_incr) - self.rect[0]) / 2),
                              self.coords[1] - (((self.rect[1] * img_select_incr) - self.rect[1]) / 2))
        self.img_select_incr = img_select_incr
        if select_transparente:
            self.superficie_select = pygame.Surface(self.rect)
            self.superficie_select.set_alpha(select_transparente)
            self.superficie_select.fill(self.cor_select)
        else:
            self.superficie_select = None
        self.custom = custom_properties
        # propriedades customizadas dadas pelo utilizador (pode ser usado para distinguir botões)
        self._tipo = 0

    @classmethod
    def init(cls) -> None:
        """
        método de classe iniciador para a classe Botão,
        tem de ser chamado no início do 'while loop' onde se renderizam os botões, se não os botões não funcionam
        """
        cls.mousex, cls.mousey = pygame.mouse.get_pos()
        cls.select = 0

    @classmethod
    def click_event(cls,
                    eventos: list[pygame.event.Event],
                    customargs: Iterable[Any] = None,
                    customkwargs: Mapping[str, Any] = None,
                    botao: Optional[int] = 1
                    ) -> None:
        """
        método de classe que deteta se algum botão foi carregado e ativa o evento correspondente, da return 'None'

        :param botao: botão do rato (event.button) necessário de se carregar para ativar os eventos, se for 'None'
                     qualquer botão do rato funciona
        :param eventos: variável correspondente a pygame.event.get()
        :param customargs: argumentos customizados passados para a função evento(), se igual a 'None' são usados os
                          self.args dados no construtor do objeto
        :param customkwargs: argumentos keyword customizados passados para a função evento(), se igual a 'None' são
                            usados os self.kwargs dados no construtor do objeto
        """
        if botao is not None:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == botao:
                        for b in cls.listed:
                            if b._tipo == 0:
                                b.click(customargs, customkwargs)
        else:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    for b in cls.listed:
                        if b._tipo == 0:
                            b.click(customargs, customkwargs)

    def instance_click_event(self,
                             eventos: list[pygame.event.Event],
                             customargs: Iterable[Any] = None,
                             customkwargs: Mapping[str, Any] = None,
                             botao: Optional[int] = 1
                             ) -> Any:
        """
        método de instância que deteta se este botão foi carregado e ativa o evento correspondente

        :param botao: botão do rato (event.button) necessário de se carregar para ativar os eventos, se for 'None'
                     qualquer botão do rato funciona
        :param eventos: variável correspondente a pygame.event.get()
        :param customargs: argumentos customizados passados para a função evento(), se igual a 'None' são usados os
                          self.args dados no construtor do objeto
        :param customkwargs: argumentos keyword customizados passados para a função evento(), se igual a 'None' são
                            usados os self.kwargs dados no construtor do objeto
        :returns: o que a função evento da instância der return
        """
        if botao is not None:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        return self.click(customargs, customkwargs)
        else:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    return self.click(customargs, customkwargs)

    def _detect(self) -> None:
        """
        deteta se o cursor do rato está a selecionar o botão
        """
        if self.coords[0] <= Button.mousex <= self.coords[0] + self.rect[0] and \
                self.coords[1] <= Button.mousey <= self.coords[1] + self.rect[1]:
            Button.select = self.id

    def _render(self) -> None:
        """
        renderiza o botão
        """
        if self:
            if self.superficie_select is not None:
                self.superficie.blit(self.superficie_select, self.coords)
            elif self._imagem_fundo is not None and self.imagem is not None:
                self.img_rect.center = (
                    int(self.coords[0]) + self.rect[0] // 2, int(self.coords[1]) + self.rect[1] // 2)
                self.superficie.blit(self.imagem, self.img_rect)
            elif self._imagem_fundo_select is not None:
                self.superficie.blit(self._imagem_fundo_select, self.select_coords)
            elif self.cor_select is not None:
                pygame.draw.rect(self.superficie, self.cor_select,
                                 (int(self.coords[0]), int(self.coords[1]), int(self.rect[0]), int(self.rect[1])),
                                 border_radius=self.arredondamento)
        else:
            if self._imagem_fundo is not None:
                self.superficie.blit(self._imagem_fundo, self.coords)
            elif self.cor_fundo is not None:
                pygame.draw.rect(self.superficie, self.cor_fundo,
                                 (int(self.coords[0]), int(self.coords[1]), int(self.rect[0]), int(self.rect[1])),
                                 border_radius=self.arredondamento)
        if self.imagem is not None and self._imagem_fundo is None:
            self.img_rect.center = (int(self.coords[0]) + self.rect[0] // 2, int(self.coords[1]) + self.rect[1] // 2)
            self.superficie.blit(self.imagem, self.img_rect)
        if self.texto is not None:
            self.superficie.blit(self.fonte.render(self.texto, True, self.cor_texto), self.coords_texto)

    def click(self,
              customargs: Iterable[Any] = None,
              customkwargs: Mapping[str, Any] = None) -> Any:
        """
        tenta acionar a função evento se o botão estiver selecionado, não faz nada se esta não existir

        :param customargs: argumentos customizados passados para a função evento(), se igual a 'None' são usados os
                          self.args dados no construtor do objeto
        :param customkwargs: argumentos keyword customizados passados para a função evento(), se igual a 'None' são
                            usados os self.kwargs dados no construtor do objeto
        :returns: o que a função evento da instância der return
        """
        if customargs is not None:
            args = customargs
        else:
            args = self.args
        if customkwargs is not None:
            kwargs = customkwargs
        else:
            kwargs = self.kwargs
        if self.event is not None:
            if self:
                return self.event(*args, **kwargs)

    def button(self) -> None:
        """
        renderiza e deteta se o botão está selecionado
        """
        self._detect()
        self._render()

    def __bool__(self) -> bool:
        """
        verifica se o botão está selecionado utilizando o valor bool do objeto (ex.: if my_button: / pause = False)

        :returns: True se estiver / False se não estiver
        """
        if Button.select == self.id:
            return True
        return False

    def change_image(self,
                     nova_imagem_fundo: pygame.Surface = None,
                     img_select_incr: Optional[float] = 1.10,
                     mudar_rect: bool = False) -> None:
        """
        muda a _imagem_fundo para uma nova e com um novo fator de aumento de tamanho quando selecionada

        :param nova_imagem_fundo: nova imagem de fundo, se for 'None' irá apenas mudar o fator de aumento de tamanho
        :param img_select_incr: fator de aumento de tamanho da imagem quando o botão estiver selecionado, se for 'None'
                                limpa a imagem de fundo
        :param mudar_rect: se True então o tamanho do botão vai ser ajustado ao tamanho da nova imagem
        """
        if img_select_incr is not None:
            self.img_select_incr = img_select_incr
            if nova_imagem_fundo is not None:
                if mudar_rect:
                    self.rect = (nova_imagem_fundo.get_width(), nova_imagem_fundo.get_height())
                self._imagem_fundo = pygame.transform.smoothscale(nova_imagem_fundo,
                                                                  (int(self.rect[0]),
                                                                   int(self.rect[1]))
                                                                  ).convert_alpha()
                self._imagem_fundo_select = \
                    pygame.transform.smoothscale(nova_imagem_fundo,
                                                 (int(self.rect[0] * img_select_incr),
                                                  int(self.rect[1] * img_select_incr))
                                                 ).convert_alpha()
            else:
                self._imagem_fundo = pygame.transform.smoothscale(self._imagem_fundo,
                                                                  (int(self.rect[0]),
                                                                   int(self.rect[1]))
                                                                  ).convert_alpha()
                self._imagem_fundo_select = pygame.transform.smoothscale(self._imagem_fundo,
                                                                         (int(self.rect[0] * img_select_incr),
                                                                          int(self.rect[1] * img_select_incr))
                                                                         ).convert_alpha()
            self.select_coords = (self.coords[0] - (((self.rect[0] * img_select_incr) - self.rect[0]) / 2),
                                  self.coords[1] - (((self.rect[1] * img_select_incr) - self.rect[1]) / 2))
        else:
            self._imagem_fundo = None
            self._imagem_fundo_select = None

    def center(self, x, y):
        """
        método para centrar o botão num ponto

        :param x: coordenada x
        :param y: coordenada y
        :returns: self (Button object)
        """
        self.coords = (x - (self.rect[0] / 2), y - (self.rect[1] / 2))
        self.select_coords = (self.coords[0] - (((self.rect[0] * self.img_select_incr) - self.rect[0]) / 2),
                              self.coords[1] - (((self.rect[1] * self.img_select_incr) - self.rect[1]) / 2))
        self.coords_texto = (int(self.coords[0] + self.tamanho_texto * (1 / 4) + self.tamanho_texto // 10),
                             int(self.coords[1] + self.rect[1] / 2 - self.tamanho_texto * (1 / 2)))
        return self


class ScrollButton(Button):
    def __init__(self,
                 superficie: pygame.Surface,
                 coords: Union[list[int, int], list[float, float],
                               tuple[int, int], tuple[float, float], pygame.Vector2],
                 texto: str = None,
                 tamanho_rect: Union[list[int, int], tuple[int, int], int,
                                     list[float, float], tuple[float, float], float] = None,
                 tamanho_texto: int = 26,
                 cor_texto: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] = 0,
                 cor_select: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str, None] = 100,
                 cor_fundo: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] = 80,
                 cor_inRect: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] =
                 (80, 160, 180),
                 arredondamento: int = -1,
                 evento: Callable[..., Any] = None,
                 args: Iterable[Any] = (),
                 kwargs: Mapping[str, Any] = None,
                 fonte: Union[str, bytes, PathLike[str], PathLike[bytes], IO] = 'freesansbold.ttf',
                 in_rect_reduc: float = 0.05,
                 min_val: Union[int, float] = 0,
                 max_val: Union[int, float] = 100,
                 custom_properties: Optional[Any] = None
                 ) -> None:
        self.texto_ = texto
        texto = f"{texto} {str(max_val)}"
        super(ScrollButton, self).__init__(superficie, coords, texto, tamanho_rect, tamanho_texto, cor_texto,
                                           cor_select, cor_fundo, arredondamento, 0, None, None, 1.10, evento,
                                           args, kwargs, fonte, custom_properties)
        self.agarrado = False
        self.min_val = min_val
        self.max_val = max_val
        if min_val == 0 and max_val == 100:
            self.changed_range = False
        else:
            self.changed_range = True
        self.value = min_val
        self.texto = f"{texto} {str(max_val)}"
        self.inRectReduc = in_rect_reduc
        self.inRectX = 0
        if isinstance(cor_inRect, int):
            self.cor_inRect = (cor_inRect, cor_inRect, cor_inRect)
        else:
            self.cor_inRect = cor_inRect
        self._tipo = 1

    @classmethod
    def click_event(cls,
                    eventos: list[pygame.event.Event],
                    customargs: Iterable[Any] = None,
                    customkwargs: Mapping[str, Any] = None,
                    botao: Optional[int] = 1
                    ) -> None:
        """
        método de classe que deteta se algum botão foi carregado e ativa o evento correspondente, da return 'None'

        :param botao: botão do rato (event.button) necessário de se carregar para ativar os eventos, se for 'None'
                     qualquer botão do rato funciona
        :param eventos: variável correspondente a pygame.event.get()
        :param customargs: argumentos customizados passados para a função evento(), se igual a 'None' são usados os
                          self.args dados no construtor do objeto
        :param customkwargs: argumentos keyword customizados passados para a função evento(), se igual a 'None' são
                            usados os self.kwargs dados no construtor do objeto
        """
        if botao is not None:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == botao:
                        for b in cls.listed:
                            if b:
                                b.agarrado = True
                if e.type == MOUSEBUTTONUP:
                    if e.button == botao:
                        for b in cls.listed:
                            b.agarrado = False
        else:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    for b in cls.listed:
                        if b:
                            b.agarrado = True
                if e.type == MOUSEBUTTONUP:
                    for b in cls.listed:
                        b.agarrado = False

    def click(self,
              customargs: Iterable[Any] = None,
              customkwargs: Mapping[str, Any] = None) -> Any:
        """
        tenta acionar a função evento se o botão estiver selecionado, não faz nada se esta não existir

        :param customargs: argumentos customizados passados para a função evento(), se igual a 'None' são usados os
                          self.args dados no construtor do objeto
        :param customkwargs: argumentos keyword customizados passados para a função evento(), se igual a 'None' são
                            usados os self.kwargs dados no construtor do objeto
        :returns: o que a função evento da instância der return
        """
        if customargs is not None:
            args = customargs
        else:
            args = self.args
        if customkwargs is not None:
            kwargs = customkwargs
        else:
            kwargs = self.kwargs
        if self.event is not None:
            return self.event(self.value, *args, **kwargs)

    def button(self):
        if self.agarrado:
            Button.select = self.id
        self._detect()
        rect_reduc = min(self.rect[0] * self.inRectReduc, self.rect[1] * self.inRectReduc)
        if self.agarrado:
            if rect_reduc >= (Button.mousex - self.coords[0]):
                self.inRectX = rect_reduc
            elif (Button.mousex - self.coords[0]) >= self.rect[0] - rect_reduc:
                self.inRectX = self.rect[0] - rect_reduc
            else:
                self.inRectX = Button.mousex - self.coords[0]
            if not self.changed_range:
                self.value = round((self.inRectX - rect_reduc) * (1 / (self.rect[0] - (rect_reduc * 2))), 2) * 100
            else:
                old_value = round((self.inRectX - rect_reduc) * (1 / (self.rect[0] - (rect_reduc * 2))), 2) * 100
                self.value = (old_value * (self.max_val - self.min_val)) / 100 + self.min_val
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        self.texto = f"{self.texto_} {str(round(self.value))}"
        self.click()
        if self:
            pygame.draw.rect(self.superficie, self.cor_select,
                             (int(self.coords[0]), int(self.coords[1]), int(self.rect[0]), int(self.rect[1])),
                             border_radius=self.arredondamento)
        else:
            pygame.draw.rect(self.superficie, self.cor_fundo,
                             (int(self.coords[0]), int(self.coords[1]), int(self.rect[0]), int(self.rect[1])),
                             border_radius=self.arredondamento)
        rect_reduc = round(rect_reduc)
        pygame.draw.rect(self.superficie, self.cor_inRect,
                         (self.coords[0] + rect_reduc, self.coords[1] + rect_reduc,
                          int(self.inRectX - rect_reduc), self.rect[1] - (rect_reduc * 2)),
                         border_radius=self.arredondamento)
        self.superficie.blit(self.fonte.render(self.texto, True, self.cor_texto), self.coords_texto)

    def starting_value(self, value: Union[int, float]):
        if self.min_val <= value <= self.max_val:
            self.value = value
            rect_reduc = min(self.rect[0] * self.inRectReduc, self.rect[1] * self.inRectReduc)
            if not self.changed_range:
                self.inRectX = (value / 100) * (self.rect[0] - (rect_reduc * 2)) + rect_reduc
            else:
                old_value = ((self.value - self.min_val) * 100) / (self.max_val - self.min_val)
                self.inRectX = (old_value / 100) * (self.rect[0] - (rect_reduc * 2)) + rect_reduc
            return self
        else:
            raise ValueError("given value doesnt fit within specifiend interval for this button")

    def _render(self) -> None:
        """
        USED FOR OTHER BUTTON CLASSES ONLY
        """

    def change_image(self,
                     nova_imagem_fundo: pygame.Surface = None,
                     img_select_incr: Optional[float] = 1.10,
                     mudar_rect: bool = False) -> None:
        """
        USED FOR OTHER BUTTON CLASSES ONLY, This Button subclass doesnt support images yet
        """
        pass


class TextButton(Button):
    def __init__(self,
                 superficie: pygame.Surface,
                 clock: pygame.time.Clock,
                 coords: Union[list[int, int], list[float, float],
                               tuple[int, int], tuple[float, float], pygame.Vector2],
                 texto: str = "",
                 tamanho_rect: Union[list[int, int], tuple[int, int], int,
                                     list[float, float], tuple[float, float], float] = None,
                 tamanho_texto: int = 26,
                 cor_texto: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str] = 0,
                 cor_select: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str, None] = 100,
                 cor_fundo: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str, None] = 80,
                 cor_cursor: Union[list[int, int, int], tuple[int, int, int], pygame.color.Color, int, str, None] = 50,
                 arredondamento: int = -1,
                 evento: Callable[..., Any] = None,
                 args: Iterable[Any] = (),
                 kwargs: Mapping[str, Any] = None,
                 convert: type = None,
                 fonte: Union[str, bytes, PathLike[str], PathLike[bytes], IO] = 'freesansbold.ttf',
                 custom_properties: Optional[Any] = None
                 ) -> None:
        super().__init__(superficie, coords, texto, tamanho_rect, tamanho_texto, cor_texto, cor_select, cor_fundo,
                         arredondamento, 0, None, None, 1.10, evento, args, kwargs, fonte, custom_properties)
        self.clock = clock
        self.convert = convert
        self.selected = False
        self.force_select = False
        self.output = None
        self.old_texto = self.texto

        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = 400
        self.keyrepeat_interval_ms = 35

        # Things cursor:
        if isinstance(cor_cursor, int):
            self.cor_cursor = (cor_cursor, cor_cursor, cor_cursor)
        else:
            self.cor_cursor = cor_cursor

        self.cursor_surface = pygame.Surface((int(self.tamanho_texto / 20 + 1), self.tamanho_texto))
        self.cursor_surface.fill(self.cor_cursor)
        self.cursor_position = 0
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500
        self.cursor_ms_counter = 0

        self._tipo = 2

    @classmethod
    def click_event(cls,
                    eventos: list[pygame.event.Event],
                    customargs: Iterable[Any] = None,
                    customkwargs: Mapping[str, Any] = None,
                    botao: Optional[int] = 1
                    ) -> None:
        """
        método de classe que deteta se algum botão foi carregado e ativa o evento correspondente, da return 'None'

        :param botao: botão do rato (event.button) necessário de se carregar para ativar os eventos, se for 'None'
                     qualquer botão do rato funciona
        :param eventos: variável correspondente a pygame.event.get()
        :param customargs: argumentos customizados passados para a função evento(), se igual a 'None' são usados os
                          self.args dados no construtor do objeto
        :param customkwargs: argumentos keyword customizados passados para a função evento(), se igual a 'None' são
                            usados os self.kwargs dados no construtor do objeto
        """
        if botao is not None:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == botao:
                        for b in cls.listed:
                            if b._tipo == 2:
                                if b:
                                    b.selected = not b.selected
                                    b.cursor_position = len(b.texto)
                                else:
                                    b.selected = False
        else:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    for b in cls.listed:
                        if b._tipo == 2:
                            if b:
                                b.selected = not b.selected
                                b.cursor_position = len(b.texto)
                            else:
                                b.selected = False

    def instance_click_event(self,
                             eventos: list[pygame.event.Event],
                             customargs: Iterable[Any] = None,
                             customkwargs: Mapping[str, Any] = None,
                             botao: Optional[int] = 1
                             ) -> None:
        """
        método de classe que deteta se algum botão foi carregado e ativa o evento correspondente, da return 'None'

        :param botao: botão do rato (event.button) necessário de se carregar para ativar os eventos, se for 'None'
                     qualquer botão do rato funciona
        :param eventos: variável correspondente a pygame.event.get()
        :param customargs: argumentos customizados passados para a função evento(), se igual a 'None' são usados os
                          self.args dados no construtor do objeto
        :param customkwargs: argumentos keyword customizados passados para a função evento(), se igual a 'None' são
                            usados os self.kwargs dados no construtor do objeto
        """
        if botao is not None:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == botao:
                        if self:
                            self.selected = not self.selected
                            self.cursor_position = len(self.texto)
                        else:
                            self.selected = False
        else:
            for e in eventos:
                if e.type == MOUSEBUTTONDOWN:
                    if self:
                        self.selected = not self.selected
                        self.cursor_position = len(self.texto)
                    else:
                        self.selected = False

    def box(self, events: list[pygame.event.Event]) -> None:
        """
        rederiza a caixa de texto

        :param events: variável correspondente a pygame.event.get()
        """
        self._detect()
        if self or self.force_select:
            if self.force_select:
                self.force_select -= 1
            if self.cor_select is not None:
                pygame.draw.rect(self.superficie, self.cor_select,
                                 (int(self.coords[0]), int(self.coords[1]), int(self.rect[0]), int(self.rect[1])),
                                 border_radius=self.arredondamento)
        else:
            if self.cor_fundo is not None:
                pygame.draw.rect(self.superficie, self.cor_fundo,
                                 (int(self.coords[0]), int(self.coords[1]), int(self.rect[0]), int(self.rect[1])),
                                 border_radius=self.arredondamento)
        if self.texto is not None:
            self.superficie.blit(self.fonte.render(self.texto, True, self.cor_texto), self.coords_texto)

        if self.selected:
            for e in events:
                if e.type == KEYDOWN:
                    self.cursor_visible = True  # So the user sees where he writes

                    # If none exist, create counter for that key:
                    if e.key not in self.keyrepeat_counters:
                        if not (e.key == K_RETURN or e.key == K_ESCAPE):  # Filters out return key, others can be added
                            self.keyrepeat_counters[e.key] = [0, e.unicode]

                    if e.key == K_BACKSPACE:
                        self.texto = (
                                self.texto[:max(self.cursor_position - 1, 0)]
                                + self.texto[self.cursor_position:]
                        )

                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 0)
                    elif e.key == K_DELETE:
                        self.texto = (
                                self.texto[:self.cursor_position]
                                + self.texto[self.cursor_position + 1:]
                        )

                    elif e.key == K_RETURN:
                        if self.convert is not None:
                            try:
                                value = self.convert(self.texto)
                            except ValueError:
                                self.texto = self.old_texto
                                value = self.texto
                        else:
                            value = self.texto
                        if self.event is not None:
                            try:
                                self.output = self.event(value, *self.args, **self.kwargs)
                            except TypeError:
                                self.texto = self.old_texto
                                self.output = self.texto
                            except ValueError:
                                self.texto = self.old_texto
                                self.output = self.texto
                        else:
                            self.output = value
                        self.force_select = self.clock.get_fps() // 5
                        self.old_texto = self.texto
                        return self.output
                        # self.texto = ""
                        # self.cursor_position = 0

                    elif e.key == K_RIGHT:
                        # Add one to cursor_pos, but do not exceed len(input_string)
                        self.cursor_position = min(self.cursor_position + 1, len(self.texto))

                    elif e.key == K_LEFT:
                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 0)

                    elif e.key == K_UP:
                        pass
                        # if self.texto != self.old_texto:
                        #     self.texto_buffer = self.texto
                        #     self.texto = self.old_texto
                        #     self.cursor_position = len(self.texto)

                    elif e.key == K_DOWN:
                        pass
                        # if self.texto == self.old_texto:
                        #     self.texto = self.texto_buffer
                        #     self.cursor_position = len(self.texto)

                    elif e.key == K_END:
                        self.cursor_position = len(self.texto)

                    elif e.key == K_HOME:
                        self.cursor_position = 0

                    elif e.key == K_TAB:
                        pass

                    elif e.key == K_ESCAPE:
                        self.selected = False
                        break

                    elif self.fonte.size(self.texto + "m")[0] < \
                            self.rect[0] - (self.tamanho_texto * (1 / 4) + self.tamanho_texto // 10):
                        if e.unicode == "(":
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode
                                    + ")"
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)
                        elif e.unicode == '[':
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode
                                    + ']'
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)
                        elif e.unicode == '"' or e.unicode == "'":
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode * 2
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)
                        else:
                            # If no special key is pressed, add unicode of key to input_string
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)  # Some are empty, e.g. K_UP

                elif e.type == KEYUP:
                    # *** Because KEYUP doesn't include e.unicode, this dict is stored in such a weird way
                    if e.key in self.keyrepeat_counters:
                        del self.keyrepeat_counters[e.key]

            # Update key counters:
            for key in self.keyrepeat_counters:
                self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

                # Generate new key events if enough time has passed:
                if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                    self.keyrepeat_counters[key][0] = (
                            self.keyrepeat_intial_interval_ms
                            - self.keyrepeat_interval_ms
                    )

                    event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                    pygame.event.post(pygame.event.Event(KEYDOWN, key=event_key, unicode=event_unicode))

            # Update self.cursor_visible
            self.cursor_ms_counter += self.clock.get_time()
            if self.cursor_ms_counter >= self.cursor_switch_ms:
                self.cursor_ms_counter %= self.cursor_switch_ms
                self.cursor_visible = not self.cursor_visible

            if self.cursor_visible:
                cursor_x_pos = self.fonte.size(self.texto[:self.cursor_position])[0] + self.coords_texto[0]
                self.superficie.blit(self.cursor_surface, (cursor_x_pos, self.coords_texto[1]))

    def new_text(self, text):
        """
        Não alterar texto via self.text = "...", usar este método em vez disso
        :param text: novo texto
        :return: self
        """
        self.texto = text
        self.old_texto = text
        return self

    def _render(self) -> None:
        """
        USED FOR OTHER BUTTON CLASSES ONLY
        """
        pass

    def button(self) -> None:
        """
        USED FOR OTHER BUTTON CLASSES ONLY, for this one use box() method instead
        """
        pass

    def change_image(self,
                     nova_imagem_fundo: pygame.Surface = None,
                     img_select_incr: Optional[float] = 1.10,
                     mudar_rect: bool = False) -> None:
        """
        USED FOR OTHER BUTTON CLASSES ONLY, This Button subclass doesnt support images yet
        """
        pass


class Interface(object):
    def __init__(self,
                 superficie: pygame.Surface,
                 clock: pygame.time.Clock,
                 coords: Union[list[int, int], list[float, float],
                               tuple[int, int], tuple[float, float], pygame.Vector2],
                 tamanho_texto: int = 26,
                 *custom_commands: tuple[str, Optional[tuple[Type[Any], ...]], str]
                 ) -> None:
        self.superficie = superficie
        self.clock = clock
        self.coords = coords
        self.tamanho_texto = tamanho_texto
        self.rect = (self.superficie.get_width() - (coords[0] * 2), int(self.tamanho_texto * (3 / 2)))
        self.coords_texto = (int(coords[0] + tamanho_texto * (1 / 4) + tamanho_texto // 10),
                             int(coords[1] + self.rect[1] / 2 - tamanho_texto * (1 / 2)))
        fonte: Union[str, bytes, PathLike[str], PathLike[bytes], IO] = 'freesansbold.ttf'
        self.fonte = pygame.font.Font(fonte, tamanho_texto)
        self.fonte_nome = fonte

        self.rendered = False
        self.texto = ""
        self.output = ""
        self.old_texto = ""
        self.texto_buffer = ""
        self.tab_shortcut = "exec('')"
        self.tab_back = 2

        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = 400
        self.keyrepeat_interval_ms = 35

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.tamanho_texto / 20 + 1), self.tamanho_texto))
        self.cursor_surface.fill((100, 100, 100))
        self.cursor_position = 0
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500
        self.cursor_ms_counter = 0

        # comandos costumizados (tp e assim..)
        self.custom_comms: list[str] = []
        self.custom_types: list[Optional[tuple[type]]] = []
        self.custom_actns: list[str] = []
        for comm in custom_commands:
            self.custom_comms.append(comm[0])
            self.custom_types.append(comm[1])
            self.custom_actns.append(comm[2])

    def render(self, events: list[pygame.event.Event], globais: dict) -> None:
        """
        rederiza a caixa de texto, deteta a escrita e executa os comandos

        :param events: variável correspondente a pygame.event.get()
        :param globais: globals() para utilizar quaisquer variaveis ou um dicionário com as que se pretende poder usar
        """
        if self.rendered:
            pygame.draw.rect(self.superficie, 10, (self.coords[0], self.coords[1], self.rect[0], self.rect[1]))
            self.superficie.blit(self.fonte.render(self.texto, True, (100, 100, 100)), self.coords_texto)

            if self.output != '':
                pygame.draw.rect(self.superficie, 10,
                                 (self.coords[0], self.coords[1] - self.rect[1], self.rect[0], self.rect[1]))
                self.superficie.blit(self.fonte.render(self.output, True, (100, 100, 100)),
                                     (self.coords_texto[0], self.coords_texto[1] - self.tamanho_texto * (3 / 2)))

            for e in events:
                if e.type == KEYDOWN:
                    self.cursor_visible = True  # So the user sees where he writes

                    # If none exist, create counter for that key:
                    if e.key not in self.keyrepeat_counters:
                        if not (e.key == K_RETURN or e.key == K_ESCAPE):  # Filters out return key, others can be added
                            self.keyrepeat_counters[e.key] = [0, e.unicode]

                    if e.key == K_BACKSPACE:
                        self.texto = (
                                self.texto[:max(self.cursor_position - 1, 0)]
                                + self.texto[self.cursor_position:]
                        )

                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 0)
                    elif e.key == K_DELETE:
                        self.texto = (
                                self.texto[:self.cursor_position]
                                + self.texto[self.cursor_position + 1:]
                        )

                    elif e.key == K_RETURN:
                        try:
                            if self.texto.find("/help") == 0:
                                space = self.texto.find(" ")
                                if space != -1:
                                    self.output = str(self._comm_help(self.texto[space + 1:]))
                                else:
                                    self.output = str(self._comm_help())
                            else:
                                space = self.texto.find(" ")
                                index = self.custom_comms.index(self.texto[:space])
                                types = self.custom_types[index]
                                if types is not None:
                                    if isinstance(eval(self.texto[space + 1:], globais), types):
                                        input_index = self.custom_actns[index].find("input")
                                        action = self.custom_actns[index][:input_index] + self.texto[space + 1:] + \
                                                 self.custom_actns[index][input_index + 5:]
                                        try:
                                            self.output = str(eval(action, globais))
                                        except Exception as exep:
                                            self.output = str(exep)
                                    else:
                                        self.output = str(f"Wrong type input into the '{self.texto[:space]}' command")
                                else:
                                    input_index = self.custom_actns[index].find("input")
                                    if input_index == -1:
                                        action = self.custom_actns[index]
                                    else:
                                        action = self.custom_actns[index][:input_index] + self.texto[space + 1:] + \
                                                 self.custom_actns[index][input_index + 5:]
                                    try:
                                        self.output = str(eval(action, globais))
                                    except Exception as exep:
                                        self.output = str(exep)
                        except ValueError:
                            try:
                                self.output = str(eval(self.texto, globais))
                            except Exception as exep:
                                self.output = str(exep)
                        except Exception as exep:
                            self.output = str(exep)
                        finally:
                            self.old_texto = self.texto
                            self.texto = ""
                            self.cursor_position = 0

                    elif e.key == K_RIGHT:
                        # Add one to cursor_pos, but do not exceed len(input_string)
                        self.cursor_position = min(self.cursor_position + 1, len(self.texto))

                    elif e.key == K_LEFT:
                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 0)

                    elif e.key == K_UP:
                        if self.texto != self.old_texto:
                            self.texto_buffer = self.texto
                            self.texto = self.old_texto
                            self.cursor_position = len(self.texto)

                    elif e.key == K_DOWN:
                        if self.texto == self.old_texto:
                            self.texto = self.texto_buffer
                            self.cursor_position = len(self.texto)

                    elif e.key == K_END:
                        self.cursor_position = len(self.texto)

                    elif e.key == K_HOME:
                        self.cursor_position = 0

                    elif e.key == K_TAB and self.fonte.size(self.texto + self.tab_shortcut)[0] < \
                            self.rect[0] - (self.tamanho_texto * (1 / 4) + self.tamanho_texto // 10):
                        self.texto = (
                                self.texto[:self.cursor_position]
                                + self.tab_shortcut
                                + self.texto[self.cursor_position:]
                        )
                        self.cursor_position += len(self.tab_shortcut) - self.tab_back

                    elif self.fonte.size(self.texto + "m")[0] < \
                            self.rect[0] - (self.tamanho_texto * (1 / 4) + self.tamanho_texto // 10):
                        if e.unicode == "(":
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode
                                    + ")"
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)
                        elif e.unicode == '[':
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode
                                    + ']'
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)
                        elif e.unicode == '"' or e.unicode == "'":
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode * 2
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)
                        else:
                            # If no special key is pressed, add unicode of key to input_string
                            self.texto = (
                                    self.texto[:self.cursor_position]
                                    + e.unicode
                                    + self.texto[self.cursor_position:]
                            )
                            self.cursor_position += len(e.unicode)  # Some are empty, e.g. K_UP

                elif e.type == KEYUP:
                    # *** Because KEYUP doesn't include e.unicode, this dict is stored in such a weird way
                    if e.key in self.keyrepeat_counters:
                        del self.keyrepeat_counters[e.key]

            # Update key counters:
            for key in self.keyrepeat_counters:
                self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

                # Generate new key events if enough time has passed:
                if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                    self.keyrepeat_counters[key][0] = (
                            self.keyrepeat_intial_interval_ms
                            - self.keyrepeat_interval_ms
                    )

                    event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                    pygame.event.post(pygame.event.Event(KEYDOWN, key=event_key, unicode=event_unicode))

            # Update self.cursor_visible
            self.cursor_ms_counter += self.clock.get_time()
            if self.cursor_ms_counter >= self.cursor_switch_ms:
                self.cursor_ms_counter %= self.cursor_switch_ms
                self.cursor_visible = not self.cursor_visible

            if self.cursor_visible:
                cursor_x_pos = self.fonte.size(self.texto[:self.cursor_position])[0] + self.coords_texto[0]
                self.superficie.blit(self.cursor_surface, (cursor_x_pos, self.coords_texto[1]))

        for e in events:
            if e.type == KEYDOWN:
                if self.rendered:
                    if e.key == K_ESCAPE:
                        self.texto = ""
                        self.cursor_position = 0
                        self.rendered = False
                else:
                    if e.unicode == 'T':
                        self.rendered = True

    def _comm_help(self, comm: str = None):
        if comm is None:
            return self.custom_comms
        else:
            try:
                for i, c in enumerate(self.custom_comms):
                    if c == comm:
                        index = i
                        break
                command = [self.custom_comms[index], self.custom_types[index], self.custom_actns[index]]
                return command
            except NameError:
                return f"The command name you typed ({str(comm)}) isn't a defined custom command"
