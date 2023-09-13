import { defineStore, acceptHMRUpdate } from 'pinia';
import { post } from '~/api/requests';
import { useSettingsStore } from './settings';

export interface Characteristic {
  name: string;
  is_active: boolean;
}

export interface CategoricalGPT {
  characteristic_certainties: Record<string, number>;
  characteristic_value_stds: Record<string, Record<string, number>>;
  characteristic_values: Record<string, Record<string, number>>;
  characteristics: Characteristic[];
  heuristic_certainties: Record<string, number>;
  heuristics: Record<string, string>;
}

const defaultCGPT = {
  characteristic_certainties: {},
  characteristic_value_stds: {},
  characteristic_values: {},
  characteristics: [],
  heuristic_certainties: {},
  heuristics: {},
} as CategoricalGPT;

const defaultResults = {
  ordering: [] as string[],
  color_coding: {} as Record<string, number[]>,
  embedding: {} as Record<string, number[]>,
  feature_vectors: {} as Record<string, number[]>,
  feature_vectors_dict: {} as Record<string, Record<string, number>>,
};

export const useDatasetStore = defineStore('dataset', {
  state: () => {
    const env: any = useRuntimeConfig();
    return {
      examples: { ...env.public.EXAMPLES },
      categoryName: '',
      categoryOptions: [] as string[],
      selectedCharacteristic: '',
      cgpt: { ...defaultCGPT },
      results: { ...defaultResults },
    };
  },
  actions: {
    reset() {
      this.$patch({
        categoryName: '',
        categoryOptions: [],
        selectedCharacteristic: '',
        cgpt: { ...defaultCGPT },
        results: { ...defaultResults },
      });
    },
    setCategoryOptions(options: string[]) {
      this.categoryOptions = options;
    },
    async loadCharacteristics(preventCache = false) {
      const structure = await post('/load-characteristics', {
        prevent_cache: preventCache,
        ...this.defaultRequestParameters,
      });
      this.cgpt.characteristics = structure.characteristics;
      this.cgpt.characteristic_certainties =
        structure.characteristic_certainties;
    },
    addCharacteristic(characteristicName: string) {
      const characteristic = {
        name: characteristicName,
        is_active: true,
      };
      this.cgpt.characteristics.push(characteristic);
      this.loadHeuristic(characteristicName);
      return characteristic;
    },
    async loadHeuristic(characteristic: string) {
      const structure = await post('/load-heuristic', {
        characteristic: characteristic,
        ...this.defaultRequestParameters,
      });

      this.cgpt.heuristics[characteristic] =
        structure?.heuristics[characteristic];

      this.cgpt.heuristic_certainties[characteristic] =
        structure?.heuristic_certainties[characteristic];
    },
    async loadValues(characteristic: string, heuristic: string) {
      if (!heuristic) {
        this.cgpt.characteristic_values[characteristic] =
          this.defaultValueAssignment;
        return this.defaultValueAssignment;
      }
      const structure = await post('/load-values', {
        characteristic: characteristic,
        heuristic: heuristic,
        ...this.defaultRequestParameters,
      });
      this.cgpt.characteristic_values[characteristic] =
        structure?.characteristic_values[characteristic] ||
        this.defaultValueAssignment;

      this.cgpt.characteristic_value_stds[characteristic] =
        structure?.characteristic_value_stds[characteristic];
    },
    async loadResults(orderingMethod: string | undefined) {
      const results = await post('/load-results', {
        structure: this.cgpt,
        ordering_method: orderingMethod,
        ...this.defaultRequestParameters,
      });
      this.$patch({
        results: results,
      });
    },
    async loadOrdering(orderingMethod: string | undefined) {
      const results = await post('/load-ordering', {
        structure: this.cgpt,
        ordering_method: orderingMethod,
        ...this.defaultRequestParameters,
      });
      this.results.ordering = results.ordering;
    },
  },
  getters: {
    defaultRequestParameters(state) {
      const settingsStore = useSettingsStore();
      return {
        category_name: state.categoryName,
        category_options: state.categoryOptions,
        model: settingsStore.model,
      };
    },
    defaultValueAssignment(state) {
      const valueAssignments: Record<string, number> = {};
      for (const option of state.categoryOptions) {
        valueAssignments[option] = -1;
      }
      return valueAssignments;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useDatasetStore, import.meta.hot));
}
