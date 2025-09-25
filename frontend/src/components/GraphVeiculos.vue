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

    const { width, height } = svg.node().getBoundingClientRect();
    const margin = 0;
    const radius = (Math.min(width, height) / 2 - margin) * 0.6;

    const g = svg.append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2 - 30})`);

    const categories = Object.keys(props.data);
    const colorScale = d3.scaleOrdinal()
        .domain(categories)
        .range(generateBluePalette(categories.length));
    const pieData = Object.entries(props.data).map(([key, value]) => ({ key, value }));
    const totalValue = d3.sum(pieData, d => d.value);
    const pie = d3.pie().value(d => d.value).sort(null);
    const data_ready = pie(pieData);

    const arcGenerator = d3.arc()
        .innerRadius(radius * 0.6)
        .outerRadius(radius);
    const arcHover = d3.arc()
        .innerRadius(radius * 0.6)
        .outerRadius(radius * 1.05);

    const centralTextGroup = g.append('g').attr('class', 'central-text-group');
    centralTextGroup.append('text').text('Total').attr('class', 'total-label').attr('text-anchor', 'middle').attr('dy', '-0.5em');
    centralTextGroup.append('text').text(totalValue).attr('class', 'total-value').attr('text-anchor', 'middle').attr('dy', '0.8em');

    g.selectAll('path')
        .data(data_ready)
        .join('path')
        .attr('d', arcGenerator)
        .attr('fill', d => colorScale(d.data.key))
        .attr('stroke', '#fff')
        .style('stroke-width', '4px') 
        .attr('class', 'donut-slice')
        .on('mouseover', function (event, d) {
            d3.select(this).transition().duration(200).attr('d', arcHover);
        })
        .on('mouseout', function (event, d) {
            d3.select(this).transition().duration(200).attr('d', arcGenerator);
        })
        .on('click', (event, d) => {
            svg.select('.info-box').remove();
            const percentage = (d.data.value / totalValue * 100).toFixed(1);
            const infoText = `${d.data.key}: ${d.data.value} registro(s) (${percentage}%)`;

            const infoBox = svg.append('g')
                .attr('class', 'info-box')
                .attr('transform', `translate(${width / 2}, ${height / 2 + radius / 2 + 50})`);

            infoBox.append('text')
                .text(infoText)
                .attr('class', 'info-box-text')
                .attr('text-anchor', 'middle');
        });
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
  width: 100%;
  height: 100%; 
  position: relative;
}
svg {
  width: 100%;
  height: 100%;
  font-family: inherit;
}

:deep(.donut-slice) { cursor: pointer; }
:deep(.total-label) { font-size: 1.2rem; font-weight: 500; fill: #6c757d; }
:deep(.total-value) { font-size: 2.2rem; font-weight: 700; fill: #212529; }
:deep(.info-box-text) { font-size: 1.25rem; font-weight: 500; fill: #333; }
</style>
