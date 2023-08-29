<template>
    <div class="flex gap-4">
        <div class="flex-shrink-0">
            <div class="max-h-[80vh] overflow-y-auto">
                <CharacteristicList :loading="loadingCharacteristics" v-model="datasetStore.selectedCharacteristic" />
                <CharacteristicForm v-if="showCharacteristicForm" @add="onAddCharacteristic"
                    @close="onCloseCharacteristicForm" />
            </div>
            <div class="text-center">
                <a class="btn btn-ghost mt-2" @click="showCharacteristicForm = true">
                    <Icon name="material-symbols:add" /> Add new
                </a>
            </div>
        </div>
        <div class="divider divider-horizontal"></div>
        <div class="flex-grow">
            <div v-if="!datasetStore.selectedCharacteristic" class="alert alert-info">
                <Icon name="zondicons:information-outline" />
                <div>Select a characteristic to edit it's heuristic.</div>
                <div>
                    <button class="btn btn-sm" @click="onReloadCharacteristics">
                        Reload
                        <Icon name="ic:round-refresh" />
                    </button>
                </div>
            </div>
            <div v-else>
                <h1 class="text-lg font-bold">{{ datasetStore.selectedCharacteristic }}</h1>
                <HeuristicForm :characteristic="datasetStore.selectedCharacteristic" />
            </div>
        </div>

    </div>
</template>
<script lang="ts" setup>
import { useWizzardStore } from "~/store/wizzard";
import { Characteristic, useDatasetStore } from "~/store/dataset";
const wizzardStore = useWizzardStore();
const datasetStore = useDatasetStore();

const showCharacteristicForm = ref<boolean>(false)

const onAddCharacteristic = (characteristicName: string) => {
    datasetStore.addCharacteristic(characteristicName)
    showCharacteristicForm.value = false
    datasetStore.selectedCharacteristic = characteristicName
}

const onCloseCharacteristicForm = () => {
    showCharacteristicForm.value = false
}

const onReloadCharacteristics = async () => {
    wizzardStore.isStepLoading[wizzardStore.steps[1].number] = true
    wizzardStore.hasStepLoaded[wizzardStore.steps[2].number] = false
    await datasetStore.loadCharacteristics(true)
    await Promise.all(
        datasetStore.cgpt.characteristics.map(
            (characteristic: Characteristic) => {
                return datasetStore.loadHeuristic(characteristic.name);
            },
        ),
    );
    wizzardStore.isStepLoading[wizzardStore.steps[1].number] = false
}

const loadingCharacteristics = computed(() => {
    const loadingCharacteristics = []
    for (let characteristic of datasetStore.cgpt.characteristics) {
        if (!datasetStore.cgpt.heuristics[characteristic.name]) {
            loadingCharacteristics.push(characteristic.name)
        }
    }
    return loadingCharacteristics
})

onMounted(() => {
    if (!wizzardStore.hasStepLoaded[wizzardStore.steps[1].number]) {
        wizzardStore.loadStep(wizzardStore.steps[1])
    }
})
</script>