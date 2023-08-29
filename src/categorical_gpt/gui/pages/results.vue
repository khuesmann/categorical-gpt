<template>
    <div class="flex">
        <div class="flex-grow">
            <ScatterPlot :points="points" />
        </div>
        <div class="divider divider-horizontal"></div>
        <div class="w-44">
            <div class="mb-2">
                <OrderingSelector />
            </div>
            <div>
                <ColorMap />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useWizzardStore } from "~/store/wizzard";
import { useDatasetStore } from "~/store/dataset";
const wizzardStore = useWizzardStore();
const datasetStore = useDatasetStore();

const points = computed(() => {
    const points = []
    for (let option in datasetStore.results.embedding) {
        points.push({
            x: datasetStore.results.embedding[option][0],
            y: datasetStore.results.embedding[option][1],
            label: option,
            color: datasetStore.results.color_coding[option].map((color) => color * 255),
        })
    }
    return points
})

onMounted(() => {
    if (!wizzardStore.hasStepLoaded[wizzardStore.steps[3].number]) {
        wizzardStore.loadStep(wizzardStore.steps[3])
    }
})

</script>