<template>
    <div class="relative h-[80vh]">
        <div class="absolute left-0 top-0 z-10">
            <label class="flex items-center">
                <input type="checkbox" class="checkbox mr-2" v-model="isColored" /> <span>Show colors</span>
            </label>
        </div>
        <div ref="canvas" class="h-full"></div>
    </div>
</template>

<script setup>
import Plotly from "plotly.js-dist";

const props = defineProps({
    points: {
        type: Array,
        default: () => [],
    },
    // isColored: {
    // type: Boolean,
    // default: true
    // }
});

const emit = defineEmits(["selected"]);

const isColored = ref(true);

const opacity = 1
// Remove 'px' from the end and convert to a number
const fontSize = Number(window.getComputedStyle(document.documentElement).fontSize.slice(0, -2));

watch(
    () => props.points,
    (newPoints) => {
        rerender();
    },
    { deep: true }
);

watch(
    () => isColored.value,
    () => rerender(),
    { deep: true }
)

const rerender = () => {
    Plotly.react(canvas.value, data.value, layout);
};

const canvas = ref(null);

const data = computed(() => {
    const x = props.points.map((point) => point.x);
    const y = props.points.map((point) => point.y);
    return [
        {
            x,
            y,
            mode: "markers",
            type: "scatter",
            text: props.points.map((point) => point.text),
            marker: {
                size: fontSize * 1.,
                color: isColored.value ? props.points.map((point) => `rgba(${point.color[0]}, ${point.color[1]}, ${point.color[2]}, ${opacity}})`) : 'black',
            },
        },
        {
            x: x,
            y: y,
            mode: "text",
            type: "scatter",
            text: props.points.map((point) => point.label),
            textposition: "top",
            textfont: {
                size: fontSize,
            },
        },
    ];
});

var layout = {
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0,
        pad: 4,
        bgcolor: "rgba(0, 0, 0, 0)",
    },
    xaxis: {
        showgrid: false,
        showticklabels: false,
        zeroline: false,
    },
    yaxis: {
        showgrid: false,
        showticklabels: false,
        zeroline: false,
    },
    dragmode: "zoom",
    showlegend: false,
};

onMounted(() => {
    setTimeout(() => {
        Plotly.newPlot(canvas.value, data, layout);
        canvas.value.on("plotly_selected", function (eventData) {
            if (eventData && eventData.points && eventData.points.length > 0) {
                const pointIndexs = eventData.points.map((point) => point.pointIndex);
                emit("selected", pointIndexs);
            }
        });
        rerender();
    }, 0);
});
</script>
