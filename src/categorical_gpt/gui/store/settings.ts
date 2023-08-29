import { defineStore } from 'pinia';
import axios from 'axios';

interface ModelParams {
  temperature: number;
  top_p: number;
  n: number;
  prevent_cache?: boolean;
}

export const useSettingsStore = defineStore('settings', {
  state: () => {
    const env: any = useRuntimeConfig();
    return {
      model: 'gpt-3.5-turbo',
      theme: 'bumblebee',
      modelParams: {
        characteristic: {
          temperature: 0.7,
          top_p: 1,
          n: 1,
        } as ModelParams,
        heuristic: {
          temperature: 0.7,
          top_p: 1,
          n: 1,
        } as ModelParams,
        apply_heuristic: {
          temperature: 0.1,
          top_p: 0.1,
          n: 1,
        } as ModelParams,
      },
      availableModels: [...env.public.AVAILABLE_MODELS],
    };
  },
  actions: {},
  getters: {},
  persist: true,
});
