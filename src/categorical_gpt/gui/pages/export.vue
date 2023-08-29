<template>
    <div class="flex gap-4">
        <div class="flex-1">
            <div class="font-bold mb-2">Feature vectors</div>
            <ClipboardTextarea :json="datasetStore.results.feature_vectors" />
            <div class="font-bold mb-2">Feature dictionary</div>
            <ClipboardTextarea :json="datasetStore.results.feature_vectors_dict" />
        </div>
        <div class="divider divider-horizontal"></div>
        <div class="flex-1">
            <div class="font-bold mb-2">Color-coding</div>
            <ClipboardTextarea :json="datasetStore.results.color_coding" />
        </div>
        <div class="divider divider-horizontal"></div>
        <div class="flex-1">
            <div class="font-bold mb-2">Ordering</div>
            <ClipboardTextarea :json="datasetStore.results.ordering" />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useWizzardStore } from "~/store/wizzard";
import { useDatasetStore } from "~/store/dataset";
const wizzardStore = useWizzardStore();
const datasetStore = useDatasetStore();

onMounted(() => {
    if (!wizzardStore.hasStepLoaded[wizzardStore.steps[4].number]) {
        wizzardStore.loadStep(wizzardStore.steps[4])
    }
})
</script>