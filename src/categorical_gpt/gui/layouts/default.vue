<template>
    <div class="flex flex-col min-h-screen bg-base-300" :data-theme="settingsStore.theme">
        <div class="flex-grow content-center">
            <div class="flex justify-between items-center p-4 pb-8 bg-base-100 shadow-md relative">
                <div class="w-32">
                    <button v-if="wizzardStore.prevStep" @click="wizzardStore.loadStep(wizzardStore.prevStep)"
                        class="btn btn-primary" :disabled="isPrevStepDisabled()">
                        <Icon name="ic:baseline-arrow-back-ios" />
                    </button>
                </div>
                <div class="flex-grow">
                    <div class="flex justify-center">
                        <WizzardStepper />
                    </div>
                </div>
                <div class="w-32 text-right">
                    <button v-if="wizzardStore.nextStep" @click="wizzardStore.loadStep(wizzardStore.nextStep)"
                        :disabled="isNextStepDisabled()" class="btn btn-primary">
                        <Icon name="ic:baseline-arrow-forward-ios" />
                    </button>
                </div>
            </div>

            <div class="p-4">
                <slot />
            </div>
        </div>
        <div>
            © Copyright 2023
        </div>
    </div>
</template>

<script setup>
import { useRouter } from "nuxt/app";
import { useSettingsStore } from "~/store/settings";
import { useWizzardStore } from "~/store/wizzard";
const settingsStore = useSettingsStore();
const wizzardStore = useWizzardStore();
const router = useRouter();

const isNextStepDisabled = () => {
    return wizzardStore.isLoading || !wizzardStore.isStepReady(wizzardStore.currentStep)
}

const isPrevStepDisabled = () => {
    return wizzardStore.isLoading
}
</script>