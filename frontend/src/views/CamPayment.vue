<template>
    <v-container>
        <v-spacer></v-spacer>
        <v-row>
            <div class="col-3 totalBox">
                <p class="totalMessage">버튼을 눌러<br />합계를 확인하세요.</p>
                <v-img
                    @mouseover="domouseover_won"
                    @click="checkTotal"
                    v-if="!won_c"
                    :src="require('../assets/images/won(w).png')"
                    class="totalBtn"
                ></v-img>
                <v-img
                    @click="checkTotal"
                    @mouseout="domouseout_won"
                    class="totalBtn"
                    v-else
                    :src="require('../assets/images/won.png')"
                ></v-img>
                <p class="totalMoney">{{ total }}</p>
            </div>
            <div class="col-6 cambox">
                <div class="camInBox">
                    <div class="camTopBox">
                        <video
                            ref="video"
                            id="video"
                            playsinline
                            muted
                            autoplay
                            class="videoBox"
                        ></video>
                    </div>
                    <div class="divider"></div>
                    <v-row class="camBottomBox">
                        <p class="guideMessage">
                            카메라를 정면으로 봐주시고
                            <br />
                            버튼을 클릭해주세요
                        </p>
                    </v-row>
                </div>
            </div>
            <div class="col-3 payBox">
                <p class="payMessage">결제를 원하시면 <br />버튼을 눌러주세요.</p>
                <v-img
                    v-if="!pay_c"
                    class="payBtn"
                    @mouseover="domouseover_pay"
                    @click="checkPayment"
                    :src="require('../assets/images/click(w).png')"
                ></v-img>
                <v-img
                    v-else
                    class="payBtn"
                    @mouseout="domouseout_pay"
                    @click="checkPayment"
                    :src="require('../assets/images/click.png')"
                ></v-img>
            </div>
        </v-row>
        <v-spacer></v-spacer>
    </v-container>
</template>

<script>
import swal from 'sweetalert';

export default {
    name: 'App',

    data() {
        return {
            img: null,
            camera: null,
            total: '',
            won_c: false,
            pay_c: false,
        };
    },
    mounted() {
        //Start the PC front camera and display real-time video on the video tag
        this.video = this.$refs.video;
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ audio: false, video: true }).then((stream) => {
                this.video.srcObject = stream;
                this.video.play();
            });
        }

        console.log(this.$refs.canvas);

        this.canvas = this.$refs.canvas;
    },
    methods: {
        domouseover_won() {
            this.won_c = true;
        },
        domouseout_won() {
            this.won_c = false;
        },
        domouseover_pay() {
            this.pay_c = true;
        },
        domouseout_pay() {
            this.pay_c = false;
        },
        checkTotal() {
            this.won_c = false;
            if (this.won_c == false) {
                console.log('금액확인');
                this.total = '￦ 1,000,000';
            }
        },
        checkPayment() {
            this.pay_c = !this.pay_c;
            if (this.pay_c == false) {
                swal('결제를 진행합니다', {
                    icon: 'success',
                });
            }
            this.total = '';
        },
    },
};
</script>
<style scoped>
@import '../assets/css/camPayment.css';
</style>
