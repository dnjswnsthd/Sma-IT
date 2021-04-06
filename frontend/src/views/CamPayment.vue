<template>
    <v-container>
        <v-spacer></v-spacer>
        <v-row>
            <div class="col-3 totalBox">
                <p class="totalMessage">
                    버튼을 눌러
                    <br />
                    합계를 확인하세요.
                </p>
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
                            얼굴인식을 위해 마스크를 잠시 벗고
                            <br />
                            화면을 보고 결제 버튼을 클릭해 주세요
                        </p>
                    </v-row>
                </div>
            </div>
            <div class="col-3 payBox">
                <p class="payMessage">
                    결제를 원하시면
                    <br />
                    버튼을 눌러주세요.
                </p>
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

                <v-dialog v-model="payDialog" persistent max-width="500">
                    <v-card>
                        <v-card-title class="headline" style="color:#000;">
                            결제 확인
                        </v-card-title>
                        <v-card-text>
                            <v-img
                                :src="require('../assets/images/card.png')"
                                style="margin-bottom:20px;"
                            ></v-img>
                            <p style="color:#000; font-size:20px;">카드번호 : {{ card_num }}</p>
                            <div class="divider" style="border:1px solid black;"></div>
                            <p style="color:#000;  font-size:20px;">
                                {{ card_name }}님 결제하시겠습니까?
                            </p>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="green darken-1" text @click="payDialog = false">
                                취소하기
                            </v-btn>
                            <v-btn color="green darken-1" text @click="completePayment">
                                결제하기
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
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
            card: {},
            card_num: '',
            card_name: '',
            payDialog: false,
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
                        this.card = response.data;
                        this.card_num = String(response.data.card_num);
                        console.log(response.data.card_num);
                        this.card_name = response.data.card_name;
                        this.changeCardNum(this.card_num);
                        this.payDialog = true;
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
        changeCardNum(card_num) {
            let cardnumtemp =
                card_num.substr(0, 4) +
                '-' +
                card_num.substr(4, 4) +
                '-' +
                card_num.substr(8, 4) +
                '-' +
                card_num.substr(12, 4);
            this.card_num = cardnumtemp;
        },
        completePayment() {
            swal('결제가 완료되었습니다.!', {
                icon: 'success',
            });
            this.payDialog = false;
        },
    },
};
</script>
<style scoped>
@import '../assets/css/camPayment.css';
</style>
