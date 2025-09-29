<script setup>
import { ref, onMounted, watch } from 'vue';
import * as d3 from 'd3';
import { generateBluePalette } from '../utils/cores';
import { translateVehicleKey } from '../utils/tradutor';

const props = defineProps({
    data: {
        type: Object,
        required: true
    }
});

const svgRef = ref(null);

const drawChart = () => {
    const svg = d3.select(svgRef.value);
    svg.selectAll('*').remove();
    const { width, height } = svg.node().getBoundingClientRect();
    const margin = { top: 30, right: 20, bottom: 80, left: 40 }
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const rawData = Object.entries(props.data).map(([key, value]) => ({ key, value }));
    rawData.sort((a, b) => translateVehicleKey(a.key).localeCompare(translateVehicleKey(b.key)));

    const categories = rawData.map(d => d.key);
    const translatedCategories = categories.map(translateVehicleKey);

    const xScale = d3.scaleBand()
        .domain(translatedCategories)
        .range([0, chartWidth])
        .padding(0.1);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(rawData, d => d.value) * 1.2])
        .range([chartHeight, 0]);

    g.append('g')
        .attr('transform', `translate(0, ${chartHeight})`)
        .call(d3.axisBottom(xScale))
        .selectAll('text')
        .attr('class', 'x-axis-label')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end');

    g.append('g')
        .call(
            d3.axisLeft(yScale)
            .tickValues(d3.range(0, d3.max(rawData, d => d.value) + 1, 1))
            .tickFormat(d3.format('d'))
        )
        .selectAll('text')
        .attr('class', 'y-axis-label');

    g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left - 4)
        .attr('x', 0 - (chartHeight / 2))
        .attr('dy', '1em')
        .attr('class', 'axis-label')
        .style('text-anchor', 'middle')
        .text('Número de Registros');

    const bars = g.selectAll('.bar')
        .data(rawData)
        .join('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(translateVehicleKey(d.key)))
        .attr('y', chartHeight)
        .attr('width', xScale.bandwidth())
        .attr('height', 0)
        .attr('fill', (d, i) => generateBluePalette(categories.length)[i])
        .on('mouseover', function (event, d) {
            d3.select(this).attr('opacity', 0.7);
            tooltip.style('visibility', 'visible')
                .html(`<strong>${translateVehicleKey(d.key)}</strong><br/>Registros: ${d.value}`)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 20) + 'px');
        })
        .on('mouseout', function () {
            d3.select(this).attr('opacity', 1);
            tooltip.style('visibility', 'hidden');
        });

    bars.transition()
        .duration(800)
        .attr('y', d => yScale(d.value))
        .attr('height', d => chartHeight - yScale(d.value))
        .delay((d, i) => i * 100);

    g.selectAll('.bar-value')
        .data(rawData)
        .join('text')
        .attr('class', 'bar-value')
        .attr('x', d => xScale(translateVehicleKey(d.key)) + xScale.bandwidth() / 2)
        .attr('y', d => yScale(d.value) - 45)
        .attr('text-anchor', 'middle')
        .text(d => d.value)
        .attr('opacity', 0)
        .transition()
        .duration(800)
        .attr('opacity', 1)
        .delay((d, i) => i * 100);

    const tooltip = d3.select('body').append('div')
        .attr('class', 'd3-tooltip')
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('background-color', 'rgba(0,0,0,0.8)')
        .style('color', 'white')
        .style('padding', '8px')
        .style('border-radius', '4px')
        .style('pointer-events', 'none');
};

onMounted(() => {
    if (svgRef.value) drawChart();
});

watch(() => props.data, () => {
    if (svgRef.value) drawChart();
}, { deep: true });
</script>

<template>
    <div class="chart-wrapper">
        <svg ref="svgRef"></svg>
    </div>
</template>

<style scoped>
.chart-wrapper {
    width: 90%;
    /* GARANTE QUE O WRAPPER OCUPE 90% DA LARGURA */
    min-height: 300px;
    height: 90%;
    /* GARANTE QUE O WRAPPER OCUPE 90% DA ALTURA */
    display: flex;
    /* Para centralizar o SVG */
    align-items: center;
    justify-content: center;
    position: relative;
    margin: auto;
}

svg {
    width: 100%;
    /* O SVG OCUPA 100% DA LARGURA E ALTURA DO WRAPPER */
    height: 100%;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Estilos D3 para elementos dentro do SVG */
:deep(.bar) {
    transition: opacity 0.2s ease-in-out;
}

:deep(.x-axis-label) {
    font-size: 0.95rem;
    fill: #555;
}

:deep(.y-axis-label) {
    font-size: 0.95rem;
    fill: #555;
}

:deep(.axis-label) {
    font-size: 1rem;
    font-weight: 500;
    fill: #333;
}

:deep(.bar-value) {
    font-size: 1.1rem;
    font-weight: 600;
    fill: #333;
}

/* Estilo para o tooltip D3 (externo ao SVG) */
.d3-tooltip {
    font-size: 0.9rem;
    line-height: 1.4;
}
</style>