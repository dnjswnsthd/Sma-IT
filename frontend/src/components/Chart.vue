<template>
    <!-- 그래프 그리기 -->
    <div>
        <canvas :id="id" height="50vh" width="80vw"></canvas>
    </div>
</template>

<script>
import Chart from 'chart.js';
import { mapState } from 'vuex';
export default {
    name: 'RadarCanvas',
    props: {
        id: String,
        labels: Array,
        data: Array,
    },
    data() {
        return {
            memberData: {
                datasets: [
                    {
                        data: [],
                        backgroundColor: 'rgba(188, 111, 241, .5)',
                        borderColor: '#ab47bc',
                        borderWidth: '1',
                    },
                ],
            },
            // chart options
            options: {
                legend: {
                    display: false,
                },
                reponsive: false,
                scale: {
                    angleLines: {
                        display: false,
                    },
                    ticks: {
                        min: 0,
                        max: 1,
                        stepSize: 0.2,
                        fontColor: '#ab47bc',
                        backgroundColor: '#000',
                        backdropColor: 'rgba(0,0,0,0)',
                    },
                    pointLabels: {
                        fontSize: 18,
                        fontColor: '#ab47bc',
                        fontFamily: 'CookieRunOTF-Bold',
                        src: `url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_twelve@1.0/CookieRunOTF-Bold00.woff') format('woff')`,
                        fontWeight: 'normal',
                        fontStyle: 'normal',
                    },
                },
            },
            chratObject: Object,
        };
    },
    computed: {
        ...mapState(['emotionAnalysis']),
    },
    watch: {
        data() {
            // 데이터가 변경 될 때마다 차트를 새로 그린다
            // this.chratObject.update();
            this.createCharts();
        },
    },
    mounted() {
        this.memberData.labels = this.labels;
        this.memberData.datasets[0].data = this.data;
        this.createCharts();
    },
    methods: {
        createCharts() {
            const ctx = document.getElementById(this.id);
            console.log(ctx);
            this.chratObject = new Chart(ctx, {
                type: 'radar',
                data: this.memberData,
                options: this.options,
            });
        },
    },
};
</script>
