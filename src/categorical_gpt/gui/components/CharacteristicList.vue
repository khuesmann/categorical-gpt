<template>
    <div class="flex flex-col gap-2">
        <ul v-for="characteristic in datasetStore.cgpt.characteristics">
            <li class="flex gap-4 justify-between items-center">
                <button class="btn flex-grow max-w-md" @click="onSelectCharacteristic(characteristic)"
                    :class="{ 'btn-primary': selectedCharacteristic === characteristic.name }">
                    {{ characteristic.name }}
                </button>

                <div class="tooltip tooltip-left" data-tip="Missing values"
                    v-if="props.erroneous.length > 0 && props.erroneous.indexOf(characteristic.name) >= 0">
                    <Icon class="text-lg text-error" name="bx:error" />
                </div>
                <span v-if="props.loading.indexOf(characteristic.name) >= 0"
                    class="loading loading-spinner loading-xs"></span>
                <input v-else type="checkbox" v-model="characteristic.is_active" class="checkbox" />
            </li>
        </ul>

    </div>
</template>

<script setup lang="ts">
import { Characteristic, useDatasetStore } from "~/store/dataset";
import { useSettingsStore } from "~/store/settings";

const datasetStore = useDatasetStore();
const settingsStore = useSettingsStore();

const props = defineProps({
    modelValue: {
        type: String,
    },
    erroneous: {
        type: Array,
        default: () => [],
    },
    loading: {
        type: Array,
        default: () => [],
    },
})

const emit = defineEmits(['update:modelValue'])
const selectedCharacteristic = ref<string>('')

watch(() => props.modelValue, (value) => {
    if (!value) return
    selectedCharacteristic.value = value
})

const onSelectCharacteristic = (characteristic: Characteristic) => {
    if (characteristic.name != selectedCharacteristic.value) {
        selectedCharacteristic.value = characteristic.name
        emit('update:modelValue', characteristic.name)
    } else {
        selectedCharacteristic.value = ''
        emit('update:modelValue', '')
    }

}

onMounted(() => {
    if (props.modelValue) {
        selectedCharacteristic.value = props.modelValue
    }
})

</script>
