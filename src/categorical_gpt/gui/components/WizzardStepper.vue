<template>
    <div class="flex items-center">
        <div v-for="(step, i) in wizzardStore.steps" class="flex items-center">
            <div class="mr-2 text-center h-16 w-28 lg:w-32">
                <button @click="wizzardStore.loadStep(step)" class="btn btn-circle btn-sm "
                    :class="{ 'btn-primary': wizzardStore.hasStepLoaded[step.number], 'btn-outline': !isCurrent(step) }">
                    <span v-if="!wizzardStore.isStepLoading[step.number]">{{ step.number - 1 }}</span>
                    <span v-else class="loading loading-spinner loading-xs"></span>
                </button> <br>
                <span class="text-sm" :class="{ 'font-bold': wizzardStore.currentStep.number == step.number }">{{ step.name
                }}</span>
            </div>
            <div v-if="i < wizzardStore.steps.length - 1">
                <progress class="progress progress-primary w-12 lg:w-16" :value="wizzardStore.stepProgress[step.number + 1]"
                    max="100"></progress>
                <br> &nbsp;
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>

import { useWizzardStore } from "~/store/wizzard";
import { useRouter } from "nuxt/app";
const wizzardStore = useWizzardStore();
const router = useRouter();

const isCurrent = (step: any) => {
    return wizzardStore.currentStep.number == step.number
}

const onClickStep = (step: any) => {
    if (!wizzardStore.isLoading) {
        wizzardStore.loadStep(step)
    }
}
</script>