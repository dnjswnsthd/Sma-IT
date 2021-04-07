<template>
    <v-container>
        <v-row class="wrapBox">
            <div class="welcomeBox col-2">
                <img src="../assets/images/welcome.png" alt="welcome" />
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
                        <p class="guideMessage col-9">
                            {{ guideMessage }}
                        </p>
                        <v-spacer></v-spacer>
                        <div
                            @click="goCapture"
                            class="clickBtn col-2"
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
            <v-spacer></v-spacer>
            <div class="bannerBox col-2">
                <img src="../assets/images/banner.png" alt="배너이미지" />
            </div>
        </v-row>
    </v-container>
</template>

<script>
import http from '../api/axios';
import Axios from 'axios';
import { mapState } from 'vuex';
import swal from 'sweetalert';
export default {
    name: 'App',
    data() {
        return {
            video: {},
            canvas: {},
            captures: [],
            imgUrl: '',
            current: '',
            clickDialog: false,
            guideMessage: '화면의 중앙에 얼굴을 맞춰주시고 버튼을 클릭해 주세요.',
            maskDialog: false,
            duplicateFlag: false,
        };
    },
    computed: {
        ...mapState(['customerInfo', 'emotionAnalysis']),
    },
    mounted() {
        //Start the PC front camera and display real-time video on the video tag
        this.video = this.$refs.video;
        // navigator.mediaDevices는 현재 연결된 미디어 입력 장치
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
            const file = this.makeFile(this.captures[this.captures.length - 1]);
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

            // 현재 시간을 저장.
            this.current = year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec;
            console.log(this.current);
            if (!this.maskDialog) {
                http.post(`/face/onlymask`, formData)
                    .then((response) => {
                        console.log(response);
                        console.log('마스크 : ' + response.data);
                        // 마스크를 끼지 않았다면
                        if (response.data == 'NO MASK') {
                            swal('마스크를 착용해야 입장이 가능합니다.', {
                                icon: 'error',
                            });
                        } else {
                            swal('마스크 확인이 완료되었습니다.', {
                                icon: 'success',
                            });
                            this.guideMessage =
                                '얼굴인식을 위해 마스크를 잠시만 벗고 화면을 보고 버튼을 클릭해 주세요';
                            this.maskDialog = true;
                        }
                    })
                    .catch(() => {
                        swal('서버 에러!', {
                            icon: 'error',
                        });
                    });
            } else {
                // 얼굴인식.
                http.post(`/face/onlyface`, formData)
                    .then((response) => {
                        let member = {
                            age: '',
                            image: '',
                            interests: '',
                            join_date: '',
                            name: '',
                            requirements: '',
                            uuid: '',
                            visit_start: '',
                        };
                        // 중복체크
                        // state의 customerInfo 크기만큼 반복해서
                        for (var i = 0; i < this.$store.state.customerInfo.length; i++) {
                            if (
                                // uuid가 같은게 있으면
                                this.$store.state.customerInfo[i].uuid == response.data.member.uuid
                            ) {
                                // 중복 flag를 true로 바꾸고.
                                this.duplicateFlag = true;

                                // 알림
                                swal('이미방문하셨습니다.', {
                                    icon: 'success',
                                });
                                // 다시 초기화.
                                this.guideMessage =
                                    '화면중앙에 얼굴을 맞춰주시고 버튼을 클릭해 주세요.';
                                this.maskDialog = false;
                                break;
                            }
                        }
                        console.log('중복여부 : ' + this.duplicateFlag);
                        // 중복flag가 false인경우만 추가.
                        if (!this.duplicateFlag) {
                            member.age = response.data.member.age;
                            member.image = response.data.image;
                            member.interests = response.data.member.interests;
                            member.join_date = response.data.member.join_date;
                            member.name = response.data.member.name;
                            member.requirements = response.data.member.requirements;
                            member.uuid = response.data.member.uuid;
                            member.visit_start = this.current;

                            // vuex에 정보를 저장.
                            this.$store.commit('setCustomerInfo', member);
                            swal(response.data.member.name + '님 반가워요!', {
                                icon: 'success',
                            });
                            this.guideMessage =
                                '화면중앙에 얼굴을 맞춰주시고 버튼을 클릭해 주세요.';
                            this.maskDialog = false;
                            this.duplicateFlag = false;
                        }
                    })
                    .catch(() => {
                        swal('Guest님 반가워요!', {
                            icon: 'success',
                        });
                        this.guideMessage = '화면중앙에 얼굴을 맞춰주시고 버튼을 클릭해 주세요.';
                        this.maskDialog = false;
                    });
            }

            // Send imgURL image to Face API
            // 감정분석.
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
@import '../assets/css/cam.css';
</style>
