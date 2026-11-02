const areaTeste = document.getElementById('area-teste');
const guiaPonteiro = document.getElementById('guia-ponteiro');
const marcador = document.getElementById('marcador');
const coordenadaPonteiro = document.getElementById('coordenada-ponteiro');
const coordenadaMarcacao = document.getElementById('coordenada-marcacao');
const anuncioMarcacao = document.getElementById('anuncio-marcacao');
const botaoLimpar = document.getElementById('limpar');
let posicaoAtual = null;

function obterCoordenadas(evento) {
  const limites = areaTeste.getBoundingClientRect();
  const largura = areaTeste.clientWidth;
  const altura = areaTeste.clientHeight;

  return {
    x: Math.round(
      Math.max(0, Math.min(evento.clientX - limites.left - areaTeste.clientLeft, largura - 1)),
    ),
    y: Math.round(
      Math.max(0, Math.min(evento.clientY - limites.top - areaTeste.clientTop, altura - 1)),
    ),
  };
}

function atualizarPosicao(x, y) {
  posicaoAtual = { x, y };
  guiaPonteiro.style.left = `${x}px`;
  guiaPonteiro.style.top = `${y}px`;
  guiaPonteiro.hidden = false;
  coordenadaPonteiro.textContent = `X: ${x}, Y: ${y}`;
}

function marcarPosicao() {
  if (!posicaoAtual) {
    atualizarPosicao(0, 0);
  }

  const { x, y } = posicaoAtual;
  marcador.style.left = `${x}px`;
  marcador.style.top = `${y}px`;
  marcador.hidden = false;
  coordenadaMarcacao.textContent = `X: ${x}, Y: ${y}`;
  anuncioMarcacao.textContent = `Posição marcada em X ${x}, Y ${y}.`;
}

areaTeste.addEventListener('pointermove', (evento) => {
  const { x, y } = obterCoordenadas(evento);
  atualizarPosicao(x, y);
});

areaTeste.addEventListener('pointerleave', () => {
  guiaPonteiro.hidden = true;
  coordenadaPonteiro.textContent = 'X: --, Y: --';
});

areaTeste.addEventListener('pointerdown', (evento) => {
  const { x, y } = obterCoordenadas(evento);
  atualizarPosicao(x, y);
  marcarPosicao();
});

areaTeste.addEventListener('keydown', (evento) => {
  const teclasDeMovimento = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];

  if (teclasDeMovimento.includes(evento.key)) {
    evento.preventDefault();
    const passo = evento.shiftKey ? 10 : 1;
    const atual = posicaoAtual || { x: 0, y: 0 };
    const x = atual.x + (evento.key === 'ArrowRight' ? passo : evento.key === 'ArrowLeft' ? -passo : 0);
    const y = atual.y + (evento.key === 'ArrowDown' ? passo : evento.key === 'ArrowUp' ? -passo : 0);

    atualizarPosicao(
      Math.max(0, Math.min(x, areaTeste.clientWidth - 1)),
      Math.max(0, Math.min(y, areaTeste.clientHeight - 1)),
    );
    return;
  }

  if (evento.key === 'Home') {
    evento.preventDefault();
    atualizarPosicao(0, 0);
    return;
  }

  if (evento.key === 'End') {
    evento.preventDefault();
    atualizarPosicao(areaTeste.clientWidth - 1, areaTeste.clientHeight - 1);
    return;
  }

  if (evento.key === 'Enter' || evento.key === ' ') {
    evento.preventDefault();
    marcarPosicao();
  }
});

botaoLimpar.addEventListener('click', () => {
  marcador.hidden = true;
  coordenadaMarcacao.textContent = 'X: --, Y: --';
  anuncioMarcacao.textContent = 'Marcação limpa.';
});
