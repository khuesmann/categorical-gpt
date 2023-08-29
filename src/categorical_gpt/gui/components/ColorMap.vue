<template>
    <div>
        <div class="flex justify-between item-center" v-for="option in datasetStore.results.ordering">
            <div class="tooltip tooltip-left" :data-tip="option">
                <div class="overflow-hidden whitespace-nowrap overflow-ellipsis w-36 text-left">
                    {{ option }}
                </div>
            </div>
            <div />

            <div class="w-4 h-4"
                :style="`background-color: rgba(${datasetStore.results.color_coding[option][0] * 255}, ${datasetStore.results.color_coding[option][1] * 255}, ${datasetStore.results.color_coding[option][2] * 255})`">
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useDatasetStore } from "~/store/dataset";
const datasetStore = useDatasetStore();
</script>