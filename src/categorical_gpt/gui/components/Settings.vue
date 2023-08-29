<template>
    <div class="modal modal-open">
        <div class="card w-96 bg-base-100 shadow-xl p-4">
            <h3 class="font-bold text-3xl mb-4">Settings</h3>

            <div class="font-bold text-xl">Model</div>
            <input class="input input-bordered w-full mb-1" placeholder="Model name" v-model="model" />
            <div class="text-xs text-error">{{ errors.model }}</div>
            <div class="text-xs text-warning">{{ warnings.model }}</div>


            <div class="divider divider-vertical"></div>

            <div class="font-bold text-xl">Model parameters</div>
            <div class="flex flex-col gap-2">

                <div class="w-full">
                    <div class="font-bold">Characteristic</div>
                    <textarea class="textarea textarea-bordered w-full" v-model="characteristicModelParameters" />
                    <div class="text-xs text-error">{{ errors.characteristicModelParameters }}</div>
                </div>

                <div class="w-full">
                    <div class="font-bold">Heuristic</div>
                    <textarea class="textarea textarea-bordered w-full" v-model="heuristicModelParameters" />
                    <div class="text-xs text-error">{{ errors.heuristicModelParameters }}</div>
                </div>

                <div class="w-full">
                    <div class="font-bold">Apply heuristic</div>
                    <textarea class="textarea textarea-bordered w-full" v-model="applyHeuristicModelParameters" />
                    <div class="text-xs text-error">{{ errors.applyHeuristicModelParameters }}</div>
                </div>
            </div>

            <div class="flex justify-between mt-4">
                <button class="btn" @click="emit('close')">Close</button>
                <button class="btn btn-success" @click="onSave" :disabled="hasErrors">Save</button>
            </div>
        </div>

    </div>
</template>

<script lang="ts" setup>
import { useSettingsStore } from '~/store/settings';

const settingsStore = useSettingsStore();

const characteristicModelParameters = ref('')
const heuristicModelParameters = ref('')
const applyHeuristicModelParameters = ref('')
const model = ref('')

const errors = ref<Record<string, string>>({
    characteristicModelParameters: '',
    heuristicModelParameters: '',
    applyHeuristicModelParameters: '',
    model: '',
})

const warnings = ref<Record<string, string>>({
    model: '',
})

const emit = defineEmits(['close'])

const hasErrors = computed(() => {
    return !Object.values(errors.value).every((error) => error === '')
})

watch(() => characteristicModelParameters.value, (value) => {
    try {
        errors.value.characteristicModelParameters = ''
        JSON.parse(value)
    } catch (e) {
        errors.value.characteristicModelParameters = 'No valid JSON'
    }
})

watch(() => heuristicModelParameters.value, (value) => {
    try {
        errors.value.heuristicModelParameters = ''
        JSON.parse(value)
    } catch (e) {
        errors.value.heuristicModelParameters = 'No valid JSON'
    }
})

watch(() => applyHeuristicModelParameters.value, (value) => {
    try {
        errors.value.applyHeuristicModelParameters = ''
        JSON.parse(value)
    } catch (e) {
        errors.value.applyHeuristicModelParameters = 'No valid JSON'
    }
})

watch(() => model.value, (value) => {
    if (value === '') {
        errors.value.model = 'Model name is empty'
    } else if (!settingsStore.availableModels.includes(value)) {
        warnings.value.model = 'Make sure that the API maps this model to a driver.'
    } else {
        errors.value.model = ''
        warnings.value.model = ''
    }
})


const onSave = () => {
    settingsStore.modelParams.characteristic = JSON.parse(characteristicModelParameters.value)
    settingsStore.modelParams.heuristic = JSON.parse(heuristicModelParameters.value)
    settingsStore.modelParams.apply_heuristic = JSON.parse(applyHeuristicModelParameters.value)
    settingsStore.model = model.value
    emit('close')
}

onMounted(() => {
    model.value = settingsStore.model
    characteristicModelParameters.value = JSON.stringify(settingsStore.modelParams.characteristic, null, 0)
    heuristicModelParameters.value = JSON.stringify(settingsStore.modelParams.heuristic, null, 0)
    applyHeuristicModelParameters.value = JSON.stringify(settingsStore.modelParams.apply_heuristic, null, 0)
})

</script>