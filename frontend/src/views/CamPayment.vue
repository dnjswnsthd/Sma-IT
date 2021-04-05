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
                        <canvas
                            ref="canvas"
                            id="emo_canvas"
                            width="650px"
                            height="650px"
                            class="canvasBox"
                        ></canvas>
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
import http from '../api/axios';
export default {
    name: 'App',

    data() {
        return {
            video: {},
            canvas: {},
            captures: [],
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

            let context = this.canvas.getContext('2d').drawImage(this.video, 0, 0, 728, 650);
            console.log('context : ' + context);
            // console.log(this.canvas.toDataURL('image/png'));
            this.captures.push(this.canvas.toDataURL('image/png')); //Store the captured image in the "captures" array

            //   //Convert the format of the image added at the end of the array and assign it to the imgURL format
            const file = this.makeFile(this.captures[this.captures.length - 1]);
            console.log('imgURL : ' + file);

            //   const fileName = 'canvas_img_'+new Date().getMilliseconds()+'.png';
            let formData = new FormData();
            formData.append('file', file);
            console.log(file);

            if (this.pay_c == false) {
                http.post(`/pay/`, formData)
                    .then((response) => {
                        console.log(response.data);
                    })
                    .catch((response) => {
                        console.log(response);
                        swal('에러발생!!', {
                            icon: 'error',
                        });
                    });
            }
            this.total = '';
        },
        makeFile: function(dataURL) {
            let BASE64_MARKER = ';base64,';
            if (dataURL.indexOf(BASE64_MARKER) == -1) {
                let parts = dataURL.split(',');
                let contentType = parts[0].split(':')[1];
                let raw = decodeURIComponent(parts[1]);
                return new File([raw], { type: contentType });
            }
            let parts = dataURL.split(BASE64_MARKER);
            let fileName = 'captureImage.jpg';
            let contentType = parts[0].split(':')[1];
            let raw = window.atob(parts[1]);
            let rawLength = raw.length;
            let uInt8Array = new Uint8Array(rawLength);
            for (let i = 0; i < rawLength; ++i) {
                uInt8Array[i] = raw.charCodeAt(i);
            }
            return new File([uInt8Array], fileName, { type: contentType });
        },
    },
};
</script>
<style scoped>
@import '../assets/css/camPayment.css';
</style>
