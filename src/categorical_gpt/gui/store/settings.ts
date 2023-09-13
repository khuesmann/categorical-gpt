import {defineStore} from 'pinia';
import {get} from '~/api/requests'

interface ModelParams {
    temperature: number;
    top_p: number;
    n: number;
    prevent_cache?: boolean;
}

export const useSettingsStore = defineStore('settings', {
    state: () => {
        return {
            theme: 'bumblebee',
        };
    },
    actions: {},
    getters: {},
    persist: true,
});
