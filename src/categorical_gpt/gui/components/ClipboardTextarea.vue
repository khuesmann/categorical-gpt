<template>
    <div>
        <textarea class="textarea w-full h-64" disabled>{{ value }}</textarea>
        <div class="text-right">
            <a class="btn btn-xs" @click="copyToClipboard(value)">
                <Icon name="ic:outline-content-copy" />
            </a>
        </div>
    </div>
</template>

<script lang="ts" setup>
const props = defineProps({
    text: {
        type: String,
        default: ''
    },
    json: {
        type: Object,
        default: null
    }
});

const prettyJsonString = (jsonObject: any) => {
    let str = JSON.stringify(jsonObject);
    console.log(str)
    str = str.replaceAll(',"', ', \n "');
    str = str.replace("{", "{\n");
    str = str.replace("}", "\n}");
    str = str.replaceAll(":[", ": [");
    return str;
};

const value = computed(() => {
    if (props.json) {
        return JSON.stringify(props.json);
    }
    return props.text;
});

const copyToClipboard = (copyText: string) => {
    navigator.clipboard.writeText(copyText);
};
</script>