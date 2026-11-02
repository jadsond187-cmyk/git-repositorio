const quantidadeEstrelas = 30;
const elementoInicial = document.getElementById('estrela');
const estrelas = [];

if (elementoInicial) {
  estrelas.push(elementoInicial);
} else {
  throw new Error('O elemento inicial da estrela não foi encontrado.');
}

for (let indice = 1; indice < quantidadeEstrelas; indice += 1) {
  const estrela = document.createElement('div');
  estrela.classList.add('estrela');
  document.body.appendChild(estrela);
  estrelas.push(estrela);
}

const animacoes = estrelas.map((elemento) => {
  const tamanho = 14 + Math.random() * 16;
  elemento.style.width = `${tamanho}px`;
  elemento.style.height = `${tamanho}px`;

  return {
    elemento,
    tamanho,
    x: Math.random() * Math.max(0, window.innerWidth - tamanho),
    y: Math.random() * window.innerHeight - tamanho,
    velocidade: 4 + Math.random() * 4,
  };
});

function animarEstrelas() {
  for (const estrela of animacoes) {
    estrela.y += estrela.velocidade;

    if (estrela.y > window.innerHeight) {
      estrela.y = -estrela.tamanho;
      estrela.x = Math.random() * Math.max(0, window.innerWidth - estrela.tamanho);
    }

    estrela.elemento.style.left = `${estrela.x}px`;
    estrela.elemento.style.top = `${estrela.y}px`;
  }

  requestAnimationFrame(animarEstrelas);
}

requestAnimationFrame(animarEstrelas);
