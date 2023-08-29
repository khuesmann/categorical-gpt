<template>
    <div class="flex gap-4">
        <div class="flex-shrink-0">
            <div class="max-h-[80vh] overflow-y-auto">
                <CharacteristicList :erroneous="erroneousValueAssignments" v-model="datasetStore.selectedCharacteristic" />
            </div>
        </div>
        <div class="divider divider-horizontal"></div>
        <div class="flex-grow">
            <div v-if="!datasetStore.selectedCharacteristic" class="alert alert-info">
                <Icon name="zondicons:information-outline" />
                <div>Select a characteristic to edit it's value assignments.</div>
            </div>
            <div v-else>
                <h1 class="text-lg font-bold">{{ datasetStore.selectedCharacteristic }}</h1>
                <div class="alert">
                    <div>{{ datasetStore.cgpt.heuristics[datasetStore.selectedCharacteristic] }}</div>
                </div>
                <ValueEditor :characteristic="datasetStore.selectedCharacteristic" />
            </div>
        </div>

    </div>
</template>
<script lang="ts" setup>
import { useWizzardStore } from "~/store/wizzard";
import { useDatasetStore } from "~/store/dataset";
const wizzardStore = useWizzardStore();
const datasetStore = useDatasetStore();

const erroneousValueAssignments = computed(() => {
    const erroneousCharacteristics = []
    for (let characteristic in datasetStore.cgpt.characteristic_values) {
        for (let option in datasetStore.cgpt.characteristic_values[characteristic]) {
            if (datasetStore.cgpt.characteristic_values[characteristic][option] < 0) {
                erroneousCharacteristics.push(characteristic)
                break
            }
        }
    }
    return erroneousCharacteristics
})

onMounted(() => {
    if (!wizzardStore.hasStepLoaded[wizzardStore.steps[2].number]) {
        wizzardStore.loadStep(wizzardStore.steps[2])
    }
})
</script>