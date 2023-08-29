<template>
    <select class="bg-base-300 w-full max-w-xs pl-1 py-1" @change="onSelectOrdering">
        <option value="mds">Ordering: mds</option>
        <option value="tsp">Ordering: tsp</option>
        <option value="tsp+mds" selected>Ordering: tsp+mds</option>
        <option value="lexicographic">Ordering: Lexicographic</option>
    </select>
</template>

<script lang="ts" setup>
import { useDatasetStore } from "~/store/dataset";
const datasetStore = useDatasetStore();

const onSelectOrdering = (method: any) => {
    datasetStore.loadOrdering(method.target.value)
}
</script>