<template>
    <v-container>
        <v-row class="wrapBox">
            <div class="col-6">
                <div class="satisfiedOutBox">
                    <p class="satisfiedMessage">
                        만족도 평가가
                        <br />
                        저장됩니다.
                    </p>
                    <div class="satisfiedBox">
                        <!-- 만족도 그래프 -->
                        <chart :id="'satisfy'" :labels="labels" :data="emo"></chart>
                    </div>
                </div>
            </div>
            <div class="col-6 cambox">
                <div class="camInBox">
                    <div class="camTopBox">
                        <!-- 캡쳐한 이미지를 그려줄 canvas -->
                        <canvas
                            ref="canvas"
                            id="emo_canvas"
                            width="650px"
                            height="650px"
                            class="canvasBox"
                        ></canvas>
                        <!-- cam video -->
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
                    </v-row>
                </div>
            </div>
        </v-row>
    </v-container>
</template>

<script>
import Chart from '../components/Chart.vue';
import http from '../api/axios';
import Axios from 'axios';
import { mapState } from 'vuex';
import swal from 'sweetalert';
export default {
    name: 'CamSatisfied',
    components: {
        chart: Chart,
    },
    data() {
        return {
            video: {},
            canvas: {},
            captures: [],
            imgUrl: '',
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
            emo: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            clickDialog: false,
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

            let subscriptionKey = 'c2ade783cde74c478a3f5ec193cf6b3f'; // 감정분석 api키
            let uriBase = 'https://koreacentral.api.cognitive.microsoft.com/face/v1.0/detect/'; // 감정분석 uri
            //   https://smait.cognitiveservices.azure.com/

            //Convert the format of the image added at the end of the array and assign it to the imgURL format
            const file = this.makeblob(this.captures[this.captures.length - 1]); // 캡쳐한 이미지를 파일로 변경

            //   const fileName = 'canvas_img_'+new Date().getMilliseconds()+'.png';
            let formData = new FormData();
            formData.append('file', file);
            console.log(file);

            // 현재 시간 data 얻기.
            var curDate = new Date();
            var year = curDate.getUTCFullYear();
            var month = curDate.getMonth() + 1;
            var day = curDate.getDate();
            var hour = curDate.getHours();
            var min = curDate.getMinutes();
            var sec = curDate.getSeconds();

            // 현재시간을 저장
            this.current = year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec;

            // 얼굴인식
            http.post('/face/onlyface', formData)
                .then((response) => {
                    this.member.uuid = response.data.member.uuid;

                    this.saveEmotion(); // 감정분석결과 저장
                    setInterval(this.$store.commit('deleteCustomerInfo', this.member.uuid), 1000); // vuex에서 제거
                })
                .catch(() => {
                    swal('인식 실패!', {
                        icon: 'error',
                    });
                });
            // console.log('uuid2 : ' + this.member.uuid);

            // Send imgURL image to Face API
            // 감정분석
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
                    var temp = response.data[0].faceAttributes.emotion;
                    let emo = [
                        temp[this.labels[0]],
                        temp[this.labels[1]],
                        temp[this.labels[2]],
                        temp[this.labels[3]],
                        temp[this.labels[4]],
                        temp[this.labels[5]],
                        temp[this.labels[6]],
                        temp[this.labels[7]],
                    ];
                    this.emo = emo;

                    this.member.anger = emo[0];
                    this.member.contempt = emo[1];
                    this.member.disgust = emo[2];
                    this.member.fear = emo[3];
                    this.member.happiness = emo[4];
                    this.member.neutral = emo[5];
                    this.member.sadness = emo[6];
                    this.member.surprise = emo[7];
                    this.member.end_visit = this.current;
                })
                .catch((error) => {
                    console.log(error.response);
                });
        },
        // 감정분석 저장
        saveEmotion() {
            http.post('/member/emotion', this.member)
                .then(() => {
                    swal('저장 성공!', {
                        icon: 'success',
                    });
                })
                .catch(() => {
                    swal('저장 실패!', {
                        icon: 'error',
                    });
                });
        },
        // 캡쳐한 이미지를 파일로 만드는 메소드
        makeblob: function(dataURL) {
            let BASE64_MARKER = ';base64,';
            // BASE64_MARKER와 일치하는 것이 없다면
            if (dataURL.indexOf(BASE64_MARKER) == -1) {
                let parts = dataURL.split(',');
                let contentType = parts[0].split(':')[1];
                let raw = decodeURIComponent(parts[1]);
                return new File([raw], { type: contentType });
            }
            // BASE64_MARKER와 일치하는 것이 있다면
            let parts = dataURL.split(BASE64_MARKER);
            let fileName = 'captureImage.jpg'; // 파일이름 지정
            let contentType = parts[0].split(':')[1];
            let raw = window.atob(parts[1]); // 인코딩
            let rawLength = raw.length;
            let uInt8Array = new Uint8Array(rawLength);
            for (let i = 0; i < rawLength; ++i) {
                uInt8Array[i] = raw.charCodeAt(i);
            }
            return new File([uInt8Array], fileName, { type: contentType });
        },
        // 호버시 dialog 변경
        hoverClickBtn() {
            this.clickDialog = true;
        },
        outClickBtn() {
            this.clickDialog = false;
        },
    },
};
</script>
<style scoped>
@import '../assets/css/camSatisfied.css';
</style>
