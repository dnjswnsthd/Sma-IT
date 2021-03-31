<template>
    <v-container>
        <v-row class="wrapBox">
            <div class="welcomeBox col-2">
                <!-- <p class="introduceMessage" style="padding-top:300px; padding-left:100px">
                    print <br />(Welcome to Visit);
                </p> -->
                <img
                    src="../assets/images/welcome.png"
                    alt="welcome"
                    style="width:300px; margin-left:50px; margin-top : 100px;"
                />
            </div>
            <v-spacer></v-spacer>
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
                            <br />버튼을 클릭해주세요
                        </p>
                        <v-spacer></v-spacer>
                        <div
                            @click="goCapture"
                            class="clickBtn"
                            @mouseover="hoverClickBtn"
                            @mouseout="outClickBtn"
                        >
                            <img
                                v-if="!clickDialog"
                                src="../assets/images/click.png"
                                alt="클릭버튼"
                            />
                            <img v-else src="../assets/images/click_color.png" alt="클릭버튼" />
                        </div>

                        <!-- <button @click="goCapture" style="color: gold; font-size:40px; ">
                            Click
                        </button> -->
                    </v-row>
                </div>
            </div>
            <v-spacer></v-spacer>
            <div class="productBox col-2" style="padding-top: 80px;">
                <img src="../assets/images/banner03.png" alt="배너이미지" style="height:700px;" />
            </div>
        </v-row>
        <!-- <v-btn @click="goCamPayment">결제화면보기</v-btn> -->
    </v-container>
</template>

<script>
import http from '../api/axios';
import Axios from 'axios';
import { mapState } from 'vuex';

export default {
    name: 'App',
    data() {
        return {
            video: {},
            canvas: {},
            captures: [],
            testTimer: '',
            decodeUrl: '',
            imgUrl: '',
            formValues: {},
            current: '',
            clickDialog: false,
        };
    },
    computed: {
        device: function() {
            return this.devices.find((n) => n.deviceId === this.deviceId);
        },
        ...mapState(['customerInfo', 'emotionAnalysis']),
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
    watch: {
        camera: function(id) {
            this.deviceId = id;
        },
        devices: function() {
            // Once we have a list select the first one
            const [first, ...tail] = this.devices; // eslint-disable-line no-unused-vars
            if (first) {
                this.camera = first.deviceId;
                this.deviceId = first.deviceId;
            }
        },
    },
    methods: {
        goCapture() {
            // console.log(this.$refs.canvas)

            let context = this.canvas.getContext('2d').drawImage(this.video, 0, 0, 728, 650);
            console.log('context : ' + context);
            this.captures.push(this.canvas.toDataURL('image/png')); //Store the captured image in the "captures" array

            let subscriptionKey = 'c2ade783cde74c478a3f5ec193cf6b3f';
            let uriBase = 'https://koreacentral.api.cognitive.microsoft.com/face/v1.0/detect/';
            //   https://smait.cognitiveservices.azure.com/
            let params = {
                returnFaceId: 'false',
                returnFaceLandmarks: 'true',
                returnFaceAttributes: 'emotion',
            };
            console.log(params);
            //   //Convert the format of the image added at the end of the array and assign it to the imgURL format
            const file = this.makeblob(this.captures[this.captures.length - 1]);
            console.log('imgURL : ' + file);

            //   const fileName = 'canvas_img_'+new Date().getMilliseconds()+'.png';
            let formData = new FormData();
            formData.append('file', file);
            console.log(file);

            var curDate = new Date();
            var year = curDate.getUTCFullYear();
            var month = curDate.getMonth() + 1;
            var day = curDate.getDate();
            var hour = curDate.getHours();
            var min = curDate.getMinutes();
            var sec = curDate.getSeconds();

            this.current = year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec;
            console.log(this.current);
            http.post(`/face/${this.current}`, formData)
                .then((response) => {
                    console.log(response.data.member);
                    this.$store.commit('setCustomerInfo', response.data.member);
                    console.log('------------------------');
                    console.log(this.customerInfo);
                    alert('승공');
                })
                .catch(() => {
                    alert('실패');
                });
            //Send imgURL image to Face API
            Axios.post(
                uriBase +
                    '?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,emotion',
                file,
                {
                    headers: {
                        'Content-Type': 'application/octet-stream',
                        'Ocp-Apim-Subscription-Key': subscriptionKey,
                    },
                }
            )
                .then((response) => {
                    console.log(response.data[0].faceAttributes.emotion);
                    this.$store.commit(
                        'setEmotionAnalysis',
                        response.data[0].faceAttributes.emotion
                    );
                    console.log();
                })
                .catch((error) => {
                    console.log(error.response);
                });
            this.clickDialog = false;
        },
        makeblob: function(dataURL) {
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
        hoverClickBtn() {
            this.clickDialog = true;
        },
        outClickBtn() {
            this.clickDialog = false;
        },
        goCamPayment() {
            this.$router.push({ name: 'CamSatisfied' });
        },
    },
};
</script>
<style scoped>
@import '../assets/css/cam.css';
.camInBox {
    width: calc(100% - 100px);
    margin: 60px auto;
}
.camTopBox {
    height: 75%;
    position: relative;
}
.camBottomBox {
    height: 25%;
    padding: 0 100px;
}
.canvasBox {
    display: block;
    position: absolute;
    left: 50%;
    top: 0;
    margin-top: 100px;
    margin-left: -200px;
    z-index: -1;
}

.videoBox {
    display: block;
    margin: 0 auto;
    width: 750px;
    height: 565px;
    border-radius: 20px;
    border: 4px solid #fff;
}
.productBox {
    margin-right: 50px;
}
.productBox img {
    display: block;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    border: 3px solid #6e0b40;
    /* box-shadow: 0px 0px 3px 7px rgb(255, 255, 255); */
}

.clickBtn {
    width: 80px;
}
.clickBtn img {
    display: block;
    width: 80px;
    height: 80px;
    margin: 0 auto;
}
</style>
