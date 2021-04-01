<template>
    <v-container>
        <v-row class="wrapBox">
            <div class="col-6">
                <p class="introduceMessage" style="padding-top:20px;">
                    만족도 평가가
                    <br />
                    저장됩니다.
                </p>
                <div class="satisfiedBox">
                    <chart :id="'satisfy'" :labels="labels" :data="data"></chart>
                </div>
            </div>
            <div class="col-6 cambox">
                <div class="camInnerBox">
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
                        height="650px"
                        playsinline
                        muted
                        autoplay
                        class="videoBox"
                    ></video>
                </div>
                <div class="divider"></div>
                <v-row>
                    <p class="guideMessage" style="padding-left:80px;">
                        얼굴을 가이드라인에 맞춰주시고
                        <br />
                        클릭 버튼을 눌러주세요!
                    </p>
                    <button @click="goCapture" style="color: gold; font-size:40px;">Click</button>
                </v-row>
            </div>
        </v-row>
    </v-container>
</template>

<script>
import Chart from '../components/Chart.vue';
import http from '../api/axios';
import Axios from 'axios';
import { mapState } from 'vuex';

export default {
    name: 'App',
    components: {
        chart: Chart,
    },
    data() {
        return {
            video: {},
            canvas: {},
            captures: [],
            imgUrl: '',
            formValues: {},
            current: '',
            member: {
                uuid: 0,
                anger: 0,
                contempt: 0,
                disgust: 0,
                fear: 0,
                happiness: 0,
                neutral: 0,
                sadness: 0,
                surprise: 0,
                end_visit: '',
            },
            labels: [
                'anger',
                'contempt',
                'disgust',
                'fear',
                'happiness',
                'neutral',
                'sadness',
                'surprise',
            ],
            data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        };
    },
    computed: {
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
    methods: {
        goCapture() {
            let context = this.canvas.getContext('2d').drawImage(this.video, 0, 0, 728, 650);
            console.log('context : ' + context);
            this.captures.push(this.canvas.toDataURL('image/png')); //Store the captured imag

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

            // Axios
            http.post('/face/onlyface', formData)
                .then((response) => {
                    console.log(response);
                    this.member.uuid = response.data.member.uuid;
                    console.log('uuid : ' + this.member.uuid);

                    alert('인식성공');

                    this.saveEmotion();
                    setInterval(this.$store.commit('deleteCustomerInfo', this.member.uuid), 1000);
                })
                .catch(() => {
                    alert('인식실패');
                });
            // console.log('uuid2 : ' + this.member.uuid);

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

                    var temp = response.data[0].faceAttributes.emotion;
                    console.log(temp[this.labels[6]]);
                    for (var i = 0; i < 8; i++) {
                        this.data[i] = temp[this.labels[i]];
                    }
                    this.member.anger = this.data[0];
                    this.member.contempt = this.data[1];
                    this.member.disgust = this.data[2];
                    this.member.fear = this.data[3];
                    this.member.happiness = this.data[4];
                    this.member.neutral = this.data[5];
                    this.member.sadness = this.data[6];
                    this.member.surprise = this.data[7];
                    this.member.end_visit = this.current;
                })
                .catch((error) => {
                    console.log(error.response);
                });
        },
        saveEmotion() {
            http.post('/member/emotion', this.member)
                .then(() => {
                    alert('저장성공.');
                })
                .catch(() => {
                    alert('저장실패!');
                });
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
    },
};
</script>
<style scoped>
@import '../assets/css/cam.css';
@import '../assets/css/camSatisfied.css';
</style>
