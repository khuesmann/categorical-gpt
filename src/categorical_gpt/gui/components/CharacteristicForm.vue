<template>
    <div class="modal modal-open">
        <div class="card bg-base-100 shadow-xl p-4">
            <h3 class="font-bold text-lg mb-4">Add new characteristic</h3>
            <input v-model="characteristicName" type="text" placeholder="Type here"
                class="input input-bordered w-full mb-4" />
            <div class="flex justify-between">
                <button class="btn" @click="emit('close')">Close</button>
                <button class="btn btn-success" @click="emit('add', characteristicName)">Add</button>
            </div>
        </div>

    </div>
</template>
<script lang="ts" setup>
const emit = defineEmits(['close', 'add'])
const characteristicName = ref<string>('')
</script>