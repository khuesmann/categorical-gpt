<template>
    <div class="flex flex-col gap-4">
        <div class="text-right">
            <div class="tooltip tooltip-left" :data-tip="`Reload values for '${props.characteristic}'`">
                <button @click="onReloadValues">
                    <Icon name="ic:round-refresh" />
                </button>
            </div>

        </div>
        <div v-for="(values, option) in datasetStore.cgpt.characteristic_values[characteristic]">
            <div class="font-bold"
                :class="{ 'text-error': datasetStore.cgpt.characteristic_values[characteristic][option] < 0 }">{{ option }}
            </div>
            <div class="flex gap-4">
                <div class="flex-grow">
                    <input type="range" min="0" max="100"
                        v-model="datasetStore.cgpt.characteristic_values[characteristic][option]" class="range" step="1" />
                    <div v-if="false" class="w-full flex justify-between text-xs px-2">
                        <span>0</span>
                        <span>25</span>
                        <span>50</span>
                        <span>75</span>
                        <span>100</span>
                    </div>
                </div>
                <div>
                    <input class="p-1" size="4" v-model="datasetStore.cgpt.characteristic_values[characteristic][option]" />
                </div>
            </div>

        </div>
    </div>
</template>

<script lang="ts" setup>
import { useDatasetStore } from "~/store/dataset";
import { useWizzardStore } from "~/store/wizzard";
const datasetStore = useDatasetStore();
const wizzardStore = useWizzardStore();

const props = defineProps({
    characteristic: {
        type: String,
        required: true
    }
})

const onReloadValues = async () => {
    wizzardStore.isStepLoading[wizzardStore.steps[2].number] = true
    await datasetStore.loadValues(props.characteristic, datasetStore.cgpt.heuristics[props.characteristic])
    wizzardStore.isStepLoading[wizzardStore.steps[2].number] = false
}
</script>