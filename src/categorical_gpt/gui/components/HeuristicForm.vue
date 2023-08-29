<template>
    <div>

        <textarea rows="8" class="textarea textarea-bordered w-full" :placeholder="`Heuristic for ${characteristic}`"
            v-model="datasetStore.cgpt.heuristics[characteristic]"></textarea>
        <progress class="progress w-full" v-if="datasetStore.cgpt.heuristics[characteristic] === undefined"></progress>
    </div>
</template>

<script lang="ts" setup>
import { useDatasetStore } from "~/store/dataset";
const datasetStore = useDatasetStore();

const props = defineProps({
    characteristic: {
        type: String,
        required: true
    }
})
</script>