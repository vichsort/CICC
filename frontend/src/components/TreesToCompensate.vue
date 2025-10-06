<template>
    <div class="container">
        <img src="../assets/tree.gif">
        <div class="data">
            <span class="number-of-trees">{{ data }}</span>
            <p>{{ data > 1 ? "Árvores" : "Árvore" }} para compensar</p>
        </div>
    </div>

</template>

<script setup>
    defineProps({
        data: {
            type: Number,
            required: true
        }
    })
</script>

<style scoped>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2em;
        gap: 2em;
        text-align: center;
    }

    img {
        height: 350px;
    }

    .data {
        font-size: 2em;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .number-of-trees {
        font-weight: bold;
        font-size: 5em;
    }

    @media (max-width: 1000px) {
        .container {
            flex-direction: column;
        }
    }
</style>