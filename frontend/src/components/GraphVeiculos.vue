<script setup>
import { ref, onMounted, watch } from 'vue';
import * as d3 from 'd3';
import { generateBluePalette } from '../utils/cores.js';

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
    const margin = 20;
    const radius = Math.min(width, height) / 2 - margin;
    const g = svg.append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const categories = Object.keys(props.data);
    const colorScale = d3.scaleOrdinal()
        .domain(categories)
        .range(generateBluePalette(categories.length));
    const pieData = Object.entries(props.data).map(([key, value]) => ({ key, value }));

    const pie = d3.pie()
        .value(d => d.value)
        .sort(null);

    const data_ready = pie(pieData);

    const arcGenerator = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

    g.selectAll('path')
        .data(data_ready)
        .join('path')
        .attr('d', arcGenerator)
        .attr('fill', d => colorScale(d.data.key))
        .attr('stroke', 'white')
        .style('stroke-width', '2px')
        .attr('class', 'pie-slice')
        .on('click', (event, d) => {
            g.selectAll('.info-text').remove();
            g.selectAll('.pie-slice').style('opacity', 1);
            d3.select(event.currentTarget).style('opacity', 0.7);

            g.append('text')
                .attr('class', 'info-text')
                .attr('text-anchor', 'middle')
                .attr('dy', '-0.5em')
                .text(d.data.key)
                .append('tspan')
                .attr('class', 'info-text-value')
                .attr('x', 0)
                .attr('dy', '1.2em')
                .text(`${d.data.value} registro(s)`);
        });

    const legendGroup = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${margin}, ${height - (categories.length * 20)})`);

    const legendItems = legendGroup.selectAll('.legend-item')
        .data(categories)
        .join('g')
        .attr('class', 'legend-item')
        .attr('transform', (d, i) => `translate(0, ${i * 20})`);

    legendItems.append('rect')
        .attr('width', 15)
        .attr('height', 15)
        .attr('fill', d => colorScale(d));

    legendItems.append('text')
        .attr('x', 20)
        .attr('y', 12)
        .text(d => d);
};

onMounted(() => {
    if (svgRef.value) drawChart();
});

watch(() => props.data, () => {
    if (svgRef.value) drawChart();
}, { deep: true });
</script>

<template>
    <div class="pie-chart-container">
        <svg ref="svgRef"></svg>
    </div>
</template>

<style scoped>
.pie-chart-container {
    width: 100%;
    height: 100%;
    min-height: 450px;
}

:deep(.pie-slice) {
    cursor: pointer;
    transition: opacity 0.2s ease-in-out;
}

:deep(.info-text) {
    font-size: 1.2rem;
    font-weight: bold;
    fill: #333;
}

:deep(.info-text-value) {
    font-size: 1rem;
    font-weight: normal;
    fill: #666;
}

:deep(.legend text) {
    font-size: 0.9rem;
}
</style>