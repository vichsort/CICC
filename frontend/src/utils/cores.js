import * as d3 from 'd3';

/**
 * Gera uma paleta com 'n' tons de azul distintos e com bom contraste.
 * @param {number} n - A quantidade de cores necessárias.
 * @returns {string[]} Um array com 'n' códigos de cores hexadecimais.
 */
export function generateBluePalette(n) {
  // Se precisarmos de apenas uma cor, retornamos um azul padrão e agradável.
  if (n === 1) {
    return ["#2c7fb8"];
  }

  const colors = [];
  // d3.interpolateBlues é uma função que retorna uma cor de um gradiente de azul.
  // O valor de entrada vai de 0 (quase branco) a 1 (azul escuro).
  const colorInterpolator = d3.interpolateBlues;

  // Para garantir um bom contraste e evitar cores muito claras,
  // vamos gerar cores no intervalo de 0.3 a 0.9 do gradiente.
  for (let i = 0; i < n; i++) {
    colors.push(colorInterpolator(0.3 + (i / (n - 1)) * 0.6));
  }

  return colors;
}