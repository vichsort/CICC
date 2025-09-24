<script setup>
import { ref, onMounted, watch } from 'vue';
import * as d3 from 'd3';
import { generateBluePalette } from '../utils/cores';

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
    const dataset = Object.entries(props.data).map(([key, value]) => ({ key, value }));

    const margin = { top: 30, right: 20, bottom: 50, left: 40 };
    const { width, height } = svg.node().getBoundingClientRect();
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const chart = svg.append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const xScale = d3.scaleBand()
        .domain(dataset.map(d => d.key))
        .range([0, innerWidth])
        .padding(0.2);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(dataset, d => d.value) * 1.1])
        .range([innerHeight, 0]);

    const xAxis = d3.axisBottom(xScale);
    chart.append('g')
        .attr('transform', `translate(0, ${innerHeight})`)
        .call(xAxis)
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.8em')
        .attr('dy', '.15em')
        .attr('transform', 'rotate(-25)');

    const yAxis = d3.axisLeft(yScale);
    chart.append('g').call(yAxis);

    const colorScale = d3.scaleOrdinal()
        .domain(dataset.map(d => d.key))
        .range(generateBluePalette(dataset.length));

    chart.selectAll('.bar')
        .data(dataset)
        .join('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(d.key))
        .attr('y', d => yScale(d.value))
        .attr('width', xScale.bandwidth())
        .attr('height', d => innerHeight - yScale(d.value))
        .attr('fill', d => colorScale(d.key));

    chart.selectAll('.bar-label')
        .data(dataset)
        .join('text')
        .attr('class', 'bar-label')
        .attr('x', d => xScale(d.key) + xScale.bandwidth() / 2)
        .attr('y', d => yScale(d.value) - 5)
        .attr('text-anchor', 'middle')
        .text(d => d.value);
};

onMounted(() => {
    if (svgRef.value) drawChart();
});

watch(() => props.data, () => {
    if (svgRef.value) drawChart();
}, { deep: true });
</script>

<template>
    <div class="bar-chart-container">
        <h5 class="chart-title">Combustíveis Utilizados</h5>
        <svg ref="svgRef"></svg>
    </div>
</template>

<style scoped>
.bar-chart-container {
    width: 100%;
    height: 100%;
    min-height: 450px;
    display: flex;
    flex-direction: column;
}

.chart-title {
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
}

svg {
    width: 100%;
    height: 100%;
}

:deep(.bar-label) {
    font-size: 0.8rem;
    font-weight: 500;
    fill: #333;
}

:deep(.bar) {
    transition: opacity 0.2s ease-in-out;
}

:deep(.bar:hover) {
    opacity: 0.8;
}
</style>