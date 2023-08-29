<template>
  <div class="flex gap-4 p-4">
    <div class="flex-grow flex flex-col gap-4">


      <div class="alert alert-info" v-if="!canEdit">
        <Icon name="zondicons:information-outline" />
        <span>You are not able to make changes to the current category and it's options, because you have already loaded
          the subsequent steps.</span>
        <div>
          <button class="btn btn-sm btn-primary" @click="reset()">Start new</button>
        </div>
      </div>
      <div>
        <div class="form-control">
          <label class="input-group input-group-vertical">
            <span class="bg-base-200">Category name</span>
            <input v-model="datasetStore.categoryName" type="text" placeholder="Type in the name of the category"
              :disabled="!canEdit" class="input input-bordered" />
          </label>
        </div>
      </div>
      <div>
        <div class="form-control">
          <label class="input-group input-group-vertical">
            <span class="bg-base-200">Category options</span>
            <textarea v-model="categoryOptions" @input="updateOptions" rows="8" class="textarea textarea-bordered"
              :disabled="!canEdit" placeholder="Type in a comma-seperated list of all category options" />
          </label>
        </div>
      </div>

      <div>
        <ul>
          <li v-for="example in datasetStore.examples">
            <button @click="loadExample(example)">
              {{ example.name }}: {{ example.description }}
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div v-if="datasetStore.categoryOptions.length > 0" class="w-80">
      <table class="table w-full table-compact">
        <tbody>
          <!-- row 1 -->
          <tr v-for="option in datasetStore.categoryOptions" :key="option">
            <td>{{ option }}</td>
            <td class="text-right">
              <a class="cursor-pointer" @click="removeOption(option)">
                <Icon name="ic:sharp-remove-circle-outline" />
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useWizzardStore } from "~/store/wizzard";
import { useDatasetStore } from "~/store/dataset";
const wizzardStore = useWizzardStore();
const datasetStore = useDatasetStore();

const categoryOptions = ref("");

const updateOptions = () => {
  let optionsArray = categoryOptions.value.split(",").map((x) => x.trim()).filter((x) => x !== "")
  optionsArray = [...new Set(optionsArray)]
  datasetStore.setCategoryOptions(optionsArray);
}

const removeOption = (option: string) => {
  categoryOptions.value = datasetStore.categoryOptions.filter(
    (item: string) => item !== option,
  ).join(',')
  updateOptions()
}

const reset = () => {
  wizzardStore.reset()
  datasetStore.reset()
  datasetStore.categoryName = ''
  categoryOptions.value = ''
}

const loadExample = (example: any) => {
  reset()
  datasetStore.categoryName = example.categoryName
  categoryOptions.value = example.options
  updateOptions()

}

const canEdit = computed(() => {
  return !wizzardStore.hasStepLoaded[3]
})

onMounted(() => {
  wizzardStore.loadStep(wizzardStore.steps[0])
  categoryOptions.value = datasetStore.categoryOptions.join(',')
})
</script>
