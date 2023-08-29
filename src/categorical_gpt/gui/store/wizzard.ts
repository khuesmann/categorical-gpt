import { defineStore, acceptHMRUpdate } from 'pinia';
import { useRouter } from 'nuxt/app';
import { Characteristic, useDatasetStore } from './dataset';

interface Step {
  name: string;
  number: number;
  path: string;
}

const steps: Step[] = [
  {
    name: 'Data Input',
    number: 2,
    path: '/',
  },
  {
    name: 'Characteristics',
    number: 3,
    path: '/characteristics',
  },
  {
    name: 'Value Assignment',
    number: 4,
    path: '/value-assignments',
  },
  {
    name: 'Results',
    number: 5,
    path: '/results',
  },
  {
    name: 'Export',
    number: 6,
    path: '/export',
  },
];

const defaultIsStepLoading = {
  2: false,
  3: false,
  4: false,
  5: false,
  6: false,
} as Record<number, boolean>;

const defaultHasStepLoaded = {
  2: true,
  3: false,
  4: false,
  5: false,
  6: false,
} as Record<number, boolean>;

const defaultStepProgress = {
  2: 0,
  3: 0,
  4: 0,
  5: 0,
  6: 0,
} as Record<number, number>;

export const useWizzardStore = defineStore('wizzard', {
  state: () => {
    return {
      isStepLoading: { ...defaultIsStepLoading },
      hasStepLoaded: { ...defaultHasStepLoaded },
      stepProgress: { ...defaultStepProgress },
      steps: steps,
      currentStep: steps[0],
    };
  },
  actions: {
    reset() {
      this.$patch({
        isStepLoading: { ...defaultIsStepLoading },
        hasStepLoaded: { ...defaultHasStepLoaded },
        stepProgress: { ...defaultStepProgress },
      });
    },
    async loadStep(step: Step, redirect = true) {
      if (step.number == 3 || step.number == 4) {
        if (this.hasStepLoaded[step.number]) {
          this.setStep(step, true);
          return;
        }
      }

      const prevStep: Step | undefined = this.steps.find(
        (s) => s.number === step.number - 1,
      );
      if (prevStep && !this.hasStepLoaded[prevStep.number]) {
        await this.loadStep(prevStep, false);
      }

      const datasetStore = useDatasetStore();

      this.isStepLoading[step.number] = true;

      if (!this.isStepReady(this.currentStep)) {
        this.isStepLoading[step.number] = false;
        this.setStep(this.currentStep);
        return;
      }

      try {
        this.stepProgress[step.number] += 10;

        switch (step.number) {
          case 2:
            console.log('Loaded step ', step.name);
            this.setStep(step, redirect);
            break;
          case 3:
            await datasetStore.loadCharacteristics();
            const heuristicProgressStepSize =
              90 / (datasetStore.cgpt.characteristics.length + 1);
            await Promise.all(
              datasetStore.cgpt.characteristics.map(
                (characteristic: Characteristic) => {
                  return datasetStore
                    .loadHeuristic(characteristic.name)
                    .then(() => {
                      this.stepProgress[step.number] +=
                        heuristicProgressStepSize;
                    });
                },
              ),
            );
            this.setStep(step, redirect);
            break;
          case 4:
            const valueAssignmentProgressStepSize =
              90 / (datasetStore.cgpt.characteristics.length + 1);

            await Promise.all(
              datasetStore.cgpt.characteristics.map(
                (characteristic: Characteristic) => {
                  return datasetStore
                    .loadValues(
                      characteristic.name,
                      datasetStore.cgpt.heuristics[characteristic.name],
                    )
                    .then(() => {
                      this.stepProgress[step.number] +=
                        valueAssignmentProgressStepSize;
                    });
                },
              ),
            );
            this.setStep(step, redirect);
            break;
          case 5:
            await datasetStore.loadResults(undefined);
            this.setStep(step, redirect);
            break;
          case 6:
            this.setStep(step, redirect);
            break;
        }
        this.hasStepLoaded[step.number] = true;
      } catch (error) {
        console.error(error);
      }
      this.isStepLoading[step.number] = false;
      this.stepProgress[step.number] = 100;
    },
    setStep(step: Step, redirect = true) {
      if (redirect) {
        const router = useRouter();
        router.push(step.path);
      }
      this.$patch({
        currentStep: step,
      });
    },
  },
  getters: {
    isLoading(): boolean {
      for (const key in this.isStepLoading) {
        if (this.isStepLoading[key]) {
          return true;
        }
      }
      return false;
    },
    nextStep(): Step | null {
      const nextStep = this.steps.find(
        (step) => step.number === this.currentStep.number + 1,
      );
      if (nextStep) {
        return nextStep;
      }
      return null;
    },
    prevStep(): Step | null {
      const prevStep = this.steps.find(
        (step) => step.number === this.currentStep.number - 1,
      );
      if (prevStep) {
        return prevStep;
      }
      return null;
    },
    isStepReady: (state) => (step: Step) => {
      const datasetStore = useDatasetStore();
      switch (step.number) {
        case 2:
          if (
            datasetStore.categoryName === '' ||
            datasetStore.categoryOptions.length === 0
          ) {
            return false;
          }
          return true;
        case 3:
          return true;
        case 4:
          return true;
        case 5:
          return true;
        case 6:
          return true;
      }
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useWizzardStore, import.meta.hot));
}
